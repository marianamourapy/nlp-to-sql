from llm.client_groq import client
from llm.prompts import context_resolver_prompt
from core.config import CONTEXT_RESOLVER_MODEL
from core.logger import get_logger

logger = get_logger(__name__)


def resolve_context(question: str, history: list) -> str:

    if not history:
        return question

    messages = [
        {
            "role": "system",
            "content": context_resolver_prompt()
        }
    ]

    limited_history = history[-6:]

    for msg in limited_history:
        role = str(msg.get("role", "")).strip().lower()
        content = msg.get("content")

        if role in ["user", "assistant"] and isinstance(content, str) and content.strip():
            messages.append({
                "role": role,
                "content": content
            })

    messages.append({
        "role": "user",
        "content": question
    })

    logger.debug(f"Context resolver messages: {messages}")

    response = client.chat.completions.create(
        model=CONTEXT_RESOLVER_MODEL,
        messages=messages,
        temperature=0
    )

    resolved = response.choices[0].message.content.strip()
    logger.debug(f"Resolved question: {resolved}")

    return resolved