import os
import json
import requests
from loguru import logger
from typing import Optional, Dict, Any
import time

class ModelManager:
    """Менеджер для работы с моделями через Ollama"""
    
    def __init__(self, model_name: str = "deepseek-r1:1.5b"):
        """
        Initialize model manager
        
        Args:
            model_name: Name of the Ollama model to use
        """
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434"
        
    def ensure_model_exists(self) -> None:
        """Ensure the model exists and is ready to use"""
        available_models = self.list_available_models()
        if not available_models:
            raise ValueError(
                "Нет доступных моделей. Убедитесь, что Ollama запущена и хотя бы одна модель установлена.\n"
                "Для установки модели используйте команду: ollama pull MODEL_NAME"
            )
            
        if self.model_name not in available_models:
            raise ValueError(
                f"Модель {self.model_name} не найдена. Доступные модели:\n"
                f"{', '.join(available_models)}\n"
                "Для использования другой модели укажите её в .env файле через MODEL_NAME=имя_модели\n"
                "Или установите новую модель командой: ollama pull MODEL_NAME"
            )
            
        logger.info(f"Модель {self.model_name} найдена и готова к использованию")

    def _check_model_exists(self) -> bool:
        """
        Check if model exists locally
        
        Returns:
            bool: True if model exists, False otherwise
        """
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                return any(model["name"] == self.model_name for model in models)
            return False
        except Exception as e:
            logger.error(f"Ошибка при проверке модели: {e}")
            return False

    def list_available_models(self) -> list:
        """
        Get list of available models
        
        Returns:
            list: List of available model names
        """
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                return [model["name"] for model in response.json().get("models", [])]
            return []
        except Exception as e:
            logger.error(f"Ошибка при получении списка моделей: {e}")
            return []

    def generate_response(self, prompt: str, max_tokens: int = 280, temperature: float = 0.7) -> str:
        """
        Generate response using the model
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum number of tokens in response
            temperature: Temperature for response generation
            
        Returns:
            str: Generated response
        """
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                }
            )
            
            if response.status_code != 200:
                raise ValueError(f"Ошибка генерации: {response.text}")
                
            result = response.json()
            return result.get("response", "").strip()
            
        except Exception as e:
            logger.error(f"Ошибка при генерации ответа: {e}")
            raise 