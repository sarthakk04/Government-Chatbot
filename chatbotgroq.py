import speech_recognition as sr
from groq import Groq
import pyttsx3
import pygame
import os
from langdetect import detect

# Initialize Groq client
client = Groq(api_key="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")

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
    
    # Debugging: List available voices
    # for i, voice in enumerate(voices):
    #     print(f"Voice {i}: {voice.name} ({voice.id})")
    
    if lang == "mr" and len(voices) > 0:
        engine.setProperty('voice', voices[0].id)  # Adjust if needed
    elif lang == "hi" and len(voices) > 1:
        engine.setProperty('voice', voices[1].id)  # Adjust if needed
    else:
        engine.setProperty('voice', voices[-1].id)  # Default English voice
    
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
            
            prompt = "Consider yourself as you know each and every law of Maharashtra and your name is Rahul. People will ask you questions about the Department of Land Record, laws of Maharashtra, so you need to answer them regarding that. Also, verify that the answers you are providing are up-to-date and correct. If someone is asking you about some topic, then you need to give complete steps and the whole process along with the resources needed for the task that the user asked you. Respond in the same language as the user's input."
            
            completion = client.chat.completions.create(
                model="mistral-saba-24b",
                messages=[
                    {"role": "user", "content": prompt + "\nUser's question: " + user_input}
                ],
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                stream=True,
                stop=None,
            )
            
            response_text = ""
            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content:
                    response_text += content
            
            print(f"🤖 Bot: {response_text}")
            
            speak_response(response_text, detected_lang)
        
        except Exception as e:
            print(f"⚠️ Error: {str(e)}")
            continue

if __name__ == "__main__":
    main()
