import google.generativeai as genai
from dotenv import load_dotenv
import os

#Configuration for AI 
default_system_instruction = '''
You are a assistant, you live inside a smart glasses that has access to camera(camera implmentation not yet accessed)
'''

Safety_rating = {   
    genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE
}

load_dotenv('APIKey.env')
genai.configure(api_key=os.getenv('google_api_key'))
tool_config = {
  "function_calling_config": {
    "mode": "AUTO",
  }
}


#Sets up the initialization of the AI
model = genai.GenerativeModel('gemini-1.5-pro', safety_settings= Safety_rating,tool_config=tool_config,system_instruction=default_system_instruction)
chat = model.start_chat(enable_automatic_function_calling=True)