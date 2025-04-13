import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 
def speak(text):
    """Directly speaks the text."""
    engine.say(text)
    engine.runAndWait()
