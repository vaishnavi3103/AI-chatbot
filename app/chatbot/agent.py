import json
from datetime import datetime

from app.chatbot.prompts import SYSTEM_PROMPT
from app.chatbot.tools import TOOLS
from app.services.open_ai_service import chat_completion
from app.db.mongo import hr_collection, project_collection, chat_history
from app.utils.chat_memory import get_chat_history


def chat_with_agent(user_message: str, session_id: str | None):

    # -----------------------------------
    # Base system prompt
    # -----------------------------------
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    # -----------------------------------
    # Load chat history (if session exists)
    # -----------------------------------
    if session_id:
        history = get_chat_history(session_id)
        messages.extend(history)

    # -----------------------------------
    # Current user message
    # -----------------------------------
    messages.append(
        {"role": "user", "content": user_message}
    )

    # -----------------------------------
    # FIRST MODEL CALL (intent detection)
    # -----------------------------------
    response = chat_completion(messages, TOOLS)
    model_message = response.choices[0].message

    # -----------------------------------
    # TOOL CALL FLOW
    # -----------------------------------
    if model_message.tool_calls:

        tool_call = model_message.tool_calls[0]

        try:
            args = json.loads(tool_call.function.arguments)
        except Exception:
            return {
                "response": "Sorry, I could not understand your request.",
                "session_id": session_id
            }

        source = args.get("source")        # "hr" or "project"
        record_id = args.get("id")         # employee_id / project_id
        name = args.get("name")            # employee_name / project_name

        record = None

        # -----------------------------------
        # HR DATA (employee_id / name)
        # -----------------------------------
        if source == "hr":
            if record_id is not None:
                record = hr_collection.find_one(
                    {"employee_id": record_id},
                    {"_id": 0}
                )
            elif name:
                record = hr_collection.find_one(
                    {"name": {"$regex": f"^{name}$", "$options": "i"}},
                    {"_id": 0}
                )

        # -----------------------------------
        # PROJECT DATA (project_id / project_name)
        # -----------------------------------
        elif source == "project":
            if record_id is not None:
                record = project_collection.find_one(
                    {"project_id": int(record_id)},
                    {"_id": 0}
                )
            elif name:
                record = project_collection.find_one(
                    {"project_name": {"$regex": f"^{name}$", "$options": "i"}},
                    {"_id": 0}
                )

        # -----------------------------------
        # TOOL RESULT (structured & safe)
        # -----------------------------------
        tool_result = {
            "status": "success" if record else "not_found",
            "source": source,
            "data": record
        }

        # -----------------------------------
        # Send tool call + tool result to model
        # -----------------------------------
        messages.append(model_message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result)
        })

        # -----------------------------------
        # FINAL MODEL RESPONSE
        # -----------------------------------
        final_response = chat_completion(messages, TOOLS)
        answer = (
            final_response.choices[0].message.content
            or "Here is the requested information."
        )

    # -----------------------------------
    # NORMAL CHAT (no tool needed)
    # -----------------------------------
    else:
        answer = model_message.content

    # -----------------------------------
    # STORE CHAT HISTORY
    # -----------------------------------
    if session_id:
        chat_history.insert_many([
            {
                "session_id": session_id,
                "role": "user",
                "content": user_message,
                "timestamp": datetime.utcnow()
            },
            {
                "session_id": session_id,
                "role": "assistant",
                "content": answer,
                "timestamp": datetime.utcnow()
            }
        ])

    return {
        "response": answer,
        "session_id": session_id
    }
