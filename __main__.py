#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import time
from commands import *
import speech_recognition as sr
from playsound import playsound


# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        speech = recognizer.recognize_google(audio).lower()
        print("Google Speech Recognition thinks you said " + speech)
        if speech in commandsDict:
            playsound("sounds/ok.mp3")
            commandsDict[speech]()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# stops the listening and kills the file
def kill(): 
    stop_listening(wait_for_stop=False)
    os._exit(1)

r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

commandsDict = {"computer open jackass": jackass, 
                "computer turn on jackass": jackass,
                
                # it LOVES to read "jackass" as "jack" in this specific sentence so i gotta put both jic
                "computer open jack": jackass,
                "computer turn on jack": jackass,

                "computer open vinny": vinny,
                "computer turn on vinny": vinny,

                "stop listening": kill}

# keep thread alive
while True:
    time.sleep(0.1)
