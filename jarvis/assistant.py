"""
JARVIS Assistant - Main Controller
Coordinates all components to create the AI assistant
"""
from typing import Optional, Dict, Any, Generator
from jarvis.gemini_engine import GeminiEngine
from jarvis.prompt_controller import PromptController
from jarvis.memory import Memory


class JarvisAssistant:
    """Main JARVIS assistant that coordinates all components"""
    
    def __init__(self, engine: GeminiEngine, prompt_controller: PromptController, 
                 memory: Memory):
        """
        Initialize JARVIS assistant
        
        Args:
            engine: Gemini API engine for generating responses
            prompt_controller: Controller for managing prompts and personalities
            memory: Memory manager for conversation history
        """
        self.engine = engine
        self.prompt_controller = prompt_controller
        self.memory = memory
        self._conversation_started = False
    
    def start_conversation(self) -> str:
        """
        Start a new conversation with a greeting
        
        Returns:
            Greeting message
        """
        greeting = self.prompt_controller.build_greeting()
        self._conversation_started = True
        # Don't store greeting in memory as it's system-generated
        return greeting
    
    def respond(self, user_input: str, save_to_memory: bool = True) -> str:
        """
        Generate a response to user input
        
        Args:
            user_input: The user's message
            save_to_memory: Whether to save this exchange to memory
            
        Returns:
            Assistant's response
        """
        if not user_input or not user_input.strip():
            return "I didn't receive any input. Please tell me how I can help you."
        
        try:
            # Build the complete prompt with context
            prompt = self.prompt_controller.build_prompt(
                user_input=user_input,
                memory=self.memory,
                include_context=True
            )
            
            # Generate response using Gemini
            response = self.engine.generate(prompt)
            
            # Save to memory if requested
            if save_to_memory:
                self.memory.add("user", user_input)
                self.memory.add("assistant", response)
            
            return response
            
        except RuntimeError as e:
            error_response = self.prompt_controller.format_error_response(str(e))
            return error_response
        except Exception as e:
            error_response = self.prompt_controller.format_error_response(
                f"Unexpected error: {str(e)}"
            )
            return error_response
    
    def respond_stream(self, user_input: str, save_to_memory: bool = True) -> Generator[str, None, None]:
        """
        Generate a streaming response to user input
        
        Args:
            user_input: The user's message
            save_to_memory: Whether to save this exchange to memory
            
        Yields:
            Chunks of the assistant's response
        """
        if not user_input or not user_input.strip():
            yield "I didn't receive any input. Please tell me how I can help you."
            return
        
        try:
            # Build the complete prompt with context
            prompt = self.prompt_controller.build_prompt(
                user_input=user_input,
                memory=self.memory,
                include_context=True
            )
            
            # Collect full response for memory
            full_response = []
            
            # Generate streaming response
            for chunk in self.engine.generate_stream(prompt):
                full_response.append(chunk)
                yield chunk
            
            # Save to memory if requested
            if save_to_memory:
                self.memory.add("user", user_input)
                self.memory.add("assistant", "".join(full_response))
                
        except Exception as e:
            error_response = self.prompt_controller.format_error_response(str(e))
            yield error_response
    
    def change_role(self, role: str) -> str:
        """
        Change the assistant's role/personality
        
        Args:
            role: New role to set
            
        Returns:
            Confirmation message
        """
        try:
            self.prompt_controller.set_role(role)
            role_info = self.prompt_controller.get_role_info()
            return f"Role changed to: {role_info['name']} - {role_info['description']}"
        except ValueError as e:
            return f"Error changing role: {str(e)}"
    
    def get_current_role(self) -> Dict[str, str]:
        """
        Get information about current role
        
        Returns:
            Dictionary with role information
        """
        return self.prompt_controller.get_role_info()
    
    def clear_memory(self) -> str:
        """
        Clear conversation history
        
        Returns:
            Confirmation message
        """
        self.memory.clear()
        return "Conversation history cleared. Starting fresh!"
    
    def get_conversation_stats(self) -> Dict[str, int]:
        """
        Get statistics about the conversation
        
        Returns:
            Dictionary with conversation statistics
        """
        return self.memory.get_statistics()
    
    def export_conversation(self, filename: Optional[str] = None) -> str:
        """
        Export conversation to a file
        
        Args:
            filename: Output filename
            
        Returns:
            Path to exported file or error message
        """
        try:
            filepath = self.memory.export_conversation(filename)
            return f"Conversation exported to: {filepath}"
        except Exception as e:
            return f"Failed to export conversation: {str(e)}"
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on all components
        
        Returns:
            Dictionary with health status
        """
        engine_health = self.engine.health_check()
        memory_stats = self.memory.get_statistics()
        role_info = self.prompt_controller.get_role_info()
        
        return {
            "engine": engine_health,
            "memory": memory_stats,
            "current_role": role_info,
            "conversation_started": self._conversation_started
        }
    
    @staticmethod
    def get_available_roles() -> Dict[str, str]:
        """
        Get all available assistant roles
        
        Returns:
            Dictionary of role names and descriptions
        """
        return PromptController.get_available_roles()