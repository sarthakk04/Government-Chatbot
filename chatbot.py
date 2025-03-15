import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import pygame
import os
from langdetect import detect

# Configure Google Gemini API
genai.configure(api_key="AIzaSyBB7oqHq3oKbsk3MIThmHuB94k5IaTpMP4")

# Initialize the model
generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config
)

# Initialize chat session with predefined role
chat = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "Consider yourself as Rahul. You know each and every law of Maharashtra, including the Department of Land Records and legal processes. Your task is to provide accurate, up-to-date, and verified information. If someone asks about a topic, provide complete steps, the whole process, and necessary resources."
            ],
        },
        {
            "role": "model",
            "parts": [
                "Hello, I'm Rahul, your expert on Maharashtra laws and land records. I will provide verified and complete information on any legal topic you ask. How can I assist you today?"
            ],
        }
    ]
)

def initialize_audio():
    pygame.mixer.init()

def detect_language(text):
    try:
        lang = detect(text)
        return lang if lang in ['mr', 'hi', 'en'] else 'en'
    except:
        return 'en'

def listen_to_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, timeout=5)
    
    try:
        text = r.recognize_google(audio, language="mr-IN")
        lang = detect_language(text)
        return text, lang
    except sr.UnknownValueError:
        return "Could not understand audio", "en"
    except sr.RequestError:
        return "Could not request results", "en"

def speak_response(text, lang):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    if lang == "mr":
        engine.setProperty('voice', voices[0].id)  # Adjust for Marathi voice if available
    elif lang == "hi":
        engine.setProperty('voice', voices[1].id)  # Adjust for Hindi voice
    else:
        engine.setProperty('voice', voices[2].id)  # Default English voice
    
    engine.setProperty('rate', 180)  # Speed up voice
    engine.say(text)
    engine.runAndWait()

def main():
    initialize_audio()
    print("🤖 Chatbot is ready! Speak in English, Hindi, or Marathi")
    
    while True:
        try:
            user_input, detected_lang = listen_to_speech()
            print(f"🗣️ You: {user_input}")
            
            if user_input.lower() in ['quit', 'exit', 'बंद', 'बंद करो']:
                print("👋 Goodbye!")
                break
            
            response = chat.send_message(user_input)
            response_text = response.text.replace("*", "").strip()
            print(f"🤖 Bot: {response_text}")
            
            speak_response(response_text, detected_lang)
        
        except Exception as e:
            print(f"⚠️ Error: {str(e)}")
            continue

if __name__ == "__main__":
    main()