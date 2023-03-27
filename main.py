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

conn = sqlite3.connect('responses.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS responses (keyword text, response text)')

# The keywords and responses
keywords = ["time", "joke", "riddle", "fact", "quit", "pasta"]
responses = ["It is bedtime", "What do you call a bear with no teeth? A gummy bear!", "What is full of holes but still holds water?", "Did you know that the average person spends 6 months of their life waiting on a red light to turn green?", "Goodbye!", "I like pasta!"]

for i in range(len(keywords)):
    c.execute("INSERT INTO responses VALUES (?, ?)", (keywords[i], responses[i]))
conn.commit()


# The main loop
while True:
    # Listen to the microphone
    text = listen()
    print(text)
    if text == "quit":
        quit()

    response_given = False
    # If question is recognized, respond with the correct response
    c.execute('SELECT response FROM responses WHERE keyword = ?', (text,))
    result = c.fetchone()
    if result is not None:
        speak(result[0])
        response_given = True

    # If question is not recognized, add the new response
    if response_given == False:
        speak("I don't know how to respond to that.")
        speak("What is the keyword of your question?")
        new_keyword = listen()
        print(keywords)
        speak("What should I answer?")
        new_response = listen()
        # Add the new keyword and response to the database
        c.execute('INSERT INTO responses VALUES (?, ?)', (new_keyword, new_response))
        conn.commit()
        speak("I have learned a new response!")
        
    
    

