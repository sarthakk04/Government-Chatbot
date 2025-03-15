import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyBIZJ2LO9dPdu7sAtI_NdEgOg_pNqaRNm0")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Consider your self as a person who knows every laws of Maharashtra and if any query is asked related to that then you should answer it\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Understood.  Ask me your Maharashtra law-related queries.  I'll do my best to answer them accurately and informatively, drawing on my knowledge of the Maharashtra legal landscape.  Please keep in mind that I am an AI and cannot offer legal advice.  My responses are for informational purposes only and should not be substituted for the guidance of a qualified legal professional.  If you require legal advice, please consult with a lawyer practicing in Maharashtra.\n",
      ],
    },
  ]
)

# response = chat_session.send_message("INSERT_INPUT_HERE")
response = chat_session.send_message("पोट हिस्सा मोजणी साठी कोणती कागदपत्रे आवश्यक असतात..हद्दकायम  सहधारका ची संमती आवश्यक आहे का")

print(response.text)