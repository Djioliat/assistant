import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import numpy as np

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration de l'API OpenAI
openai.api_key = 'clés-API-openai'
model = 'gpt-4'

# Initialisation de la synthèse vocale
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Vous pouvez changer l'indice pour choisir une voix différente

# Création de l'objet Recognizer en dehors de la fonction
r = sr.Recognizer()

# Définir le nom et les salutations
name = "Nom"
greetings = [
    f"Quoi de neuf maître {name} ?",
]

# Fonction pour écouter le mot de réveil
def listen_for_wake_word(source):
    print("En attente du mot de réveil 'Biloute'...")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='fr-FR')
            if "biloute" in text.lower():
                print("Mot de réveil détecté.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass

# Fonction pour écouter et répondre avec l'API OpenAI
def listen_and_respond(source):
    print("En écoute...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='fr-FR')
            print(f"Vous avez dit : {text}")
            if not text:
                continue

            # Envoyer l'entrée à l'API OpenAI
            response = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": f"{text}"}])
            response_text = response.choices[0].message.content

            print(response_text)

            # Générer et sauvegarder le fichier audio
            myobj = gTTS(text=response_text, lang='fr', slow=False)
            # Lire la réponse
            os.system("cvlc response.mp3")

  # Parler la réponse
            engine.say(response_text)
            engine.runAndWait()

            if not audio:
                listen_for_wake_word(source)

        except sr.UnknownValueError:
            time.sleep(22)
            print("Silence détecté, en attente, à l'écoute...")
            listen_for_wake_word(source)
            break
        except sr.RequestError as e:
            print(f"Impossible de récupérer les résultats ; {e}")
            engine.say(f"Impossible de récupérer les résultats ; {e}")
            engine.runAndWait()
            listen_for_wake_word(source)
            break

# Utiliser le microphone par défaut comme source audio
with sr.Microphone() as source:
    listen_for_wake_word(source)

            # Lire la réponse
            os.system("cvlc response.mp3")

  # Parler la réponse
            engine.say(response_text)
            engine.runAndWait()

            if not audio:
                listen_for_wake_word(source)

        except sr.UnknownValueError:
            time.sleep(22)
            print("Silence détecté, en attente, à l'écoute...")
            listen_for_wake_word(source)
            break
        except sr.RequestError as e:
            print(f"Impossible de récupérer les résultats ; {e}")
            engine.say(f"Impossible de récupérer les résultats ; {e}")
            engine.runAndWait()
            listen_for_wake_word(source)
            break

# Utiliser le microphone par défaut comme source audio
with sr.Microphone() as source:
    listen_for_wake_word(source)

