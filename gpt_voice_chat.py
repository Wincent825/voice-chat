import speech_recognition as sr
import pyttsx3
import openai

openai.api_key = "YOUR_API_KEY"

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
        
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages = [{"role": "user", "content": listen()}],
    max_tokens = 1024,
    temperature = 0.8)

message = completion.choices[0].message.content
speak(str(message))
print(message)
