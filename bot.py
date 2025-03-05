import os
import time
from typing import Dict, Optional
import tweepy
from loguru import logger
from tenacity import retry, wait_exponential, stop_after_attempt
from x_com_bot.model_manager import ModelManager

class XComBot:
    def __init__(self, config: Dict[str, str]):
        """
        Initialize the bot with configuration
        
        Args:
            config: Dictionary containing API keys and configuration
                Required keys:
                - twitter_api_key
                - twitter_api_secret
                - twitter_access_token
                - twitter_access_token_secret
                Optional keys:
                - model_name (имя модели Ollama для использования)
                - check_interval (интервал проверки в секундах)
        """
        self.setup_twitter_client(config)
        self.setup_logging()
        
        # Получаем интервал проверки из конфига
        self.check_interval = int(config.get('check_interval', 60))
        logger.info(f"Интервал проверки: {self.check_interval} секунд")
        
        # Инициализация модели через Ollama
        try:
            model_name = config.get('model_name')
            logger.info(f"Инициализация модели: {model_name}")
            
            self.model_manager = ModelManager(model_name=model_name)
            
            # Проверяем доступные модели
            available_models = self.model_manager.list_available_models()
            if not available_models:
                raise ValueError(
                    "Ollama не запущена или недоступна. "
                    "Убедитесь, что сервис запущен командой: ollama serve"
                )
            
            logger.info(f"Доступные модели: {', '.join(available_models)}")
            
            # Проверяем и загружаем модель
            self.model_manager.ensure_model_exists()
            logger.info(f"Модель {self.model_manager.model_name} готова к использованию")
            
        except Exception as e:
            logger.error(f"Ошибка при инициализации модели: {e}")
            if 'available_models' in locals() and available_models:
                logger.info(
                    "Для использования другой модели, укажите MODEL_NAME в .env файле. "
                    f"Доступные модели: {', '.join(available_models)}"
                )
            raise
        
        # Rate limiting configuration
        self.request_delay = 2.0  # Delay between requests in seconds
        self.last_request_time = 0
        
    def setup_twitter_client(self, config: Dict[str, str]) -> None:
        """Set up Twitter API v2 client"""
        self.twitter_client = tweepy.Client(
            bearer_token=config['twitter_bearer_token'],
            consumer_key=config['twitter_api_key'],
            consumer_secret=config['twitter_api_secret'],
            access_token=config['twitter_access_token'],
            access_token_secret=config['twitter_access_token_secret'],
            wait_on_rate_limit=True  # Автоматическая обработка rate limits
        )
        logger.info("Twitter API v2 client initialized")

    def setup_logging(self) -> None:
        """Configure logging"""
        logger.add(
            "bot.log",
            rotation="500 MB",
            level="INFO",
            format="{time} {level} {message}"
        )

    @retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(3))
    async def generate_response(self, context: str, query: str) -> str:
        """
        Generate response using Ollama model
        
        Args:
            context: Post context
            query: User query
            
        Returns:
            Generated response text
        """
        try:
            # Формируем промпт
            prompt = f"""You are an AI assistant responding to posts on X.com (Twitter).
            Your task is to provide brief and relevant responses within 280 characters.

            Original post: {context}
            Reply to respond to: {query}

            Please provide a concise and engaging response that fits Twitter's character limit."""

            # Генерируем ответ через Ollama
            return self.model_manager.generate_response(
                prompt=prompt,
                max_tokens=280,  # Лимит Twitter
                temperature=0.7
            )
                    
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            raise

    def enforce_rate_limit(self) -> None:
        """Enforce rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.request_delay:
            time.sleep(self.request_delay - time_since_last)
        self.last_request_time = time.time()

    @retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(3))
    def post_response(self, response: str, reply_to_id: str) -> None:
        """
        Post response to X.com using API v2
        
        Args:
            response: Text to post
            reply_to_id: ID of tweet to reply to
        """
        try:
            self.enforce_rate_limit()
            self.twitter_client.create_tweet(
                text=response,
                in_reply_to_tweet_id=reply_to_id
            )
            logger.info(f"Posted response to tweet {reply_to_id}")
        except Exception as e:
            logger.error(f"Error posting response: {e}")
            raise

    def get_mentions(self, since_id: Optional[str] = None) -> list:
        """
        Get mentions and replies using Twitter API v2
        
        Args:
            since_id: Only return tweets more recent than this ID
            
        Returns:
            List of tweets
        """
        try:
            self.enforce_rate_limit()
            
            # Получаем ID текущего пользователя
            me = self.twitter_client.get_me()
            user_id = me.data.id
            
            # Получаем твиты через API v2 (упоминания и ответы)
            tweets = self.twitter_client.get_users_tweets(
                id=user_id,
                since_id=since_id,
                tweet_fields=['referenced_tweets', 'text', 'in_reply_to_user_id'],
                expansions=['referenced_tweets.id']
            )
            
            if not tweets.data:
                return []
                
            # Фильтруем только ответы и упоминания
            relevant_tweets = [
                tweet for tweet in tweets.data 
                if (tweet.referenced_tweets and any(ref.type == 'replied_to' for ref in tweet.referenced_tweets)) or
                   (tweet.text and f"@{me.data.username}" in tweet.text)
            ]
                
            logger.info(f"Retrieved {len(relevant_tweets)} new interactions")
            return relevant_tweets
            
        except Exception as e:
            logger.error(f"Error getting tweets: {e}")
            return []

    async def process_mention(self, mention) -> None:
        """
        Process a single mention using API v2
        
        Args:
            mention: Tweet object from API v2
        """
        try:
            # Получаем оригинальный твит, на который был ответ
            if mention.referenced_tweets:
                for ref in mention.referenced_tweets:
                    if ref.type == 'replied_to':
                        original_tweet = self.twitter_client.get_tweet(
                            ref.id,
                            tweet_fields=['text']
                        )
                        context = original_tweet.data.text
                        break
                else:
                    logger.warning(f"No reply reference found for mention {mention.id}")
                    return
            else:
                logger.warning(f"No references found for mention {mention.id}")
                return
            
            # Generate and post response
            response = await self.generate_response(context, mention.text)
            self.post_response(response, mention.id)
            
        except Exception as e:
            logger.error(f"Error processing mention {mention.id}: {e}")

    async def run(self) -> None:
        """
        Main bot loop
        """
        last_mention_id = None
        
        while True:
            try:
                mentions = self.get_mentions(since_id=last_mention_id)
                
                if mentions:
                    last_mention_id = mentions[0].id
                    
                    for mention in mentions:
                        await self.process_mention(mention)
                        
                time.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(self.check_interval) 