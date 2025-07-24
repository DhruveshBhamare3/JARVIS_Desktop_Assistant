# Create main.py - Entry point
main_content = '''"""
Main entry point for JARVIS Desktop Assistant
"""
import sys
import logging
from voice_processor import VoiceProcessor
from command_processor import CommandProcessor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("JARVIS")

def main():
    # Initialize voice processor
    voice_proc = VoiceProcessor()
    
    # Initialize command processor
    cmd_proc = CommandProcessor(voice_processor=voice_proc)
    
    # Provide greeting
    voice_proc.speak("Hello! I am JARVIS, your desktop assistant. How can I help you today?")
    
    # Start continuous listening
    def callback(command_text):
        cmd_proc.process_command(command_text)
    
    voice_proc.start_continuous_listening(callback)
    
    # Keep the main thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Shutting down JARVIS...")
        voice_proc.cleanup()
        sys.exit(0)

if __name__ == "__main__":
    main()
'''

with open("main.py", "w") as f:
    f.write(main_content)

print("Created main.py")