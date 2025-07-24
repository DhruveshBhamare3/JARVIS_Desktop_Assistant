# Create the main application structure and save multiple files
import os

# Create the main directory
os.makedirs("JARVIS_Desktop_Assistant", exist_ok=True)
os.chdir("JARVIS_Desktop_Assistant")

# Create requirements.txt file
requirements_content = """
speechrecognition==3.10.4
pyttsx3==2.90
pyautogui==0.9.54
openai==1.12.0
requests==2.31.0
pyaudio==0.2.14
pillow==10.2.0
pygame==2.5.2
wikipedia==1.4.0
beautifulsoup4==4.12.3
python-dotenv==1.0.1
tkinter-tooltip==2.1.0
pvporcupine==3.0.2
openwakeword==0.6.0
threading-timer==1.0.0
"""

with open("requirements.txt", "w") as f:
    f.write(requirements_content.strip())

print("Created requirements.txt")