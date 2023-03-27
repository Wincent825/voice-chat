import speech_recognition as sr
import pyttsx3
import sqlite3
import time

r = sr.Recognizer()
engine = pyttsx3.init()

# Speak the text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen to the microphone, and return the text.
# If it can't recognize the text, it will return an error message.
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None

def quit():
    exit()

try:
    conn = sqlite3.connect('responses.db')
except sqlite3.Error:
    print("Error connecting to database")
c = conn.cursor()
try:
    c.execute('CREATE TABLE IF NOT EXISTS responses (keyword text, response text)')
except sqlite3.Error:
    print("Error creating table")

# The main loop
while True:
    try:

        # Listen to the microphone
        text = listen()
        print(text)
        if text == "quit":
            quit()

        response_given = False
        # If question is recognized, respond with the correct response
        keywords = [row[0] for row in c.execute('SELECT keyword FROM responses')]
        for word in text.split():
            if word.lower() in keywords:
                c.execute('SELECT response FROM responses WHERE keyword = ?', (word.lower(),))
                result = c.fetchone()
                if result is not None:
                    # special case for riddle
                    if result[0] == "What is full of holes but still holds water?":
                        speak("What is full of holes but still holds water?")
                        time.sleep(5)
                        speak("A sponge!")
                        response_given = True
                        break
                    else:
                        speak(result[0])
                        response_given = True
                        break

        # If question is not recognized, add the new response
        if response_given == False:
            speak("I don't know how to respond to that.")
            speak("What is the keyword of your question?")
            new_keyword = listen()
            speak("What should I answer?")
            new_response = listen()
            # Add the new keyword and response to the database
            try:
                c.execute('INSERT INTO responses VALUES (?, ?)', (new_keyword.lower(), new_response))
                conn.commit()
                speak("I have learned a new response!")
            except sqlite3.Error as e:
                print(f"Error adding new response: {e}")
    except sr.UnknownValueError:
        print("Error listening to microphone")
    except sr.RequestError as e:
        print(f"Error: {e}")
