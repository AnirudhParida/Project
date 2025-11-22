import speech_recognition as sr
import pyttsx3
import threading


class Listener:
    """Handles speech-to-text conversion."""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise on initialization
        print("Calibrating microphone for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Microphone ready!")

    def listen(self, timeout=5, phrase_time_limit=10):
        """
        Listen for voice input and convert to text.
        
        Args:
            timeout (int): Seconds to wait for speech to start
            phrase_time_limit (int): Max seconds for a phrase
            
        Returns:
            str: Recognized text or error message
        """
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, 
                                              phrase_time_limit=phrase_time_limit)
            
            print("Processing speech...")
            # Use Google Web Speech API (free)
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            return "ERROR:TIMEOUT"
        except sr.UnknownValueError:
            return "ERROR:UNCLEAR"
        except sr.RequestError as e:
            return f"ERROR:SERVICE:{str(e)}"
        except Exception as e:
            return f"ERROR:{str(e)}"


class Speaker:
    """Handles text-to-speech conversion."""
    
    def __init__(self):
        self.engine = pyttsx3.init()
        
        # Configure voice properties
        voices = self.engine.getProperty('voices')
        # Try to use a female voice if available (usually index 1)
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        
        # Set speech rate (default is 200)
        self.engine.setProperty('rate', 175)
        
        # Set volume (0.0 to 1.0)
        self.engine.setProperty('volume', 0.9)

    def speak(self, text, async_mode=False):
        """
        Convert text to speech.
        
        Args:
            text (str): Text to speak
            async_mode (bool): If True, speak in background thread
        """
        print(f"Agent: {text}")
        
        if async_mode:
            # Run in separate thread to avoid blocking
            thread = threading.Thread(target=self._speak_sync, args=(text,))
            thread.daemon = True
            thread.start()
        else:
            self._speak_sync(text)

    def _speak_sync(self, text):
        """Internal method to speak synchronously."""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in speech synthesis: {e}")


# Quick test function
if __name__ == "__main__":
    print("Testing Speech Engine...")
    
    # Test TTS
    speaker = Speaker()
    speaker.speak("Hello! I am your OS agent. Speech engine is working correctly.")
    
    # Test STT
    print("\nNow testing microphone. Please say something...")
    listener = Listener()
    result = listener.listen()
    
    if result.startswith("ERROR"):
        print(f"Listening failed: {result}")
    else:
        print(f"Success! I heard: {result}")
        speaker.speak(f"You said: {result}")
