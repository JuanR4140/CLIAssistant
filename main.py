import os
import time
import playsound
import speech_recognition as sr
import pickle
from gtts import gTTS
import datetime
import ctypes
import pywhatkit
import pyjokes
import requests
from bs4 import BeautifulSoup

apps = {
    "clone hero": "C:\\Users\\juanr\\Desktop\\Clone Hero\\CLone Hero.exe",
    "youtube": "https://www.youtube.com/"
}

def clear():
    os.system("cls")

def say(text):
    tts = gTTS(text=text, lang="en")
    file = "voice.mp3"
    tts.save(file)
    playsound.playsound(file)
    os.remove("voice.mp3")

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print(f"Exception: {str(e)}")

    return said

def status(title, status, separator, wake):
    clear()
    print(f"{title}".center(40, " "))
    print(f"To wake up assistant, say: 'Hey {wake}'".center(40, " "))
    print(f"Status: {status}".center(40, separator))

def save(text, file):
    pickle.dump(text, open(f"{file}", "wb"))

def load(file):
    return str(pickle.load(open(f"{file}", "rb"))).split(";")

def note(text):
    date = datetime.datetime.now()
    file = str(date).replace(":", "-") + "-note.txt"
    os.chdir("texts")
    with open(file, "w") as f:
        f.write(text)
    os.chdir("..")
    f.close()


if not os.path.isfile("data.cli"):
    print("It seems you do not currently have CLI Assistant installed.")
    print("Please answer the following questions to sign up for CLI.\n")
    name = input("[What is your name?] >")
    wakeup = input("[What is your preferred wake-up word for the assistant?] >")

    save(f"{name};{wakeup}", "data.cli")
    print("CLI Assistant installed. Restart required.")
    input("> ");exit


data = load("data.cli")
wakeup = data[1].lower()

while True:
    status("CLI Assistant", "Waiting for wake-up word..", "-", wakeup)
    text = listen()
    if text.count(wakeup) > 0:
        say("Listening")
        status("CLI Assistant", "Listening for command..", "-", wakeup)
        text = listen()
        text = text.lower()

        notecmds = ["note", "remember"]
        for phrase in notecmds:
            if phrase in text:
                text = text.split(phrase)[1]
                note(text)
                say("I've noted it down.")

        googlecmds = ["google", "search up"]
        for phrase in googlecmds:
            if phrase in text:
                google = "https://www.google.com/search?q="
                text = text.split(phrase)[1]
                say(f"Searching for: {text} on Google")
                google += text.replace(" ", "+")
                os.system(f"start {google}")

        appscmds = ["open", "launch"]
        for phrase in appscmds:
            if phrase in text:
                text = text.split(phrase)
                text = text[1]
                text = text[1:]

                for name, path in apps.items():
                    if name == text:
                        say(f"Opening: {name}")
                        os.system(f'start "" "{path}"')

        if "youtube" in text:
            yt = "https://www.youtube.com/results?search_query="
            text = text.split("youtube")[1]
            say(f"Searching for: {text} on YouTube")
            yt += text.replace(" ", "+")
            os.system(f"start {yt}")

        if "play" in text:
            url = "https://www.azlyrics.com/lyrics/beatles/"
            text = text.split("play")[1]
            say(f"Searching lyrics for: {text} on AZLyrics")
            url += text.replace(" ", "") + ".html"
            req = requests.get(url)
            if req.status_code == 404:
                say(f"Song: {text} does not have any lyrics on AZLyrics.")
                say(f"Playing song: {text} on YouTube")
                pywhatkit.playonyt(text)
            else:
                say("Lyrics found.")
                soup = BeautifulSoup(req.content, "html.parser")
                lyrics = soup.find_all("div")[20].get_text()
                print(lyrics)
                say("Playing song on YouTube")
                pywhatkit.playonyt(text)
                input("> ")

        if "tell me a joke" in text:
            say("Sure, here's a joke for you.")
            say(pyjokes.get_joke(language="en", category="neutral"))

        if "say" in text:
            say(text.split("say")[1])

        infocmds = ["who", "what", "when", "where", "why", "how"]
        for phrase in infocmds:
            if phrase in text:
                say(f"Searching for information on query: {text}")
                say(pywhatkit.info(text, 3, True))

        if "shutdown" in text:
            say("shutting down..")
            exit()

        lockcmds = ["lock", "lock computer"]
        for phrase in lockcmds:
            if phrase in text:
                say("Locking up computer.")
                ctypes.windll.user32.LockWorkStation()