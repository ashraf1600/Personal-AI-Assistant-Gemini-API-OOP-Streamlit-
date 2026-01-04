"""
Conversation Memory Management
Handles storing and retrieving conversation history
"""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime


class Memory:
    """Manages conversation history and persistence"""
    
    def __init__(self, memory_file: str = "conversation_history.json", max_history: int = 50):
        """
        Initialize memory management
        
        Args:
            memory_file: Path to the JSON file for storing conversations
            max_history: Maximum number of messages to keep in memory
        """
        self.memory_file = memory_file
        self.max_history = max_history
        self.conversation: List[Dict[str, str]] = []
        self._load_from_file()
    
    def _load_from_file(self) -> None:
        """Load conversation history from JSON file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversation = data.get('messages', [])
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load memory file: {e}")
                self.conversation = []
        else:
            self.conversation = []
    
    def _save_to_file(self) -> None:
        """Save conversation history to JSON file"""
        try:
            data = {
                'messages': self.conversation,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save memory file: {e}")
    
    def add(self, role: str, message: str) -> None:
        """
        Add a message to conversation history
        
        Args:
            role: The role of the message sender ('user' or 'assistant')
            message: The message content
        """
        if role not in ['user', 'assistant']:
            raise ValueError("Role must be either 'user' or 'assistant'")
        
        self.conversation.append({
            'role': role,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Trim history if it exceeds max_history
        if len(self.conversation) > self.max_history:
            self.conversation = self.conversation[-self.max_history:]
        
        self._save_to_file()
    
    def get_history(self, last_n: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Get conversation history
        
        Args:
            last_n: Number of recent messages to return (None for all)
            
        Returns:
            List of conversation messages
        """
        if last_n is None:
            return self.conversation.copy()
        return self.conversation[-last_n:] if last_n > 0 else []
    
    def get_formatted_history(self, last_n: Optional[int] = None) -> str:
        """
        Get formatted conversation history as a string
        
        Args:
            last_n: Number of recent messages to return
            
        Returns:
            Formatted conversation history
        """
        history = self.get_history(last_n)
        
        if not history:
            return "No conversation history."
        
        formatted = []
        for msg in history:
            role_name = "User" if msg['role'] == 'user' else "JARVIS"
            formatted.append(f"{role_name}: {msg['message']}")
        
        return "\n".join(formatted)
    
    def clear(self) -> None:
        """Clear all conversation history"""
        self.conversation = []
        self._save_to_file()
    
    def get_context_for_prompt(self, last_n: int = 10) -> str:
        """
        Get recent conversation context formatted for prompts
        
        Args:
            last_n: Number of recent exchanges to include
            
        Returns:
            Formatted context string
        """
        history = self.get_history(last_n)
        
        if not history:
            return ""
        
        context_parts = ["Previous conversation:"]
        for msg in history:
            role_prefix = "User" if msg['role'] == 'user' else "Assistant"
            context_parts.append(f"{role_prefix}: {msg['message']}")
        
        return "\n".join(context_parts)
    
    def export_conversation(self, filename: Optional[str] = None) -> str:
        """
        Export conversation to a file
        
        Args:
            filename: Output filename (default: conversation_export_TIMESTAMP.txt)
            
        Returns:
            Path to the exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_export_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("JARVIS Conversation Export\n")
                f.write("=" * 50 + "\n\n")
                
                for msg in self.conversation:
                    role_name = "User" if msg['role'] == 'user' else "JARVIS"
                    timestamp = msg.get('timestamp', 'N/A')
                    f.write(f"[{timestamp}] {role_name}:\n")
                    f.write(f"{msg['message']}\n\n")
                    f.write("-" * 50 + "\n\n")
            
            return filename
        except IOError as e:
            raise RuntimeError(f"Failed to export conversation: {e}")
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get statistics about the conversation
        
        Returns:
            Dictionary with conversation statistics
        """
        user_messages = sum(1 for msg in self.conversation if msg['role'] == 'user')
        assistant_messages = sum(1 for msg in self.conversation if msg['role'] == 'assistant')
        
        return {
            'total_messages': len(self.conversation),
            'user_messages': user_messages,
            'assistant_messages': assistant_messages
        }