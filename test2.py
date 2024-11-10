import wikipedia
from gtts import gTTS
from io import BytesIO
import pygame
from pydub import AudioSegment

def speak(text, tempo=1.2):
    """Converts text to speech and plays it with a specified tempo."""
    # Convert text to speech using gTTS
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
    
    # Initialize Pygame and play the audio
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(sped_up_fp, "mp3")
    pygame.mixer.music.play()
    
    # Wait until the audio finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def main():
    search_query = input("What to search? ")
    search_result = wikipedia.summary(search_query, sentences=2)
    
    # Speak the result
    speak("According to Wikipedia, " + search_result)

    # Optionally, print the summary as well
    print(search_result)

if __name__ == "__main__":
    main()
