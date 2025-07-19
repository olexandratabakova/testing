from ollama import chat
from relation import *
from db.schema import insert_chunk

def model_responses(chunk):
    prompt = (
        f"Extract all meaningful connections between people with specific surnames from the text.\n"
        f"For each connection, output a JSON object with:\n"
        f"person1: short description (up to 3 words)\n"
        f"person2: short description (up to 3 words)\n"
        f"relation_type: one of ['command', 'support', 'conflict', 'cooperation', 'association', 'unknown']\n"
        f"polarity: one of ['positive', 'negative', 'neutral']\n"
        f"keywords: list of up to 5 important keywords summarizing the connection\n"
        f"Text: {chunk}"
    )

    response = chat(
        model='llama3.1:8b',
        messages=[{
            "role": "user",
            "content": prompt
        }],
        format=RelationList.model_json_schema()
    )
    return RelationList.model_validate_json(response.message.content)