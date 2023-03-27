import speech_recognition as sr
import pyttsx3

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

keywords = ["time", "joke", "riddle", "fact", "quit", "pasta"]
responses = ["It is bedtime", "What do you call a bear with no teeth? A gummy bear!", "What is full of holes but still holds water?", "Did you know that the average person spends 6 months of their life waiting on a red light to turn green?", "Goodbye!", "I like pasta!"]

# The main loop
while True:
    # Listen to the microphone
    text = listen()
    print(text)

    response_given = False
    # If question is recognized, respond with the correct response
    for i in range(len(keywords)):
        if text == None:
            speak("I didn't catch that. Please try again.")
            break
        
        if "quit" in text:
            speak(responses[i])
            quit()

        print(keywords[i])
        if keywords[i] in text:
            
            if "riddle" in text:
                speak(responses[i])
                answer = listen()
                if "a sponge" in answer or "sponge" in answer:
                    speak("Correct!")
                    response_given = True
                    break

                else:
                    speak("Incorrect! The answer is a sponge.")
                    response_given = True
                    break

            else:
                speak(responses[i])
                response_given = True
                break

    # If question is not recognized, add the new response
    if response_given == False:
        speak("I don't know how to respond to that.")
        speak("What is the keyword of your question?")
        new_keyword = listen()
        print(keywords)
        for i in range(len(keywords)):
            if keywords[i] in new_keyword:
                speak("I already know how to respond to that.")
                speak(responses[i])
                break
        keywords.append(new_keyword)
        speak("What should I answer?")
        responses.append(listen())
        print(responses)
        speak("I have learned a new response!")
        
    
    
    # Speak the recognized text
    #speak(text)
