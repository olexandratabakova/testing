import json
from utils.ollama_response import model_response_simple, model_response_poetry
from tqdm import tqdm

def process_text_chunks(file_path, chunk_size=2400):
    #for txt
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     data = file.read().replace('\n', ' ')
    # chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # print(data['songs'][1]['lyrics'])

    #for json
    with open(file_path, "r", encoding="utf-8") as r:
        data = json.load(r)

    songs = data["songs"]
    all_relations = []

    for i, song in enumerate(tqdm(songs, desc="Processing songs")):
        lyrics = song["lyrics"]
        title = song.get("title", f"song_{i + 1}")
        year = song.get("year")
        date = song.get("date")
        parsed = model_response_poetry(lyrics)
        relations = parsed.model_dump()

        for rel in relations:
            rel["song_title"] = title
            rel["song_year"] = year
            rel["song_date"] = date
        all_relations.extend(relations)

        with open("texts_result/relations_ver3.json", "w", encoding="utf-8") as f:
            json.dump(all_relations, f, indent=2, ensure_ascii=False)

#relation - 29/29
#relation_ver2 - 18/29
