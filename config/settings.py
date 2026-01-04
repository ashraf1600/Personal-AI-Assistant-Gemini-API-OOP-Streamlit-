"""
Configuration and Settings Management
Handles environment variables and application settings
"""
import os
from dotenv import load_dotenv
from typing import Optional


class Settings:
    """Manages application configuration and environment variables"""
    
    def __init__(self):
        """Initialize settings and load environment variables"""
        load_dotenv()
        self._api_key: Optional[str] = None
        self._model_name: str = "gemini-pro"
        self._max_tokens: int = 1000
        self._temperature: float = 0.7
        
    def load_api_key(self) -> str:
        """
        Load and validate Gemini API key from environment
        
        Returns:
            str: The API key
            
        Raises:
            ValueError: If API key is not found
        """
        if self._api_key is None:
            self._api_key = os.getenv("GEMINI_API_KEY") # API KEY nicche from .env
            
        if not self._api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Please set it in your .env file"
            )
            
        return self._api_key
    
    @property
    def model_name(self) -> str:
        """Get the model name"""
        return os.getenv("GEMINI_MODEL", self._model_name) # Model name nicche from .env
    
    @property
    def max_tokens(self) -> int:
        """Get maximum tokens for generation"""
        return int(os.getenv("MAX_TOKENS", self._max_tokens))
    
    @property
    def temperature(self) -> float:
        """Get temperature for generation"""
        return float(os.getenv("TEMPERATURE", self._temperature))
    
    def validate(self) -> bool:
        """
        Validate all required settings
        
        Returns:
            bool: True if all settings are valid
        """
        try:
            self.load_api_key()
            return True
        except ValueError:
            return False