from app.db.mongo import chat_history

def get_chat_history(session_id: str, limit: int = 6):
    cursor = (
        chat_history.find(
            {"session_id": session_id},
            {"_id": 0, "role": 1, "content": 1}
        )
        .sort("timestamp", -1)
        .limit(limit)
    )

    messages = list(cursor)
    messages.reverse()  # oldest → newest

    return messages