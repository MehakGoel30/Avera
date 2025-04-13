from listener import take_command
from speak import speak
from assistant import handle_command

speak("Hello! I am your AI assistant. How can I help you today?")

while True:
    command = take_command()
    if command:
        handle_command(command)
