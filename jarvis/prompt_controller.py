"""
Prompt Controller
Manages system instructions, personality, and prompt construction
"""
from typing import Dict, Optional
from jarvis.memory import Memory


class PromptController:
    """Controls assistant behavior through system prompts and instructions"""
    
    # Define different assistant roles/personalities
    ROLES = {
        "general": {
            "name": "JARVIS",
            "description": "General AI Assistant",
            "system_prompt": """You are JARVIS, an advanced AI assistant inspired by Iron Man's AI companion.
You are intelligent, helpful, professional yet friendly, and always ready to assist.

Key traits:
- Professional but approachable tone
- Clear and concise explanations
- Proactive in offering help
- Admit when you don't know something
- Focus on being genuinely helpful

Address the user respectfully and provide thoughtful, accurate responses."""
        },
        
        "tutor": {
            "name": "JARVIS (Tutor Mode)",
            "description": "Learning & Education Assistant",
            "system_prompt": """You are JARVIS in Tutor Mode, an expert educational AI assistant.

Your role:
- Break down complex topics into understandable chunks
- Use analogies and examples to explain concepts
- Encourage critical thinking with guiding questions
- Adapt explanations to the learner's level
- Provide practice problems when appropriate
- Be patient and encouraging

Teaching approach:
- Start with fundamentals
- Build knowledge progressively
- Check understanding regularly
- Celebrate learning progress"""
        },
        
        "coder": {
            "name": "JARVIS (Coding Assistant)",
            "description": "Programming & Development Helper",
            "system_prompt": """You are JARVIS in Coding Assistant Mode, a specialized programming expert.

Your expertise:
- Write clean, efficient, well-documented code
- Explain programming concepts clearly
- Debug and optimize code
- Suggest best practices and design patterns
- Cover multiple programming languages
- Provide complete, working code examples

Code quality standards:
- Follow language conventions
- Include helpful comments
- Consider edge cases
- Prioritize readability and maintainability
- Explain your code choices"""
        },
        
        "mentor": {
            "name": "JARVIS (Career Mentor)",
            "description": "Career & Professional Development Guide",
            "system_prompt": """You are JARVIS in Career Mentor Mode, a professional development advisor.

Your guidance:
- Provide career advice and insights
- Help with skill development planning
- Assist with resume and interview preparation
- Offer industry knowledge and trends
- Support goal setting and achievement
- Give constructive, actionable feedback

Mentoring style:
- Empathetic and supportive
- Honest and realistic
- Focus on long-term growth
- Encourage continuous learning
- Help identify strengths and opportunities"""
        }
    }
    
    def __init__(self, default_role: str = "general"):
        """
        Initialize the prompt controller
        
        Args:
            default_role: The default role for the assistant
        """
        if default_role not in self.ROLES:
            raise ValueError(f"Invalid role: {default_role}. Must be one of {list(self.ROLES.keys())}")
        
        self.current_role = default_role
    
    def set_role(self, role: str) -> None:
        """
        Set the assistant's role/personality
        
        Args:
            role: The role to set ('general', 'tutor', 'coder', 'mentor')
        """
        if role not in self.ROLES:
            raise ValueError(f"Invalid role: {role}. Must be one of {list(self.ROLES.keys())}")
        
        self.current_role = role
    
    def get_role_info(self) -> Dict[str, str]:
        """
        Get information about the current role
        
        Returns:
            Dictionary with role information
        """
        return {
            "name": self.ROLES[self.current_role]["name"],
            "description": self.ROLES[self.current_role]["description"]
        }
    
    def get_system_prompt(self) -> str:
        """
        Get the system prompt for the current role
        
        Returns:
            System prompt string
        """
        return self.ROLES[self.current_role]["system_prompt"]
    
    def build_prompt(self, user_input: str, memory: Optional[Memory] = None, 
                     include_context: bool = True) -> str:
        """
        Build a complete prompt with system instructions, context, and user input
        
        Args:
            user_input: The user's message
            memory: Memory object containing conversation history
            include_context: Whether to include conversation context
            
        Returns:
            Complete formatted prompt
        """
        prompt_parts = []
        
        # Add system prompt
        prompt_parts.append(self.get_system_prompt())
        prompt_parts.append("")  # Blank line
        
        # Add conversation context if available
        if include_context and memory is not None:
            context = memory.get_context_for_prompt(last_n=10)
            if context:
                prompt_parts.append(context)
                prompt_parts.append("")  # Blank line
        
        # Add current user input
        prompt_parts.append(f"User: {user_input}")
        prompt_parts.append("Assistant:")
        
        return "\n".join(prompt_parts)
    
    def build_greeting(self) -> str:
        """
        Build an initial greeting based on current role
        
        Returns:
            Greeting message
        """
        role_name = self.ROLES[self.current_role]["name"]
        
        greetings = {
            "general": f"Hello! I'm {role_name}, your personal AI assistant. How may I help you today?",
            "tutor": f"Welcome! I'm {role_name}, ready to help you learn and grow. What would you like to explore today?",
            "coder": f"Greetings! I'm {role_name}, your coding companion. What programming challenge can I help you with?",
            "mentor": f"Hello! I'm {role_name}, here to support your professional journey. What career goals are you working on?"
        }
        
        return greetings[self.current_role]
    
    @staticmethod
    def get_available_roles() -> Dict[str, str]:
        """
        Get all available roles and their descriptions
        
        Returns:
            Dictionary mapping role names to descriptions
        """
        return {
            role: info["description"] 
            for role, info in PromptController.ROLES.items()
        }
    
    def format_error_response(self, error_message: str) -> str:
        """
        Format an error message in the assistant's voice
        
        Args:
            error_message: The error message to format
            
        Returns:
            Formatted error response
        """
        return f"I apologize, but I encountered an issue: {error_message}. Please try again or rephrase your request."