#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

# TODO: maybe add fuzzy matching


import time, os, glob

import speech_recognition as sr
from playsound import playsound

basedir = os.path.dirname(os.path.abspath(__file__))
shortcutpath = os.path.join(basedir, "shortcuts")


# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        speech = recognizer.recognize_google(audio).lower()
        print("Google Speech Recognition thinks you said " + speech)
        if "computer" in speech:
            keyword = speech[speech.index("computer"):]
            if keyword in shortcuts:
                playsound("sounds/ok.mp3")
                
                os.system(glob.glob(shortcutpath + "\\" + shortcuts[keyword] + ".*")[0])
            else:
                playsound("sounds/no.mp3")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# stops the listening and kills the process
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

shortcuts = {
    "computer open jackass": "jackass",
    "computer turn on jackass": "jackass",
    
    # it LOVES to read "jackass" as "jack" in this specific sentence so i gotta put both jic
    "computer open jack": "jackass",
    "computer turn on jack": "jackass",

    "computer open vinny": "vinny",
    "computer turn on vinny": "vinny",

    "computer turn on youtube": "youtube",

    "computer open trimmer": "trimmer",

    "computer let's go gambling": "gambling",
    "computer let's go gam": "gambling",

    "computer open hsr": "hsr",

    "computer the other one": "other",
    
    "computer clip that":  "clip",

    "computer start recording": "record",
    "computer stop recording": "record",

    "stop listening": kill
}


# keep thread alive
while True:
    time.sleep(0.1)
