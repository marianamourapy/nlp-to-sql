from llm.client_groq import client
from core.config import SCHEMA_CONTEXT, INTERPRETER_MODEL
from llm.prompts import interpreter_system_prompt, interpreter_user_prompt

def interpret_result(question: str, sql: str, result: list, history: list) -> str:
    messages = [
        {
            "role": "system",
            "content": interpreter_system_prompt(SCHEMA_CONTEXT)
        }
    ]

    for msg in history:
        if msg.get("role") in ["user", "assistant"] and msg.get("content"):
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
    messages.append({
        "role": "user",
        "content": interpreter_user_prompt(question, sql, result)
    })
    
    response = client.chat.completions.create(
        model = INTERPRETER_MODEL,
        messages = messages
    )
    
    return response.choices[0].message.content.strip()