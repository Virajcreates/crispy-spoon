import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
from googlesearch import search
from sympy import sympify,N

listener = sr.Recognizer()
machine = pyttsx3.init()
voices = machine.getProperty('voices')

# Print the available voices and their IDs
for i, voice in enumerate(voices):
    print(f"Voice ID {i}: {voice.name}")

# Set the desired voice (replace index with the desired voice ID)
voice_id = 1  # Change this to the index of the voice you want
machine.setProperty('voice', voices[voice_id].id)

def talk(text):
    machine.say(text)
    machine.runAndWait()

def input_instruction():
    instruction=""
    try:
        with sr.Microphone() as origin:
            print("listening...")
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech, language="en-in")

            instruction = instruction.lower()
            if "Joscata" in instruction:
                instruction = instruction.replace("Joscata", "")
                print(instruction)
    except sr.UnknownValueError:
        pass
    return instruction

def play_joscata():
    instruction = input_instruction()
    print(instruction)
    if "play" in instruction:
        song = instruction.replace('play', "")
        talk("playing " + song)
        pywhatkit.playonyt(song)
        play_joscata()
    elif 'time' in instruction:
        time = datetime.datetime.now().strftime("%I:%M %p")
        talk('Current time is ' + time)
        play_joscata()
    elif 'date' in instruction:
        date = datetime.datetime.now().strftime("%m/%d/%Y")
        talk("Today's date is " + date)
        play_joscata()
    elif 'how are you' in instruction:
        talk('I am fine, how about you?')
        play_joscata()
    elif "what is your name" in instruction:
        talk("I am Joscata, what can I do for you?")
        play_joscata()
    elif "who is" in instruction:
        human = instruction.replace("who is", "")
        try:
            info = wikipedia.summary(human, 1)
            print(info)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk("Multiple results found. Please be more specific.")
        play_joscata()
    elif "stop" in instruction:
        talk("Nice Chatting with you")
    elif "search" in instruction:
        query = instruction.replace("search", "")
        talk(f"Searching Google for {query}")
        
        # Using Google search to get the top search results
        for result in search(query, num_results=5):
            print(result)
            talk(result)
            
        play_joscata()
    
    elif "calculate" in instruction:
        expression = instruction.replace("calculate", "")
        expression = expression.replace("multiplied by", "*")
        expression = expression.replace("into", "*")
        expression = expression.replace("x", "*")
        expression = expression.replace("divided by", "*")
        try:
            result = sympify(expression)
            result = N(result)  # Convert to a numerical value
            talk(f"The result is {result}")
            print(result)
        except Exception as e:
            talk("Sorry, I couldn't perform the calculation.")

        play_joscata()
        
    else:
        talk('Please repeat')
        play_joscata()
play_joscata()

