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
        Analyze the lyrics of The Beatles and identify the key semantic and symbolic patterns in their language.
        Your goal is to uncover how words, images, and symbols connect to reveal deeper themes, emotions, and worldviews.
        
        For each meaningful connection found, output a JSON object with the following fields:
        
          "node1": "core lexeme, image, or symbol",
          "node2": "related lexeme, image, or symbol",
          "relation_type": "one of ['co-occurrence', 'contextual', 'metaphoric', 'emotional_association']",
          "topic_terms": ["up to 5 words capturing the main context or theme"],
          "dominant_emotion": "main emotional tone of this connection (e.g., love, melancholy, longing, joy, surrealism, spirituality)",
          "symbolic_layer": "short description of symbolic meaning (e.g., 'freedom', 'transcendence', 'isolation', 'psychedelia')",
          "typical_lexicon": ["up to 15 words frequently co-occurring with this pair across the lyrics"]
        
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