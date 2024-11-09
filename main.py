import tkinter as tk
from tkinter import *
from tkinter import ttk
import speech_recognition as sr
import wikipedia as wiki
from gtts import gTTS

def speak(text):
    pass

def take_command():
    r = sr.Recognizer()
    r.pause_threshold = 1
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language="en-US")
    except LookupError:
        return "Could not understand audio"
    return query 

def perform_task(text_widget):
    query = take_command().lower()
    if 'wikipedia' in query:
        query = refined_search_wiki(query.replace("wikipedia", ""))
        text_widget.insert('0.0', "According to wikipedia, " +query + '\n')
        text_widget.insert('0.0', "\n")
        
def refined_search_wiki(query):
    try:
        refined_query = query.lower().replace("who is", "").replace("what is", "").strip()
        search_results = wiki.search(refined_query)
        if not search_results:
            return 
        best_match = search_results[0]
        return wiki.summary(best_match, sentences=2)
    
    except wiki.DisambiguationError as e:
        return f"Multiple results found for '{query}'. Please be more specific."
    except wiki.exceptions.PageError:
        return "The Wikipedia page could not be found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    root = tk.Tk()
    root.title("Voice Assistant")

    text_widget = tk.Text(font=('Arial', 15))
    text_widget.grid(column=0, row=0)

    button_frame = tk.Frame()
    button_frame.grid(column=0, row=1)

    save_button = ttk.Button(button_frame, text='assist', command=lambda: perform_task(text_widget))
    save_button.grid(column=0, row=0)
    # button call start_task ---> perform_task ---> take_command

    root.mainloop()
if __name__ == '__main__':
    main()