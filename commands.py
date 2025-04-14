import speech_recognition as sr
import datetime
import webbrowser
import re
import calendar
import pywhatkit
import pyautogui

# Mapping words to digits
text_to_num = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
    'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
    'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
    'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19,
    'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60,
    'seventy': 70, 'eighty': 80, 'ninety': 90
}

def convert_words_to_digits(text):
    words = text.lower().split()
    digits = []
    for word in words:
        if word in text_to_num:
            digits.append(text_to_num[word])
        elif word.isdigit():
            digits.append(int(word))
    return digits

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=10)
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "Sorry, there was an issue with the speech recognition service."
        except sr.WaitTimeoutError:
            return "Sorry, the listening process timed out."

def perform_action(command):
    command = command.lower()
    command = re.sub(r'[^\w\s]', '', command)

    if 'hi avera' in command or 'hello avera' in command or 'hey avera' in command or 'avera' in command:
        return "Hi there! How can I assist you today?"

    if 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        return f"The time is {time}"

    if 'date' in command:
        date = datetime.datetime.now().strftime('%A, %B %d, %Y')
        return f"Today's date is {date}"

    if 'what day is it' in command or 'what is the day today' in command or 'what day it is' in command or 'it is ' in command or 'is it' in command:
        day_of_week = calendar.day_name[datetime.datetime.now().weekday()]
        return f"Today is {day_of_week}."

    # Math
    if 'add' in command or '+' in command or 'plus' in command:
        numbers = convert_words_to_digits(command)
        if len(numbers) >= 2:
            return f"The result is {sum(numbers)}"
        return "Please provide two or more numbers to add."

    elif 'subtract' in command or '-' in command or 'minus' in command:
        numbers = convert_words_to_digits(command)
        if len(numbers) >= 2:
            result = numbers[0] - numbers[1]
            return f"The result is {result}"
        return "Please provide two numbers to subtract."

    elif 'multiply' in command or 'x' in command or 'X' in command:
        numbers = convert_words_to_digits(command)
        if len(numbers) >= 2:
            result = numbers[0] * numbers[1]
            return f"The result is {result}"
        return "Please provide two numbers to multiply."

    elif 'divide' in command or '/' in command or 'division' in command:
        numbers = convert_words_to_digits(command)
        if len(numbers) >= 2 and numbers[1] != 0:
            result = numbers[0] / numbers[1]
            return f"The result is {result:.2f}"
        return "Please provide two numbers to divide, and make sure the divisor is not zero."

    elif 'square of' in command:
        number = convert_words_to_digits(command)
        if number:
            num = number[0]
            return f"The square of {num} is {num ** 2}"
        return "Please provide a number to square."

    elif 'cube of' in command:
        number = convert_words_to_digits(command)
        if number:
            num = number[0]
            return f"The cube of {num} is {num ** 3}"
        return "Please provide a number to cube."

    # Google/YouTube Search
    elif 'search for' in command or 'what do you mean by' in command or 'meaning of' in command or 'what is the meaning of' in command:
        if 'what do you mean by' in command:
            query = command.split('what do you mean by')[-1].strip()
        elif 'what is the meaning of' in command:
            query = command.split('what is the meaning of')[-1].strip()
        elif 'meaning of' in command:
            query = command.split('meaning of')[-1].strip()
        else:
            query = command.split('search for')[-1].strip()

        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching Google for: {query}"

    elif 'search on youtube for' in command:
        query = command.replace('search on youtube for', '').strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        return f"Searching on YouTube for {query}"

    elif 'play song' in command:
        song = command.replace('play song', '').strip()
        if song:
            pywhatkit.playonyt(song)
            return f"Playing song: {song} on YouTube"
        else:
            return "Please provide a song name to play."

    elif 'open youtube' in command:
        webbrowser.open('https://youtube.com')
        return "Opening YouTube"

    elif 'open google' in command:
        webbrowser.open('https://google.com')
        return "Opening Google"

    elif 'what is your name' in command:
        return "I am Avera, your virtual assistant."

    elif 'help' in command or 'how to use' in command or 'what can you do' in command:
        return ("You can ask me to:\n"
                "- Tell time or date\n"
                "- Search Google or YouTube\n"
                "- Do basic math\n"
                "- Play a song\n"
                "- Take notes\n"
                "- Open websites\n"
                "- Tell a joke\n"
                "- And more!")

    elif 'tell me a joke' in command:
        return "Why don't skeletons fight each other? They don't have the guts!"

    elif 'tell me a fact' in command or 'fun fact' in command or 'interesting fact' in command or 'fact' in command:
        return "Did you know? Honey never spoils. Archaeologists found 3000-year-old jars of honey in Egyptian tombs that still taste great!"

    elif any(phrase in command for phrase in ['take a note', 'write this down', 'take note', 'note']):
        for trigger in ['take a note', 'write this down', 'take note', 'note']:
            if trigger in command:
                note = command.split(trigger, 1)[-1].strip()
                break
        if note:
            with open("avera_notes.txt", "a") as f:
                f.write(f"{datetime.datetime.now()}: {note}\n")
            return "Note saved successfully!"
        else:
            return "What should I note down?"

    elif 'take screenshot' in command or 'take ss' in command:
        screenshot = pyautogui.screenshot()
        file_name = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        screenshot.save(file_name)
        return f"Screenshot taken and saved as {file_name}"

    elif 'repeat after me' in command:
        phrase = command.split('repeat after me')[-1].strip()
        return phrase if phrase else "Sure, what would you like me to repeat?"

    elif 'weather' in command:
        return "Weather functionality coming soon! Currently, I can't fetch live weather data."

    else:
        return "Sorry, I didn't quite understand that. Could you please rephrase your request?"
