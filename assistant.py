from commands import perform_action
from speak import speak

def handle_command(command, return_response=False):
    if 'exit' in command:
        response = "Goodbye, take care! Have a wonderful day ahead!"
        speak(response)
        if return_response:
            return response
        exit()
    else:
        response = perform_action(command)
        if return_response:
            return response
