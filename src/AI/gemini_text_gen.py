import os
import google.generativeai as genai
from keys import gemini_key
from src.rate_limiter import RateLimiter

class GenerateException(Exception):
    pass

@RateLimiter(min_interval=15, max_calls=5, period=60)
def generate_text(prompt, role):
    genai.configure(api_key=gemini_key)
    
    model = genai.GenerativeModel('gemini-1.5-pro', 
                                  system_instruction=f'Ты {role}')
    
    response = model.generate_content(f"""{prompt}""")
    
    if response is None:
        raise GenerateException("Ошибка генерации")
    return response.text