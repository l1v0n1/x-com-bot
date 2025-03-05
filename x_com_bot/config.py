import os
from typing import Dict
from dotenv import load_dotenv

def load_config() -> Dict[str, str]:
    """
    Load configuration from environment variables
    
    Returns:
        Dictionary containing configuration values
    """
    load_dotenv()
    
    required_vars = [
        'TWITTER_API_KEY',
        'TWITTER_API_SECRET',
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_TOKEN_SECRET',
        'TWITTER_BEARER_TOKEN',  # Добавляем Bearer токен для API v2
    ]
    
    config = {}
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value is None:
            missing_vars.append(var)
        config[var.lower()] = value
    
    # Добавляем имя модели (необязательный параметр)
    model_name = os.getenv('MODEL_NAME')
    if model_name:
        config['model_name'] = model_name
        print(f"Используем модель из .env: {model_name}")
    else:
        config['model_name'] = 'deepseek-r1:1.5b'  # Модель по умолчанию
        print(f"Модель не указана в .env, используем: {config['model_name']}")
    
    # Добавляем интервал проверки (необязательный параметр)
    check_interval = os.getenv('CHECK_INTERVAL')
    if check_interval:
        try:
            config['check_interval'] = int(check_interval)
            print(f"Используем интервал проверки из .env: {check_interval} секунд")
        except ValueError:
            config['check_interval'] = 60
            print(f"Неверный формат CHECK_INTERVAL в .env, используем: {config['check_interval']} секунд")
    else:
        config['check_interval'] = 60  # Интервал по умолчанию
        print(f"Интервал проверки не указан в .env, используем: {config['check_interval']} секунд")
    
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )
    
    return config 