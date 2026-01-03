from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from app.chatbot.agent import chat_with_agent
from app.db.mongo import chat_history

load_dotenv()

app = FastAPI()



@app.get("/history/{session_id}")
def get_history(session_id: str):
    chats = list(
        chat_history.find(
            {"session_id": session_id},
            {"_id": 0}
        ).sort("timestamp", 1)
    )

    return {
        "session_id": session_id,
        "messages": chats
    }



class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@app.post("/chat")
def chat(req: ChatRequest):
    return chat_with_agent(req.message, req.session_id)