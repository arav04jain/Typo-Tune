# import statement
import customtkinter
import tkinter
from transformers import pipeline
import pyglet
import speech_recognition as sr
import pyttsx3
import warnings
import logging

# Remove Warnings
logging.getLogger("transformers").setLevel(logging.ERROR)
warnings.filterwarnings('ignore')

# Model
model = pipeline("summarization", model="facebook/bart-large-cnn")

# Main Window:
window = customtkinter.CTk()
x = window.winfo_screenwidth()
y = window.winfo_screenheight()
window.geometry(str(x) + "x" + str(y) + "+0+0")
window.title("Typo Tune")
window.iconbitmap("logo.ico")
window.configure(fg_color="#ffffba")

# Main Frame:
mainFrame = customtkinter.CTkScrollableFrame(master=window, width=window._max_width, height=2000, border_width=4, border_color="black")
mainFrame.configure(fg_color="#ffffba")
mainFrame.pack(pady=4, padx=4)
mainFrame.rowconfigure(0, weight=1)
mainFrame.rowconfigure(1, weight=1)
mainFrame.rowconfigure(2, weight=1)
mainFrame.rowconfigure(3, weight=1)
mainFrame.columnconfigure(0, weight=2)
mainFrame.columnconfigure(1, weight=1)

# Speaker Setting:
speaker = pyttsx3.init()
speaker.setProperty('rate', 125)
speaker.setProperty('volume', 0.8)

# Dyslexia Font:
pyglet.font.add_file('font/OpenDyslexic3-Regular.ttf')

# Important Functions
def simplify(text):
    sim = model(text, max_length=1000, min_length=0, do_sample=False)
    return sim[0]['summary_text']

def friendly():
    mainFrame.result.delete("0.0", "end")
    mainFrame.result.insert("0.0", simplify(mainFrame.textbox.get("1.0", "end-1c")))
def say():
    speaker.say(mainFrame.result.get("1.0", "end-1c"))
    speaker.runAndWait()
def audio():
    r = sr.Recognizer()
    mainFrame.textbox.delete("0.0", "end")
    with sr.Microphone() as source:
        audio_text = r.listen(source)
        try:
            mainFrame.textbox.insert("0.0", r.recognize_google(audio_text))

        except:
            mainFrame.textbox.insert("0.0", "Please Retry the Audio")



# Elements of Window:
title = customtkinter.CTkLabel(mainFrame, text="Typo Tune", text_color="black", font=("OpenDyslexic 3", 35))
title.grid(pady=10, padx=10, column=0, row=0)

image = tkinter.PhotoImage(file="logo2.png")
image_label = tkinter.Label(mainFrame, image=image)
image_label.grid(column=1, row=0, pady=10, padx=10)

mainFrame.textbox = customtkinter.CTkTextbox(master=mainFrame, width=x * .75, corner_radius=10, border_width=2, border_color="black", height=y / 2.9, border_spacing=5, font=("OpenDyslexic 3", 20), fg_color="#EDE8DC")
mainFrame.textbox.grid(row=1, column=0, sticky="nsew", pady=10, padx=10)
mainFrame.textbox.insert("0.0", "Text to be simplified")

mainFrame.result = customtkinter.CTkTextbox(master=mainFrame, width=x * .75, corner_radius=10, border_width=2, border_color="black", height=y / 2.9, border_spacing=5, font=("OpenDyslexic 3", 20), fg_color="#EDE8DC")
mainFrame.result.grid(row=3, column=0, sticky="nsew", pady=10, padx=10)
mainFrame.result.insert("0.0", "Get Result Here")

convert = customtkinter.CTkButton(mainFrame, text="Make it Friendly", command=friendly, font=("OpenDyslexic 3", 25))
convert.grid(row=2, column=0, pady=10, padx=10)

audio = customtkinter.CTkButton(mainFrame, text="🔊", command=audio, font=("OpenDyslexic 3", 25), width=20)
audio.grid(row=1, column=1, pady=10, padx=10)
speak = customtkinter.CTkButton(mainFrame, text="🔊", command=say, font=("OpenDyslexic 3", 25), width=20)
speak.grid(row=3, column=1, pady=10, padx=10)

window.mainloop()



