import os
import fitz
import sqlite3
import spacy  # Import spaCy
from langchain.text_splitter import SpacyTextSplitter
import re

# Get the directory of the script and then access the "pdfs" directory
pdf_directory = os.path.join(os.path.dirname(__file__), 'pdfs/')

# Connect to the SQLite database (create it if it doesn't exist)
conn = sqlite3.connect('my_chunks3.db')
cursor = conn.cursor()

CTR = 100

pdf_files = os.listdir(pdf_directory)

# Create the chunks_fact table if it doesn't exist
create_table_sql = '''
CREATE TABLE IF NOT EXISTS chunks_fact (
    chunk_id INTEGER PRIMARY KEY,
    chunk_text TEXT,
    page_number INTEGER,
    document_file_name TEXT,
    case_date TEXT
)
'''
cursor.execute(create_table_sql)

# Load a spaCy model for English
nlp = spacy.load("en_core_web_sm")

# Initialize the SpacyTextSplitter
text_splitter = SpacyTextSplitter(chunk_size=400, chunk_overlap=50, pipeline="en_core_web_sm")

CTR += 1
def extract_date_from_chunk(chunk_text):
    # Use regular expression to find date patterns in the chunk text
    date_pattern = r'\b(\d{1,2}\s[a-zA-Z]+\,\s\d{4})\b'
    matches = re.findall(date_pattern, chunk_text)
    if matches:
        return matches[0]  # Return the first match as the date
    else:
        return None  # Return None if no date is found
# Iterate over PDF files in the directory
for each_file in pdf_files:
    try:
        print("Parsing from the pdf files....", each_file)
        pdf_doc = fitz.open(pdf_directory + each_file)
        doc_chunks = []
        num_pages = pdf_doc.page_count
        print("Total number of pages.. ", num_pages)
        for page_num in range(num_pages):
            print("Reading page....", page_num)
            try:
                current_page = pdf_doc.load_page(page_num).get_text()
                chunks = text_splitter.split_text(str(current_page))
                print("Total chunks...", len(chunks))
                for each_chunk in range(len(chunks)):
                    date = extract_date_from_chunk(str(chunks[each_chunk]))
                    if date:
                        dict_temp = {'chunk_id': CTR,
                                     'chunk_text': str(chunks[each_chunk]),
                                     'page_number': page_num,
                                     'document_file_name': each_file,
                                     'case_date': date}
                        cursor.execute(
                            "INSERT INTO chunks_fact (chunk_id,chunk_text,page_number,document_file_name,case_date) VALUES (?,?,?,?,?)",
                            (CTR, str(chunks[each_chunk]), page_num, each_file, date))
                        conn.commit()
                        CTR += 1
            except Exception as e:
                print(f"Exception occurred: {e}")
    except Exception as e:
        print(f"Exception occurred: {e}")

# Commit the changes and close the database connection
conn.close()



