#saburii
import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import pygame
import os
import time
from langdetect import detect
from gtts import gTTS  # Import gTTS for Marathi voice output

# Google Gemini API Configuration
genai.configure(api_key="AIzaSyDZ_v2xmxY9AMMiLYLAjFOvQf4g_dL-uy4")

# Initialize Model
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

chat = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "तुम्ही स्वतःला राहुल समजा. तुम्हाला महाराष्ट्रातील सर्व कायदे आणि भू अभिलेख विभागाच्या प्रक्रिया माहित आहेत. तुम्ही योग्य, अचूक आणि संपूर्ण माहिती पुरवली पाहिजे."
            ],
        },
        {
            "role": "model",
            "parts": [
                "नमस्कार! मी राहुल, तुमचा महाराष्ट्रातील कायदे आणि भू अभिलेख तज्ज्ञ. मी तुम्हाला योग्य आणि संपूर्ण माहिती देईन."
            ],
        }
    ]
)

# Initialize pyttsx3 for English TTS
engine = pyttsx3.init()
engine.setProperty('rate', 180)

# Initialize Pygame for playing Marathi gTTS audio
pygame.mixer.init()

def detect_language(text):
    try:
        return detect(text)
    except:
        return 'en'

def listen_to_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... Speak now!")

        # Increase listening duration
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.energy_threshold = 300
        recognizer.pause_threshold = 2  # Wait longer for user to speak

        audio = recognizer.listen(source, timeout=10)  # Increased timeout

    try:
        text = recognizer.recognize_google(audio, language="mr-IN")
        lang = detect_language(text)
        return text, lang
    except sr.UnknownValueError:
        return "Could not understand audio", "en"
    except sr.RequestError:
        return "Could not request results", "en"

def get_response(text, lang):
    """Ensures Marathi response if needed"""
    if lang == "mr":
        response = chat.send_message(f"कृपया हा प्रश्न मराठीत उत्तर द्या: {text}")
    else:
        response = chat.send_message(text)

    response_text = response.text.replace("*", "").strip()
    print(f"🤖 Bot: {response_text}")
    return response_text

def speak_response(text, lang):
    """Marathi audio using gTTS, English using pyttsx3"""
    print(f"🎙️ Speaking in {lang}...")

    if lang == "mr":
        tts = gTTS(text=text, lang="mr", slow=False)
        audio_file = "response.mp3"
        tts.save(audio_file)
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.5)
        os.remove(audio_file)
    else:
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(text)
        engine.runAndWait()

def main():
    print("🤖 Chatbot is ready! Speak in English, Hindi, or Marathi.")

    while True:
        try:
            user_input, detected_lang = listen_to_speech()
            print(f"🗣️ You: {user_input} (Detected: {detected_lang})")

            if user_input.lower() in ['quit', 'exit', 'बंद', 'बंद करो']:
                print("👋 Goodbye!")
                break

            response_text = get_response(user_input, detected_lang)
            speak_response(response_text, detected_lang)

        except Exception as e:
            print(f"⚠️ Error: {str(e)}")
            continue

if __name__ == "__main__":
    main()
