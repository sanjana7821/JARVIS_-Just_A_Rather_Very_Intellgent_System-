import re
import struct
from time import time
from click import command
import eel
import os
import pygame  # Updated import
import pvporcupine
import pyaudio
from engine.config import ASSISTANT_NAME
from engine.command import speak
import pywhatkit as kit
from engine.helper import extract_yt_term

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    pygame.mixer.init()  # Initialize the mixer
    pygame.mixer.music.load(music_dir)  # Load the audio file
    pygame.mixer.music.play()  # Play the audio
    while pygame.mixer.music.get_busy():  # Wait until the audio finishes playing
        continue

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower()
    if query != '':
        speak('Opening ' + query)
        os.system('start ' + query)
    else:
        speak('Not Found')

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if not search_term:
        speak("Sorry, I couldn't understand what to play on YouTube.")
        return
    speak("Playing " + search_term + " on YouTube")
    try:
        kit.playonyt(search_term)
    except Exception as e:
        speak("Failed to play on YouTube. Please check your internet connection or try again.")

@eel.expose
def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)
            if keyword_index >= 0:
                print("hotword detected")
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()