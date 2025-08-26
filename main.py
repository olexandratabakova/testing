from utils.analyse_document import process_text_chunks

# init_db()

file_path = "texts/text.txt"
# insert_document(file_path)

process_text_chunks(file_path)
print("Response has been written.")

