from ollama import chat
from schemas.relation_simple import *
from schemas.relation_poetry import *


model = "llama3.1:8b"

prompt_TheBeatles = (f"""Hello
                        """)
def model_response_simple(chunk):
    prompt = (
        # f"""
        # Analyze the song lyrics and extract semantic connections.
        # For each connection, output a JSON object with:
        # node1: lexeme, image, or symbol
        # node2: lexeme, image, or symbol
        # relation_type: one of ['co-occurrence', 'context', 'shared_line']
        # lines: list of line numbers where the connection occurs
        # keywords: up to 5 significant terms related to the connection
        # Text: {chunk}
        # """
        f"Extract all meaningful connections between people with specific surnames from the text.\n"
        f"For each connection, output a JSON object with:\n"
        f"person1: short description (up to 3 words)\n"
        f"person2: short description (up to 3 words)\n"
        f"relation_type: one of ['command', 'support', 'conflict', 'cooperation', 'association', 'unknown']\n"
        f"polarity: one of ['positive', 'negative', 'neutral']\n"
        f"Text: {chunk}"
    )

    response = chat(
        model="llama3.1:8b",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        format=RelationList.model_json_schema()
    )
    return RelationList.model_validate_json(response.message.content)

def model_response_poetry(chunk):
    prompt = (
        f"""
        Analyze the song lyrics and extract semantic connections.
        For each connection, output a JSON object with:
        node1: lexeme, image, or symbol
        node2: lexeme, image, or symbol
        relation_type: one of ['co-occurrence', 'context']
        topic_terms: up to 5 words that characterize the context of this connection
        typical_lexicon: list of up to 15 words frequently co-occurring with this pair
        Text: {chunk}
        """
    )

    response = chat(
        model="llama3.1:8b",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        format=RelationListPoetry.model_json_schema()
    )
    return RelationListPoetry.model_validate_json(response.message.content)