# llm_client.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")  

if not API_KEY:
    raise RuntimeError("Please set LLM_API_KEY in your .env file")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def call_llm(prompt: str, max_tokens: int = 800, temperature: float = 0.0):
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
    )
    return {"output_text": response.text}
