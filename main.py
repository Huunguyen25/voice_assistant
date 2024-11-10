import tkinter as tk
from tkinter import *
from tkinter import ttk
import speech_recognition as sr
import wikipedia as wiki
import wikipediaapi
from gtts import gTTS
from pydub import AudioSegment
from io import BytesIO
import pygame
import threading
import re

is_speaking = False
stop_requested = False

def speak(text, button):
    global is_speaking, stop_requested
    is_speaking = True
    stop_requested = False
    tempo = 1.2
    mp3_fp = BytesIO()
    tts = gTTS(text=str(text), lang="en", slow=False)
    tts.write_to_fp(mp3_fp)
    
    # Convert the MP3 file to an audio segment and speed it up
    mp3_fp.seek(0)
    audio = AudioSegment.from_file(mp3_fp)
    audio = audio.speedup(tempo)
    
    # Export the sped-up audio to a new BytesIO object
    sped_up_fp = BytesIO()
    audio.export(sped_up_fp, format="mp3")
    sped_up_fp.seek(0)

    button.config(text="Stop")
    
    # Initialize Pygame and play the audio
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(sped_up_fp, "mp3")
    pygame.mixer.music.play()
    
    # Wait until the audio finishes playing
    while pygame.mixer.music.get_busy():
        if stop_requested:
            pygame.mixer.music.stop()
            break
        pygame.time.Clock().tick(10)
    
    is_speaking = False
    stop_requested = False
    button.config(text="Assist")

def stop_speaking():
    global stop_requested
    stop_requested = True
    
def take_command():
    r = sr.Recognizer()
    r.pause_threshold = 1.5
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language="en-US")
    except LookupError:
        return "Could not understand audio"
    return query 

def perform_task(text_widget, button):
    global is_speaking
    if is_speaking:
        stop_speaking()
        return
    
    query = take_command().lower()
    text_widget.insert('1.0', query + '\n'*2)
    text_widget.update()
    if 'wikipedia' in query:
        query_result = refined_search_wiki(query.replace("wikipedia", ""))
        if query_result:
            text_widget.insert('1.0', query_result + '\n'*2)
            text_widget.update()
            threading.Thread(target=speak, args=(query_result, button)).start()
        else:
            text_widget.insert('1.0', "Sorry, I couldn't find relevant information.\n")
            speak("Sorry, I couldn't find relevant information.")

def refined_search_wiki(query):
    sentence_limit = 2
    wiki_wiki = wikipediaapi.Wikipedia('voiceassistant', 'en')
    try:
        refined_query = query.lower().replace("who is", "").replace("what is", "").strip()
        if not refined_query:
            return "The query is empty. Please provide a valid search term."
        search_results = wiki.search(refined_query)
        if not search_results:
            return
        best_match = None
        for result in search_results:
            if len(result.split()) > 1:
                best_match = result
                break
        if not best_match:
            best_match = search_results[0]
        page = wiki_wiki.page(best_match)
        if not page.exists():
            return "The Wikipedia page could not be found."
        summary_text = page.summary

        sentence_endings = re.compile(r'(?<!\b(?:U|e)\.S\.|etc\.)\.(?=\s[A-Z])')
        summary_sentences = sentence_endings.split(summary_text)

        limited_summary = '.'.join(summary_sentences[:sentence_limit]) if sentence_limit > 0 else ''
        return "According to Wikipedia, " + limited_summary
    
    except wiki.DisambiguationError as e:
        return f"Multiple results found for '{query}'. Please be more specific."
    except wiki.exceptions.PageError:
        return "The Wikipedia page could not be found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def on_closing():
    stop_speaking()
    root.destroy()
def main():
    global root
    root = tk.Tk()
    root.title("Voice Assistant")

    text_widget = tk.Text(font=('Arial', 15))
    text_widget.grid(column=0, row=0)

    button_frame = tk.Frame()
    button_frame.grid(column=0, row=1)

    assist_button = ttk.Button(button_frame, text='assist', command=lambda: perform_task(text_widget, assist_button))
    assist_button.grid(column=0, row=0)
    # button call start_task ---> perform_task ---> take_command
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
if __name__ == '__main__':
    main()