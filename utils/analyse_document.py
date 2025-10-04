import json
from utils.ollama_response import model_response_simple, model_response_poetry
from tqdm import tqdm
# from db.schema import *
# insert_document(file_path)
def process_text_chunks(file_path, chunk_size=2400):
    #for txt
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     data = file.read().replace('\n', ' ')
    # chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # print(data['songs'][1]['lyrics'])
    #for json
    with open(file_path, "r", encoding="utf-8") as r:
        data = json.load(r)
    songs = data['songs']
    for song in songs:
        song_lyrics = song['lyrics']

    all_relations = []

    for song in tqdm(songs, desc="Processing chunks"):
        # parsed = model_response_simple(chunk)
        # song["index"] =
        parsed = model_response_poetry(song)
        all_relations.extend(parsed.model_dump())

    with open("texts_result/relations.json", "w", encoding='utf-8') as f:
        json.dump(all_relations, f, indent=2, ensure_ascii=False)
