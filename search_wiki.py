import wikipedia
from gtts import gTTS
from io import BytesIO
import pygame
from pydub import AudioSegment
import time

def speak(text):
    tempo = 1.2
    mp3_fp = BytesIO()
    tts = gTTS(text=str(text), lang="en", slow=False)
    tts.write_to_fp(mp3_fp)

    mp3_fp.seek(0)
    audio = AudioSegment.from_file(mp3_fp)
    audio = audio.speedup(tempo)

    sped_up_fp = BytesIO()
    audio.export(sped_up_fp, format="mp3")
    sped_up_fp.seek(0)
    return sped_up_fp

def main():
    search_result = wikipedia.summary(input("what to search? "), sentences=2)
    pygame.init()
    pygame.mixer.init()
    sound = speak("According to wikipedia, " + search_result)

    pygame.mixer.music.load(sound, "mp3")
    pygame.mixer.music.play()

    print(search_result)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
if __name__ == "__main__":
    main()

