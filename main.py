import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import errors

app = FastAPI()
client = genai.Client()

PRIMARY_MODEL = "gemini-2.5-flash"
FALLBACK_MODEL = "gemini-2.5-flash-lite"

class ChatRequest(BaseModel):
    session_id: str
    message: str

def ask_gemini(prompt: str) -> str:
    for model in [PRIMARY_MODEL, FALLBACK_MODEL]:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
                return response.text
            except errors.ServerError:
                time.sleep(2 ** attempt)
    raise HTTPException(
        status_code=503,
        detail="Abhi server par zyada demand hai. Thodi der baad dobara try karein.",
    )

@app.post("/chat")
def chat(req: ChatRequest):
    reply = ask_gemini(req.message)
    return {"reply": reply}
    
