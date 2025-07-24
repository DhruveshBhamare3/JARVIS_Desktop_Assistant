"""
Voice Processing Module for JARVIS Desktop Assistant
Handles speech recognition, text-to-speech, and wake word detection
"""
import speech_recognition as sr
import pyttsx3
import threading
import time
import logging
from config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = None
        self.is_listening = False
        self.wake_word_detected = False

        # Initialize TTS engine
        self._initialize_tts()

        # Configure speech recognition
        self._configure_recognition()

        # Initialize wake word detection (if enabled)
        self.wake_word_detector = None
        if Config.ENABLE_WAKE_WORD:
            self._initialize_wake_word()

    def _initialize_tts(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()

            # Set voice properties
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Select voice based on gender preference
                for voice in voices:
                    if Config.VOICE_GENDER.lower() in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                else:
                    # If preferred gender not found, use first available voice
                    self.tts_engine.setProperty('voice', voices[0].id)

            # Set speech rate and volume
            self.tts_engine.setProperty('rate', Config.VOICE_RATE)
            self.tts_engine.setProperty('volume', Config.VOICE_VOLUME)

            logger.info("TTS engine initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            self.tts_engine = None

    def _configure_recognition(self):
        """Configure speech recognition settings"""
        try:
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)

            # Set recognition parameters
            self.recognizer.energy_threshold = Config.ENERGY_THRESHOLD
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            self.recognizer.phrase_threshold = 0.3

            logger.info("Speech recognition configured successfully")

        except Exception as e:
            logger.error(f"Failed to configure speech recognition: {e}")

    def _initialize_wake_word(self):
        """Initialize wake word detection"""
        try:
            # Try to import and initialize Porcupine for wake word detection
            import pvporcupine

            self.wake_word_detector = pvporcupine.create(
                access_key=Config.PORCUPINE_ACCESS_KEY,
                keywords=['jarvis']  # Built-in keyword
            )
            logger.info("Wake word detection initialized")

        except ImportError:
            logger.warning("Porcupine not available. Wake word detection disabled.")
            Config.ENABLE_WAKE_WORD = False
        except Exception as e:
            logger.error(f"Failed to initialize wake word detection: {e}")
            Config.ENABLE_WAKE_WORD = False

    def speak(self, text, interrupt=False):
        """Convert text to speech"""
        if not self.tts_engine:
            logger.error("TTS engine not available")
            return

        try:
            if interrupt:
                self.tts_engine.stop()

            logger.info(f"Speaking: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()

        except Exception as e:
            logger.error(f"TTS error: {e}")

    def listen(self, timeout=None, phrase_timeout=None):
        """Listen for voice input and convert to text"""
        if timeout is None:
            timeout = Config.RECOGNITION_TIMEOUT
        if phrase_timeout is None:
            phrase_timeout = Config.RECOGNITION_PHRASE_TIMEOUT

        try:
            with self.microphone as source:
                logger.info("Listening...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_timeout
                )

            logger.info("Processing speech...")
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized: {text}")
            return text.lower()

        except sr.WaitTimeoutError:
            logger.warning("Listening timeout")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during listening: {e}")
            return None

    def start_continuous_listening(self, callback):
        """Start continuous listening for voice commands"""
        self.is_listening = True

        def listen_continuously():
            while self.is_listening:
                try:
                    # If wake word detection is enabled, wait for wake word first
                    if Config.ENABLE_WAKE_WORD and not self.wake_word_detected:
                        if self._wait_for_wake_word():
                            self.wake_word_detected = True
                            self.speak("Yes, I'm listening")
                        continue

                    # Listen for command
                    command = self.listen(timeout=10)
                    if command:
                        self.wake_word_detected = False  # Reset wake word flag
                        callback(command)

                    time.sleep(0.1)  # Small delay to prevent excessive CPU usage

                except Exception as e:
                    logger.error(f"Error in continuous listening: {e}")
                    time.sleep(1)

        # Start listening in a separate thread
        self.listen_thread = threading.Thread(target=listen_continuously, daemon=True)
        self.listen_thread.start()
        logger.info("Started continuous listening")

    def stop_continuous_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        logger.info("Stopped continuous listening")

    def _wait_for_wake_word(self):
        """Wait for wake word detection"""
        if not self.wake_word_detector:
            # Fallback: simple keyword detection in speech
            try:
                command = self.listen(timeout=1)
                if command and any(word in command for word in ['jarvis', 'hey jarvis']):
                    return True
            except:
                pass
            return False

        try:
            # Use Porcupine for wake word detection
            # This is a simplified implementation
            # In practice, you'd process audio frames continuously
            audio = self._get_audio_frame()
            if audio:
                keyword_index = self.wake_word_detector.process(audio)
                return keyword_index >= 0
        except Exception as e:
            logger.error(f"Wake word detection error: {e}")

        return False

    def _get_audio_frame(self):
        """Get audio frame for wake word detection"""
        try:
            # This is a placeholder - you'd implement proper audio frame capture
            # For now, we'll use the speech recognition to get audio
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=0.5, phrase_time_limit=0.5)
                # Convert to the format expected by Porcupine
                # This would require additional audio processing
                return None  # Simplified for this example
        except:
            return None

    def test_voice_system(self):
        """Test voice input and output systems"""
        try:
            self.speak("Voice system test. Please say something.")

            text = self.listen(timeout=5)
            if text:
                self.speak(f"I heard you say: {text}")
                return True
            else:
                self.speak("I didn't hear anything. Please check your microphone.")
                return False

        except Exception as e:
            logger.error(f"Voice system test failed: {e}")
            self.speak("Voice system test failed.")
            return False

    def cleanup(self):
        """Clean up resources"""
        try:
            if self.is_listening:
                self.stop_continuous_listening()

            if self.tts_engine:
                self.tts_engine.stop()

            if self.wake_word_detector:
                self.wake_word_detector.delete()

            logger.info("Voice processor cleaned up")

        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

# Example usage and testing
if __name__ == "__main__":
    processor = VoiceProcessor()

    # Test the voice system
    processor.test_voice_system()

    # Cleanup
    processor.cleanup()
