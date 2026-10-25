import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai

app = FastAPI()
client = genai.Client()

MODEL = "gemini-3.8-flash"

class ChatRequest(BaseModel):
    session_id: str
    message: str

def ask_gemini(prompt: str) -> str:
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                time.sleep(2 ** attempt)
                continue
            raise HTTPException(status_code=502, detail=f"Gemini error: {e}")
    raise HTTPException(
        status_code=503,
        detail="Server par demand zyada hai, thodi der baad try karein.",
    )

@app.post("/chat")
def chat(req: ChatRequest):
    return {"reply": ask_gemini(req.message)}
