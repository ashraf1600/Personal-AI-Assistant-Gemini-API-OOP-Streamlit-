# 🧠 JARVIS - Personal AI Assistant

A sophisticated AI assistant built with Python, Streamlit, and Google's Gemini API, following Object-Oriented Programming principles.

## ✨ Features

* **Multiple AI Personalities** : Switch between General Assistant, Tutor, Coding Assistant, and Career Mentor modes
* **Conversation Memory** : Persistent chat history stored in JSON format
* **Clean Architecture** : Built with OOP principles (Encapsulation, Inheritance, Modularity)
* **Modern UI** : Sleek JARVIS-themed Streamlit interface
* **Error Handling** : Graceful fallbacks and user-friendly error messages
* **Export Functionality** : Save conversations to text files
* **Conversation Statistics** : Track your interaction history

## 🛠️ Tech Stack

* **Python 3.10+**
* **Streamlit** - Web UI framework
* **Google Gemini API** - AI intelligence engine
* **python-dotenv** - Environment variable management

## 📁 Project Structure

```
jarvis_assistant/
│
├── app.py                          # Streamlit UI application
│
├── jarvis/
│   ├── __init__.py                 # Package initializer
│   ├── assistant.py                # Main JARVIS controller
│   ├── gemini_engine.py            # Gemini API handler
│   ├── prompt_controller.py        # System prompts & personalities
│   └── memory.py                   # Conversation memory management
│
├── config/
│   ├── __init__.py                 # Config package initializer
│   └── settings.py                 # Environment & configuration
│
├── .env                            # API keys (DO NOT COMMIT)
├── .env.example                    # Environment template
├── requirements.txt                # Python dependencies
├── conversation_history.json       # Stored conversations (auto-generated)
└── README.md                       # This file
```

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd jarvis_assistant
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
# Get your API key from: https://makersuite.google.com/app/apikey
```

Your `.env` file should look like:

```
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-pro
MAX_TOKENS=1000
TEMPERATURE=0.7
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 🎯 Usage Guide

### Choosing Assistant Modes

JARVIS offers four specialized modes:

1. **General Assistant** - For everyday tasks and general questions
2. **Tutor Mode** - Specialized for learning and education
3. **Coding Assistant** - Expert help with programming
4. **Career Mentor** - Professional development guidance

Switch modes using the sidebar control panel.

### Chat Interface

* Type your message in the chat input at the bottom
* JARVIS responds based on the current mode
* Conversation history is automatically saved
* Use sidebar actions to clear history or export conversations

### Exporting Conversations

Click "📥 Export Chat" in the sidebar to save your conversation to a text file with timestamps.

## 🏗️ Architecture & OOP Concepts

### Class Design

#### 1. **Settings** (`config/settings.py`)

* **Responsibility** : Environment variable management
* **Encapsulation** : Protects API keys and configuration
* **Methods** : `load_api_key()`, `validate()`

#### 2. **GeminiEngine** (`jarvis/gemini_engine.py`)

* **Responsibility** : Gemini API communication
* **Encapsulation** : Hides API implementation details
* **Methods** : `generate()`, `generate_stream()`, `health_check()`
* **Error Handling** : Comprehensive exception management

#### 3. **Memory** (`jarvis/memory.py`)

* **Responsibility** : Conversation history management
* **Persistence** : JSON file storage
* **Methods** : `add()`, `get_history()`, `clear()`, `export_conversation()`

#### 4. **PromptController** (`jarvis/prompt_controller.py`)

* **Responsibility** : System prompts and personality management
* **Modularity** : Easily add new assistant roles
* **Methods** : `build_prompt()`, `set_role()`, `build_greeting()`

#### 5. **JarvisAssistant** (`jarvis/assistant.py`)

* **Responsibility** : Orchestrates all components
* **Composition** : Uses Engine, PromptController, and Memory
* **Methods** : `respond()`, `change_role()`, `clear_memory()`

### Design Patterns Used

* **Facade Pattern** : JarvisAssistant provides simple interface to complex subsystems
* **Strategy Pattern** : PromptController switches between different assistant strategies
* **Singleton-like** : Settings class manages single configuration source
* **Separation of Concerns** : Each class has a single, well-defined responsibility

## 🔒 Security Best Practices

✅ API keys stored in `.env` file

✅ `.env` file in `.gitignore`

✅ No hardcoded credentials

✅ Environment validation on startup

✅ Graceful error handling without exposing internals

## 🎨 Customization

### Adding New Assistant Roles

Edit `jarvis/prompt_controller.py` and add to the `ROLES` dictionary:

```python
"custom_role": {
    "name": "JARVIS (Custom Mode)",
    "description": "Your custom description",
    "system_prompt": """Your custom system prompt here"""
}
```

### Modifying UI Theme

Edit the CSS in `app.py` under the `st.markdown()` section with custom styles.

### Adjusting Memory Limits

In `app.py`, modify the Memory initialization:

```python
memory = Memory(memory_file="conversation_history.json", max_history=100)
```

## 🐛 Troubleshooting

### "GEMINI_API_KEY not found"

* Ensure `.env` file exists in project root
* Check that `GEMINI_API_KEY` is set correctly
* Verify no extra spaces or quotes in the key

### "Failed to configure Gemini API"

* Verify your API key is valid
* Check internet connection
* Ensure API quota is not exceeded

### "Import errors"

* Ensure all dependencies are installed: `pip install -r requirements.txt`
* Verify you're in the correct virtual environment

## 📚 Learning Resources

* [Gemini API Documentation](https://ai.google.dev/docs)
* [Streamlit Documentation](https://docs.streamlit.io/)
* [Python OOP Tutorial](https://docs.python.org/3/tutorial/classes.html)

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

* Voice input/output
* Streaming responses
* Additional assistant roles
* Enhanced memory features
* Multi-language support

## 📝 License

This project is for educational purposes. Ensure compliance with Gemini API terms of service.

## 👨‍💻 Author

Built as a learning project demonstrating:

* Object-Oriented Programming
* API Integration
* Modern Python Development
* UI/UX Design with Streamlit

---

 **Note** : Remember to never commit your `.env` file or expose your API keys!
