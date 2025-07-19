from analyse_document import process_text_chunks
from db.schema import *

init_db()

file_path = "text.txt"
insert_document(file_path)

process_text_chunks(file_path)
print("Response has been written.")
