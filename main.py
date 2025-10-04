from utils.analyse_document import process_text_chunks

# init_db()

file_path = "text_for_analysis/songs_TheBeatles.json"
# insert_document(file_path)

process_text_chunks(file_path)
print("Response has been written.")

