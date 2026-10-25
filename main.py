import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import errors

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
        except errors.ServerError:
            # 503 "high demand" jaisi temporary error par wait karke retry
            time.sleep(2 ** attempt)
        except errors.ClientError as e:
            # 404 (model nahi mila), 400 (galat request), 403 (key), 429 (quota)
            # ke liye retry ka fayda nahi, seedha error bhejo
            raise HTTPException(status_code=502, detail=f"Gemini error: {e}")
    raise HTTPException(
        status_code=503,
        detail="Abhi server par zyada demand hai. Thodi der baad dobara try karein.",
    )

@app.post("/chat")
def chat(req: ChatRequest):
    reply = ask_gemini(req.message)
    return {"reply": reply}
