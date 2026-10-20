from fastapi import FastAPI
from pydantic import BaseModel
import anthropic

app = FastAPI()
client = anthropic.Anthropic()

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": req.message}],
    )
    text = "".join(b.text for b in response.content if b.type == "text")
    return {"reply": text}
