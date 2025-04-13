from tkinter import *
from PIL import Image, ImageTk
from listener import take_command
from assistant import handle_command
from speak import speak
import threading

# --- GUI SETUP ---
root = Tk()
root.title("Avera")
root.geometry("575x775")
root.resizable(False, False)
root.config(bg="#6f8faf")

# --- Functions ---
def ask():
    def run():
        text.insert(END, "Listening...\n")
        text.update()  
        command = take_command() 
        text.insert(END, f"You: {command}\n")
        response = handle_command(command, return_response=True)
        text.insert(END, f"Avera: {response}\n")
        speak(response) 
        
    threading.Thread(target=run).start()

def send():
    user_input = entry.get()
    if user_input:
        text.insert(END, f"You: {user_input}\n")
        response = handle_command(user_input, return_response=True)
        text.insert(END, f"Avera: {response}\n")
        speak(response)
        entry.delete(0, END)

def delete():
    text.delete(1.0, END)
    
def on_entry_click(event):
    if entry.get() == "Type here":
        entry.delete(0, END)
        entry.config(fg='black')  

def on_focusout(event):
    if entry.get() == "":
        entry.insert(0, "Type here")
        entry.config(fg='grey') 


# --- Frame & Image ---
frame = LabelFrame(root, padx=50, pady=7, borderwidth=3, relief="raised", bg="#6f8faf", width=450, height=500)
frame.grid(row=0, column=1, padx=55, pady=10)
frame.grid_propagate(False)

text_label = Label(frame, text="AVERA", font=("Comic Sans MS", 15, "bold"), bd=5, bg="#356696")
text_label.grid(row=0, column=0, padx=20, pady=10)

try:
    image = Image.open("assistant.jpg")
    image = image.resize((300, 300), Image.Resampling.LANCZOS)
    image = ImageTk.PhotoImage(image)
    image_label = Label(frame, image=image)
    image_label.grid(row=1, column=0, padx=20, pady=10)
    image_label.image = image
except Exception as e:
    print(f"Error loading image: {e}")

# --- Text area ---
text = Text(root, font=('courier 10 bold'), bg="#356696")
text.place(x=100, y=520, width=375, height=100)


# --- Entry box ---
entry = Entry(root, justify=CENTER, fg='grey')
entry.insert(0, "Type here")
entry.place(x=112.5, y=630, width=350, height=50)
entry.bind("<FocusIn>", on_entry_click)
entry.bind("<FocusOut>", on_focusout)


# --- Buttons ---
button_width = 120
button_height = 45
gap = 20
total_width = 3 * button_width + 2 * gap
start_x = (575 - total_width) // 2

Button1 = Button(root, text="PROMPT", bg="#356696", borderwidth=3, relief=SOLID, command=ask)
Button1.place(x=start_x, y=700, width=button_width, height=button_height)

Button2 = Button(root, text="SUBMIT", bg="#356696", borderwidth=3, relief=SOLID, command=send)
Button2.place(x=start_x + button_width + gap, y=700, width=button_width, height=button_height)

Button3 = Button(root, text="DELETE", bg="#356696", borderwidth=3, relief=SOLID, command=delete)
Button3.place(x=start_x + 2 * (button_width + gap), y=700, width=button_width, height=button_height)

def greet_user():
    text.insert(END, "Avera: Hello, I am Avera, your AI assistant. How can I help you today?\n")
    speak("Hello, I am Avera, your AI assistant. How can I help you today?")

root.after(1000, greet_user)
root.mainloop()
