# import json
from ollama_response import model_responses
from tqdm import tqdm
from db.schema import *

file_path = "text.txt"
insert_document(file_path)
def process_text_chunks(file_path, chunk_size=2400):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read().replace('\n', ' ')

    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    all_relations = []

    for chunk in tqdm(chunks, desc="Processing chunks"):
        parsed = model_responses(chunk)
        all_relations.extend(parsed.model_dump())


    # with open("relations.json", "w", encoding='utf-8') as f:
    #     json.dump(all_relations, f, indent=2, ensure_ascii=False)


