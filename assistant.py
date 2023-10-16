import os
import openai
import time
import speech_recognition as sr
import pyttsx3
import subprocess
import numpy as np
from gtts import gTTS

mytext = 'Bienvenue'
language = 'fr'
# from os.path import join, dirname
# import matplotlib.pyplot as plt
# ^ matplotlib is great for visualising data and for testing purposes but usually not needed for production
# openai.api_key='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'
openai.api_base = "http://localhost:4891/v1"
openai.api_key=''

model = "mistral-openorca"
# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init("dummy")
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)
name = "Alex"
greetings = [f"Captain {name}! Commen vas tu?"]
def listen_for_wake_word(source):
    print("En attente d'activation 'Oracle'...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='fr-FR')
            if "oracle" in text.lower():
                print("Mot clés détecté.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass
# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Vas-si parles")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='fr-FR')
            print(f"Tu as dis : {text}")
            if not text:
                continue
            # Send input to OpenAI API
            # response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{text}"}])
            response = openai.Completion.create(model=model, prompt=f"{text}", max_tokens=2048, stop=["\n"])
            response_text = response.choices[0].text
            print(response_text)

            # Check if the response text is empty
            if response_text:
                print("generating audio")
                myobj = gTTS(text = response_text, lang = language, slow = False)
                myobj.save("response.mp3")
                print("speaking")

                subprocess.run(["vlc", "response.mp3"])
                # Speak the response
                print("speaking")
                engine.say(response_text)
                engine.runAndWait()
            else:
                print("No response from OpenAI")
        except sr.UnknownValueError:
            time.sleep(10)
            print("Silence...")
            listen_for_wake_word(source)
            break
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            listen_for_wake_word(source)
            break

# Use the default microphone as the audio source
with sr.Microphone() as source:
    listen_for_wake_word(source)
