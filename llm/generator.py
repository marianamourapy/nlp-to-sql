from llm.client_groq import client
from llm.prompts import generator_system_prompt, generator_user_prompt
from core.config import SCHEMA_CONTEXT, SQL_MODEL

def generate_sql(question: str) -> str:
    response = client.chat.completions.create(
        model=SQL_MODEL,
        messages=[
            {
                "role": "system",
                "content": generator_system_prompt(SCHEMA_CONTEXT)
            },
            {
                "role": "user",
                "content": generator_user_prompt(question)
            }
        ]
    )
    return response.choices[0].message.content.strip()
