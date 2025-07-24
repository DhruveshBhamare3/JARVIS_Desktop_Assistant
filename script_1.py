# Create config.py - Configuration management
config_content = '''"""
Configuration file for JARVIS Desktop Assistant
Store all settings, API keys, and configurations here
"""
import os
from pathlib import Path

class Config:
    # Application Settings
    APP_NAME = "JARVIS Desktop Assistant"
    VERSION = "2.0.0"
    
    # Paths
    BASE_DIR = Path(__file__).parent
    MODELS_DIR = BASE_DIR / "models"
    LOGS_DIR = BASE_DIR / "logs"
    DATA_DIR = BASE_DIR / "data"
    
    # Create directories if they don't exist
    for directory in [MODELS_DIR, LOGS_DIR, DATA_DIR]:
        directory.mkdir(exist_ok=True)
    
    # Voice Settings
    WAKE_WORD = "Hey Jarvis"
    VOICE_RATE = 180  # Words per minute
    VOICE_VOLUME = 0.8  # 0.0 to 1.0
    VOICE_GENDER = "male"  # "male" or "female"
    
    # Speech Recognition Settings
    RECOGNITION_TIMEOUT = 5  # seconds
    RECOGNITION_PHRASE_TIMEOUT = 1  # seconds
    ENERGY_THRESHOLD = 4000
    
    # OpenAI Settings (User needs to add their API key)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
    OPENAI_MODEL = "gpt-4"
    MAX_TOKENS = 150
    
    # Wake Word Detection
    ENABLE_WAKE_WORD = True
    PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY", "your-porcupine-key-here")
    
    # GUI Settings
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    THEME = "dark"
    
    # Automation Settings
    PYAUTOGUI_PAUSE = 0.5
    PYAUTOGUI_FAILSAFE = True
    
    # Weather API (Optional)
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "your-weather-api-key")
    
    # Supported Commands
    COMMANDS = {
        "greeting": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
        "time": ["time", "what time is it", "current time"],
        "date": ["date", "today's date", "what date is it"],
        "weather": ["weather", "temperature", "forecast"],
        "open_app": ["open", "launch", "start", "run"],
        "close_app": ["close", "quit", "exit", "terminate"],
        "search": ["search", "google", "find", "look up"],
        "music": ["play music", "music", "song", "play"],
        "news": ["news", "headlines", "latest news"],
        "shutdown": ["shutdown", "turn off", "sleep", "hibernate"],
        "restart": ["restart", "reboot"],
        "volume": ["volume up", "volume down", "mute", "unmute"],
        "screenshot": ["screenshot", "capture screen", "take screenshot"],
        "reminder": ["remind me", "set reminder", "reminder"],
        "note": ["take note", "write note", "note"],
        "calculate": ["calculate", "math", "compute"],
        "joke": ["joke", "tell me a joke", "funny"],
        "goodbye": ["goodbye", "bye", "see you later", "farewell"]
    }
    
    # Application Shortcuts
    APPLICATIONS = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
        "edge": "msedge.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "vscode": "code.exe",
        "spotify": "spotify.exe",
        "discord": "discord.exe",
        "zoom": "zoom.exe",
        "teams": "teams.exe"
    }
    
    # Default Responses
    RESPONSES = {
        "greeting": [
            "Hello! How can I assist you today?",
            "Hi there! What can I do for you?",
            "Greetings! I'm here to help.",
            "Hello! Ready to assist you."
        ],
        "goodbye": [
            "Goodbye! Have a great day!",
            "See you later! Take care!",
            "Farewell! Until next time!",
            "Bye! It was great helping you!"
        ],
        "error": [
            "I'm sorry, I didn't understand that. Could you please repeat?",
            "I couldn't process that request. Please try again.",
            "Sorry, something went wrong. Please rephrase your request.",
            "I didn't catch that. Could you say it again?"
        ],
        "success": [
            "Task completed successfully!",
            "Done! Is there anything else I can help with?",
            "Completed! What's next?",
            "All set! How else can I assist you?"
        ]
    }

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
'''

with open("config.py", "w") as f:
    f.write(config_content)

print("Created config.py")