from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

app = FastAPI()
client = genai.Client()

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    response = client.models.generate_content(
        model="gemini-3.5-flash",",
        contents=req.message,
    )
    return {"reply": response.text}
