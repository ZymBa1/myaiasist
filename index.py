from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# Пароль для доступа к твоему API
SECRET_TOKEN = "XaiAPI_X4A2I0" 

class ChatData(BaseModel):
    prompt: str
    model: str

@app.post("/ask")
async def ask_ai(data: ChatData, x_app_token: str = Header(None)):
    # Проверяем, что запрос пришел именно от твоего приложения
    if x_app_token != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Access Denied")

    # Ключ Gemini берем из настроек Vercel (Environment Variables)
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    try:
        model = genai.GenerativeModel(data.model)
        response = model.generate_content(data.prompt)
        return {"answer": response.text}
    except Exception as e:
        return {"error": str(e)}
