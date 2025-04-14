import speech_recognition as sr
import pyttsx3
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Speak out the given text."""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen to the user's voice input and return it as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")  # ✅ Show visually instead of speaking
        time.sleep(0.5)  # Short pause to ensure mic is ready
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=7)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "Sorry, there was an issue with the speech recognition service."
        except sr.WaitTimeoutError:
            return "Sorry, the listening process timed out."

# Example usage
if __name__ == "__main__":
    while True:
        command = take_command()
        print("You said:", command)
        if "stop" in command:
            speak("Goodbye!")
            break
        # You can add more command processing logic here
