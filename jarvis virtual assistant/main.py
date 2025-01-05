import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import openai
from gtts import gTTS
import pygame
import time
import os

#  pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "4b75b96f21bb45df9c971807aedbbadc"


def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):   
    tts = gTTS(text)
    tts.save('temp.mp3')
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    mp3_file = "temp.mp3"  # Replace with your MP3 file path
    pygame.mixer.music.load(mp3_file)

    # Play the MP3 file
    pygame.mixer.music.play()

    # Wait while the music is playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)  # Sleep for a short duration to prevent busy-waiting

    # Stop the playback to release the file lock
    pygame.mixer.music.stop()
    pygame.mixer.quit()  # Cleanly quit the mixer

    # Remove the temporary MP3 file
    try:
        os.remove("temp.mp3")
        print("Temporary file deleted.")
    except PermissionError as e:
        print(f"Error deleting file 'temp.mp3': {e}")

    

def aiprocess(command):
    client = openai(
    api_key = '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',
)

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant jarvis skilled in general tasks like alexa and google cloud."},
            {
            "role": "user",
            "content": "what is coding."
            }
        ]
    )
    return completion.choices[0].message

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link =  musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=4b75b96f21bb45df9c971807aedbbadc")
        if r.status_code == 200:
            #parse the json response
            data = r.json()

            #extract the articles
            articles = data.get('articles', [])

            #print the headlines
            for article in articles:
                speak(article['title'])
    
    else:
        #let open ai handle the request
        output = aiprocess(c)
        speak(output)


    

if __name__ == "__main__":
    speak("initializing jarvis...")
    while True:
        #listen for the wake word "jarvis"
        #obtain audio from the microphone
        r = sr.Recognizer()
        
        print("recognizing..")
        try:
            with sr.Microphone() as source:
                print("Listening..")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("yes furqaan")
                #listen for command
                with sr.Microphone() as source:
                    print("jarvis active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("error; {0}".format(e))