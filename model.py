import os

import google.generativeai as genai
from config import OPENAI_API_KEY, GEMINI_API_KEY


from openai import OpenAI 

class Model:
    def __init__(self):
        pass
    @staticmethod
    def google_gemini(transcript, prompt, extra=""):
       
        genai.configure(api_key="GOOGLE_GEMINI_API_KEY")
        model = genai.GenerativeModel("gemini-pro")
        try:
            response = model.generate_content(prompt + extra + transcript)
            return response.text
        except Exception as e:
            response_error = "⚠️ There is a problem with the API key or with python module."
            return response_error,e
    
    
    @staticmethod
    def openai_chatgpt(transcript, prompt, extra=""):
        client =   OpenAI(api_key="OPENAI_CHATGPT_API_KEY")
        model="Gpt-4o-mini"
        message = [{"role": "system", "content": prompt + extra + transcript}]
        try:
            response = client.chat.completions.create(model=model, messages=message)
            return response.text
        except Exception as e:
            response_error = "⚠️ There is a problem with the API key or with python module."
            return response_error,e