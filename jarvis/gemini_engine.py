"""
Gemini API Engine
Handles all interactions with Google's Gemini API
"""
import google.generativeai as genai
from typing import Optional, Dict, Any


class GeminiEngine:
    """Handles communication with Gemini API"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-pro"):
        """
        Initialize the Gemini Engine
        
        Args:
            api_key: Google Gemini API key
            model_name: Name of the Gemini model to use
        """
        self.api_key = api_key
        self.model_name = model_name
        self._configure_api()
        self._initialize_model()
        
    def _configure_api(self) -> None:
        """Configure the Gemini API with the API key"""
        try:
            genai.configure(api_key=self.api_key)
        except Exception as e:
            raise ConnectionError(f"Failed to configure Gemini API: {str(e)}")
    
    def _initialize_model(self) -> None:
        """Initialize the generative model"""
        try:
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as e:
            raise ValueError(f"Failed to initialize model '{self.model_name}': {str(e)}")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from Gemini API
        
        Args:
            prompt: The input prompt for the model
            **kwargs: Additional generation parameters (temperature, max_tokens, etc.)
            
        Returns:
            str: Generated response from the model
            
        Raises:
            RuntimeError: If generation fails
        """
        try:
            # Create generation config if kwargs provided
            generation_config = None
            if kwargs:
                generation_config = genai.types.GenerationConfig(**kwargs)
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Extract text from response
            if response and response.text:
                return response.text
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
                
        except Exception as e:
            error_msg = str(e).lower()
            
            # Handle specific error cases
            if "api key" in error_msg:
                raise RuntimeError("Invalid API key. Please check your configuration.")
            elif "quota" in error_msg:
                raise RuntimeError("API quota exceeded. Please try again later.")
            elif "safety" in error_msg:
                return "I cannot provide a response to that request due to safety guidelines."
            else:
                raise RuntimeError(f"Generation failed: {str(e)}")
    
    def generate_stream(self, prompt: str, **kwargs):
        """
        Generate a streaming response from Gemini API
        
        Args:
            prompt: The input prompt for the model
            **kwargs: Additional generation parameters
            
        Yields:
            str: Chunks of generated text
        """
        try:
            generation_config = None
            if kwargs:
                generation_config = genai.types.GenerationConfig(**kwargs)
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                stream=True
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            yield f"Error in streaming: {str(e)}"
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if the API connection is working
        
        Returns:
            dict: Status information about the connection
        """
        try:
            test_response = self.generate("Hello")
            return {
                "status": "healthy",
                "model": self.model_name,
                "test_response": test_response[:50] + "..." if len(test_response) > 50 else test_response
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "model": self.model_name,
                "error": str(e)
            }