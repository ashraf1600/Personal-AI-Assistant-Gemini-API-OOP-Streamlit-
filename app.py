"""
JARVIS - Personal AI Assistant
Streamlit UI Application
"""
import streamlit as st
from config.settings import Settings
from jarvis.gemini_engine import GeminiEngine
from jarvis.prompt_controller import PromptController
from jarvis.memory import Memory
from jarvis.assistant import JarvisAssistant


# Page configuration
st.set_page_config(
    page_title="Personal AI Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for JARVIS theme
# Professional JARVIS Theme
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400&display=swap');

    /* Global App Styling */
    .stApp {
        background-color: #0E1117;
        font-family: 'Inter', sans-serif;
    }
    
    /* Modern Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        background: #0E1117;
    }
    ::-webkit-scrollbar-thumb {
        background: #1f2937;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #00d4ff;
    }

    /* Headers */
    .main-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4ff 0%, #0080ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 2rem 0;
        letter-spacing: 2px;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 10px rgba(0, 212, 255, 0.2); }
        to { text-shadow: 0 0 20px rgba(0, 212, 255, 0.6); }
    }

    /* --- SIDEBAR STYLING --- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b0f19 0%, #11141d 100%);
        border-right: 1px solid rgba(0, 212, 255, 0.1);
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.5);
    }
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        font-family: 'Orbitron', sans-serif;
        color: #00d4ff !important;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.2);
        letter-spacing: 1px;
    }
    
    /* Custom Selectbox in Sidebar */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        color: #e0e0e0 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover {
        border-color: #00d4ff !important;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.1);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        color: #00d4ff !important;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.9rem !important;
    }

    /* Role Badge */
    .role-badge {
        background: rgba(0, 212, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.3);
        color: #00d4ff;
        padding: 0.8rem;
        border-radius: 8px;
        display: block;
        text-align: center;
        margin: 1rem 0;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 1px;
        font-size: 1rem;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.1);
        text-transform: uppercase;
    }

    /* Chat Messages - High Visibility */
    div[data-testid="stChatMessage"] {
        background: rgba(20, 25, 35, 0.9);
        border: 1px solid rgba(0, 212, 255, 0.15);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    div[data-testid="stChatMessage"] p {
        font-size: 1.1rem !important;
        line-height: 1.6 !important;
        color: #f0f0f0 !important;
        font-weight: 400;
        letter-spacing: 0.3px;
    }

    div[data-testid="stChatMessage"]:nth-child(even) {
        background: rgba(0, 50, 70, 0.4);
        border-left: 4px solid #00d4ff;
    }
    
    div[data-testid="stChatMessage"]:hover {
        border-color: rgba(0, 212, 255, 0.5);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.15);
        transform: translateY(-1px);
        transition: all 0.3s ease;
    }

    /* Metric Styling */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        color: #00d4ff !important;
        font-size: 2rem !important;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    [data-testid="stMetricLabel"] {
        color: #a0a0a0 !important;
        font-size: 0.9rem !important;
    }

    /* Input Field */
    .stChatInputContainer textarea {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-size: 1rem;
    }
    .stChatInputContainer textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3) !important;
    }
    
    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #0b1120 0%, #16213e 100%);
        border: 1px solid #00d4ff;
        color: #00d4ff;
        border-radius: 6px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8rem;
        letter-spacing: 1px;
    }
    div.stButton > button:hover {
        background: rgba(0, 212, 255, 0.1);
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.4);
        transform: scale(1.02);
    }
    
    /* Divider */
    hr {
        border-top: 1px solid rgba(0, 212, 255, 0.2) !important;
        margin: 2rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'assistant' not in st.session_state:
        try:
            # Load settings
            settings = Settings()
            api_key = settings.load_api_key()
            
            # Initialize components
            engine = GeminiEngine(api_key=api_key, model_name=settings.model_name)
            prompt_controller = PromptController(default_role="general")
            memory = Memory(memory_file="conversation_history.json", max_history=50)
            
            # Create assistant
            st.session_state.assistant = JarvisAssistant(
                engine=engine,
                prompt_controller=prompt_controller,
                memory=memory
            )
            
            st.session_state.initialized = True
            st.session_state.messages = []
            
        except Exception as e:
            st.error(f"Failed to initialize AI: {str(e)}")
            st.info("Please ensure your .env file is configured with a valid GEMINI_API_KEY")
            st.session_state.initialized = False


def display_sidebar():
    """Display sidebar with controls and information"""
    with st.sidebar:
        st.markdown('<h2 style="color: #00d4ff;">⚙️ JARVIS Control Panel</h2>', unsafe_allow_html=True)
        
        # Role selection
        st.subheader("🎭 Assistant Mode")
        available_roles = JarvisAssistant.get_available_roles()
        
        current_role_info = st.session_state.assistant.get_current_role()
        
        role_options = list(available_roles.keys())
        role_labels = [f"{role.title()}: {desc}" for role, desc in available_roles.items()]
        
        # Find current role index
        current_role_name = current_role_info['name'].split('(')[0].strip()
        current_index = 0
        for idx, role in enumerate(role_options):
            if role in current_role_info['name'].lower():
                current_index = idx
                break
        
        selected_role = st.selectbox(
            "Choose mode:",
            options=role_options,
            format_func=lambda x: f"{x.title()}: {available_roles[x]}",
            index=current_index,
            key="role_selector"
        )
        
        # Apply role change
        if st.button("🔄 Apply Mode Change", use_container_width=True):
            result = st.session_state.assistant.change_role(selected_role)
            st.success(result)
            st.rerun()
        
        st.divider()
        
        # Current role display
        st.subheader("📊 Current Status")
        role_info = st.session_state.assistant.get_current_role()
        st.markdown(f'<div class="role-badge">{role_info["name"]}</div>', unsafe_allow_html=True)
        st.caption(role_info["description"])
        
        st.divider()
        
        # Conversation statistics
        st.subheader("💬 Conversation Stats")
        stats = st.session_state.assistant.get_conversation_stats()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Messages", stats['total_messages'])
        with col2:
            st.metric("Your Messages", stats['user_messages'])
        
        st.divider()
        
        # Action buttons
        st.subheader("🛠️ Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.assistant.clear_memory()
                st.session_state.messages = []
                st.success("Memory cleared!")
                st.rerun()
        
        with col2:
            if st.button("📥 Export Chat", use_container_width=True):
                result = st.session_state.assistant.export_conversation()
                st.success(result)
        
        st.divider()
        
        # Help section
        with st.expander("ℹ️ Help & Tips"):
            st.markdown("""
            **How to use JARVIS:**
            
            1. **Choose a Mode**: Select the assistant mode that fits your needs
            2. **Ask Questions**: Type your questions or requests in the chat
            3. **Get Help**: JARVIS adapts to provide relevant assistance
            
            **Available Modes:**
            - **General**: For everyday tasks and questions
            - **Tutor**: For learning and education
            - **Coder**: For programming help
            - **Mentor**: For career guidance
            
            **Tips:**
            - Be specific in your questions
            - Use the export feature to save important conversations
            - Clear history to start fresh conversations
            """)


def display_chat_interface():
    """Display main chat interface"""
    # Header
    st.markdown('<div class="main-header">🧠 Personal AI Assistant</div>', unsafe_allow_html=True)
    
    role_info = st.session_state.assistant.get_current_role()
    st.markdown(f"<p style='text-align: center; color: #00d4ff;'>Current Mode: {role_info['name']}</p>", 
                unsafe_allow_html=True)
    
    st.divider()
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask JARVIS anything..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("JARVIS is thinking..."):
                response = st.session_state.assistant.respond(prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})


def main():
    """Main application entry point"""
    # Initialize session state
    initialize_session_state()
    
    # Check if initialization was successful
    if not st.session_state.get('initialized', False):
        st.warning("⚠️ Could not be initialized. Please check your configuration.")
        return
    
    # Display greeting on first run
    if not st.session_state.messages:
        greeting = st.session_state.assistant.start_conversation()
        st.session_state.messages.append({"role": "assistant", "content": greeting})
    
    # Display sidebar
    display_sidebar()
    
    # Display chat interface
    display_chat_interface()


if __name__ == "__main__":
    main()