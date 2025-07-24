# Create command_processor.py - Command processing and execution
command_processor_content = '''"""
Command Processing Module for JARVIS Desktop Assistant
Handles command interpretation, AI integration, and task execution
"""
import os
import sys
import subprocess
import webbrowser
import pyautogui
import datetime
import random
import requests
import json
import logging
from pathlib import Path
import wikipedia
from config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure PyAutoGUI
pyautogui.PAUSE = Config.PYAUTOGUI_PAUSE
pyautogui.FAILSAFE = Config.PYAUTOGUI_FAILSAFE

class CommandProcessor:
    def __init__(self, voice_processor=None):
        self.voice_processor = voice_processor
        self.openai_client = None
        self.conversation_history = []
        
        # Initialize OpenAI client if API key is provided
        self._initialize_openai()
    
    def _initialize_openai(self):
        """Initialize OpenAI client for AI responses"""
        if Config.OPENAI_API_KEY and Config.OPENAI_API_KEY != "your-openai-api-key-here":
            try:
                import openai
                self.openai_client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
                logger.info("OpenAI client initialized")
            except ImportError:
                logger.warning("OpenAI library not available")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
        else:
            logger.warning("OpenAI API key not configured")
    
    def process_command(self, command_text):
        """Process and execute voice command"""
        if not command_text:
            return False
        
        command_text = command_text.lower().strip()
        logger.info(f"Processing command: {command_text}")
        
        try:
            # Check for specific command patterns
            if self._handle_greeting(command_text):
                return True
            elif self._handle_time_date(command_text):
                return True
            elif self._handle_weather(command_text):
                return True
            elif self._handle_open_app(command_text):
                return True
            elif self._handle_close_app(command_text):
                return True
            elif self._handle_search(command_text):
                return True
            elif self._handle_system_control(command_text):
                return True
            elif self._handle_automation(command_text):
                return True
            elif self._handle_media_control(command_text):
                return True
            elif self._handle_screenshot(command_text):
                return True
            elif self._handle_calculate(command_text):
                return True
            elif self._handle_joke(command_text):
                return True
            elif self._handle_goodbye(command_text):
                return True
            else:
                # If no specific handler matches, try AI response
                return self._handle_ai_response(command_text)
                
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            self._speak("Sorry, I encountered an error while processing that command.")
            return False
    
    def _speak(self, text):
        """Speak text using voice processor"""
        if self.voice_processor:
            self.voice_processor.speak(text)
        else:
            print(f"JARVIS: {text}")
    
    def _handle_greeting(self, command):
        """Handle greeting commands"""
        if any(word in command for word in Config.COMMANDS["greeting"]):
            response = random.choice(Config.RESPONSES["greeting"])
            self._speak(response)
            return True
        return False
    
    def _handle_time_date(self, command):
        """Handle time and date requests"""
        if any(word in command for word in Config.COMMANDS["time"]):
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self._speak(f"The current time is {current_time}")
            return True
        elif any(word in command for word in Config.COMMANDS["date"]):
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            self._speak(f"Today is {current_date}")
            return True
        return False
    
    def _handle_weather(self, command):
        """Handle weather requests"""
        if any(word in command for word in Config.COMMANDS["weather"]):
            weather_info = self._get_weather()
            self._speak(weather_info)
            return True
        return False
    
    def _get_weather(self):
        """Get weather information"""
        try:
            # This is a simplified weather implementation
            # You can integrate with weather APIs like OpenWeatherMap
            if Config.WEATHER_API_KEY and Config.WEATHER_API_KEY != "your-weather-api-key":
                # Implement actual weather API call here
                return "Weather information is currently unavailable. Please configure your weather API key."
            else:
                return "Weather service is not configured. Please add your weather API key in the config."
        except Exception as e:
            logger.error(f"Weather error: {e}")
            return "Sorry, I couldn't fetch the weather information right now."
    
    def _handle_open_app(self, command):
        """Handle application opening commands"""
        if "open" in command or "launch" in command or "start" in command:
            # Extract application name from command
            for app_name, app_executable in Config.APPLICATIONS.items():
                if app_name in command:
                    try:
                        if sys.platform == "win32":
                            subprocess.Popen(app_executable, shell=True)
                        elif sys.platform == "darwin":  # macOS
                            subprocess.Popen(["open", "-a", app_executable])
                        else:  # Linux
                            subprocess.Popen(app_executable, shell=True)
                        
                        self._speak(f"Opening {app_name}")
                        return True
                    except Exception as e:
                        logger.error(f"Failed to open {app_name}: {e}")
                        self._speak(f"Sorry, I couldn't open {app_name}")
                        return False
            
            # Handle websites
            if "youtube" in command:
                webbrowser.open("https://www.youtube.com")
                self._speak("Opening YouTube")
                return True
            elif "google" in command:
                webbrowser.open("https://www.google.com")
                self._speak("Opening Google")
                return True
            elif "gmail" in command:
                webbrowser.open("https://gmail.com")
                self._speak("Opening Gmail")
                return True
        
        return False
    
    def _handle_close_app(self, command):
        """Handle application closing commands"""
        if any(word in command for word in ["close", "quit", "exit"]):
            # This is a basic implementation - you can enhance it
            # to close specific applications
            try:
                if sys.platform == "win32":
                    pyautogui.hotkey('alt', 'f4')
                else:
                    pyautogui.hotkey('cmd', 'q')  # macOS
                
                self._speak("Closing the current application")
                return True
            except Exception as e:
                logger.error(f"Failed to close application: {e}")
                self._speak("Sorry, I couldn't close the application")
        
        return False
    
    def _handle_search(self, command):
        """Handle search commands"""
        if "search" in command or "google" in command or "find" in command:
            # Extract search query
            search_terms = ["search for", "google", "find", "look up"]
            query = command
            for term in search_terms:
                if term in command:
                    query = command.split(term, 1)[-1].strip()
                    break
            
            if query and query != command:
                # Search on Google
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(search_url)
                self._speak(f"Searching for {query}")
                return True
            else:
                self._speak("What would you like me to search for?")
                return True
        
        return False
    
    def _handle_system_control(self, command):
        """Handle system control commands"""
        if "shutdown" in command:
            self._speak("Shutting down the system in 10 seconds. Say cancel to abort.")
            # Implement shutdown logic here
            return True
        elif "restart" in command or "reboot" in command:
            self._speak("Restarting the system in 10 seconds. Say cancel to abort.")
            # Implement restart logic here
            return True
        elif "sleep" in command or "hibernate" in command:
            self._speak("Putting the system to sleep")
            # Implement sleep logic here
            return True
        
        return False
    
    def _handle_automation(self, command):
        """Handle automation commands"""
        if "volume up" in command:
            pyautogui.press('volumeup')
            self._speak("Volume increased")
            return True
        elif "volume down" in command:
            pyautogui.press('volumedown')
            self._speak("Volume decreased")
            return True
        elif "mute" in command:
            pyautogui.press('volumemute')
            self._speak("Audio muted")
            return True
        elif "minimize" in command:
            pyautogui.hotkey('win', 'down')
            self._speak("Window minimized")
            return True
        elif "maximize" in command:
            pyautogui.hotkey('win', 'up')
            self._speak("Window maximized")
            return True
        
        return False
    
    def _handle_media_control(self, command):
        """Handle media control commands"""
        if "play" in command or "pause" in command:
            pyautogui.press('playpause')
            self._speak("Media toggled")
            return True
        elif "next" in command:
            pyautogui.press('nexttrack')
            self._speak("Next track")
            return True
        elif "previous" in command:
            pyautogui.press('prevtrack')
            self._speak("Previous track")
            return True
        
        return False
    
    def _handle_screenshot(self, command):
        """Handle screenshot commands"""
        if "screenshot" in command or "capture screen" in command:
            try:
                screenshot = pyautogui.screenshot()
                screenshot_path = Config.DATA_DIR / f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                screenshot.save(screenshot_path)
                self._speak(f"Screenshot saved to {screenshot_path}")
                return True
            except Exception as e:
                logger.error(f"Screenshot error: {e}")
                self._speak("Sorry, I couldn't take a screenshot")
        
        return False
    
    def _handle_calculate(self, command):
        """Handle calculation commands"""
        if "calculate" in command or "math" in command or "compute" in command:
            # Extract mathematical expression
            # This is a basic implementation - you can enhance it
            try:
                # Remove command words
                calc_command = command.replace("calculate", "").replace("math", "").replace("compute", "").strip()
                
                # Basic math operations
                if "plus" in calc_command or "add" in calc_command:
                    calc_command = calc_command.replace("plus", "+").replace("add", "+")
                elif "minus" in calc_command or "subtract" in calc_command:
                    calc_command = calc_command.replace("minus", "-").replace("subtract", "-")
                elif "times" in calc_command or "multiply" in calc_command:
                    calc_command = calc_command.replace("times", "*").replace("multiply", "*")
                elif "divided by" in calc_command or "divide" in calc_command:
                    calc_command = calc_command.replace("divided by", "/").replace("divide", "/")
                
                # Simple evaluation (be careful with security in production)
                # This is a basic implementation
                result = eval(calc_command)
                self._speak(f"The result is {result}")
                return True
                
            except Exception as e:
                logger.error(f"Calculation error: {e}")
                self._speak("Sorry, I couldn't perform that calculation")
        
        return False
    
    def _handle_joke(self, command):
        """Handle joke requests"""
        if any(word in command for word in Config.COMMANDS["joke"]):
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "Why don't eggs tell jokes? They'd crack each other up!",
                "What do you call a fake noodle? An impasta!",
                "Why did the coffee file a police report? It got mugged!"
            ]
            joke = random.choice(jokes)
            self._speak(joke)
            return True
        return False
    
    def _handle_goodbye(self, command):
        """Handle goodbye commands"""
        if any(word in command for word in Config.COMMANDS["goodbye"]):
            response = random.choice(Config.RESPONSES["goodbye"])
            self._speak(response)
            return True
        return False
    
    def _handle_ai_response(self, command):
        """Handle general AI responses using OpenAI"""
        if not self.openai_client:
            self._speak("AI responses are not available. Please configure your OpenAI API key.")
            return False
        
        try:
            # Add command to conversation history
            self.conversation_history.append({"role": "user", "content": command})
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-8:]
            
            # Create system message
            system_message = {
                "role": "system",
                "content": "You are JARVIS, a helpful desktop AI assistant. Provide concise, helpful responses. Keep responses under 100 words."
            }
            
            # Get AI response
            response = self.openai_client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[system_message] + self.conversation_history,
                max_tokens=Config.MAX_TOKENS,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Add AI response to conversation history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            self._speak(ai_response)
            return True
            
        except Exception as e:
            logger.error(f"AI response error: {e}")
            self._speak("Sorry, I couldn't process that request right now.")
            return False
    
    def get_help(self):
        """Provide help information"""
        help_text = """
        I can help you with the following commands:
        - Time and date queries
        - Opening applications and websites
        - System controls like volume and screenshots
        - Web searches
        - Simple calculations
        - Weather information
        - Media controls
        - General questions using AI
        
        Just speak naturally and I'll try to help!
        """
        return help_text

# Example usage
if __name__ == "__main__":
    processor = CommandProcessor()
    
    # Test some commands
    test_commands = [
        "hello",
        "what time is it",
        "open notepad",
        "search for python programming",
        "tell me a joke"
    ]
    
    for command in test_commands:
        print(f"\\nTesting: {command}")
        processor.process_command(command)
'''

with open("command_processor.py", "w") as f:
    f.write(command_processor_content)

print("Created command_processor.py")