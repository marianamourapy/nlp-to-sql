from llm.client_groq import client
from core.config import SCHEMA_CONTEXT, CLASSIFIER_MODEL
from llm.prompts import classifier_prompt


def is_database_question(question: str) -> str:
    response = client.chat.completions.create(
        model=CLASSIFIER_MODEL,
        messages=[
            {
                "role": "system",
                "content": classifier_prompt(SCHEMA_CONTEXT)
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    result = response.choices[0].message.content.strip().upper()
    if result not in ("YES", "NO", "WRITE"):
        return "YES"  
    return result