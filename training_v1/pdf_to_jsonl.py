import os
import json
import pandas as pd
from pdfminer.high_level import extract_text
from dotenv import load_dotenv


load_dotenv()
# Directories
pdfs_directory = os.getenv('PDFS_DIRECTORY')
jsonl_directory = os.getenv('JSONL_DIRECTORY')
excel_file_path = os.getenv('EXCEL_FILE_PATH')

# Make sure the JSONL directory exists
os.makedirs(jsonl_directory, exist_ok=True)
combined_jsonl_file_path = os.path.join(jsonl_directory, 'research_articles.jsonl')

# Read the Excel file to map PDF names to their corresponding ticker
df = pd.read_excel(excel_file_path)
pdf_to_ticker_map = dict(zip(df['Article'], df['Company']))

# Iterate over all PDF files in the directory
for pdf_file in os.listdir(pdfs_directory):
    if pdf_file.endswith('.pdf'):
        pdf_file_path = os.path.join(pdfs_directory, pdf_file)
        text = extract_text(pdf_file_path)
        
        ticker = pdf_to_ticker_map.get(pdf_file, "UNKNOWN")

        json_record = json.dumps({
            "messages": [
                {"role": "system", "content": "A report-style equity analysis is produced per ticker."},
                {"role": "user", "content": ticker},
                {"role": "assistant", "content": text.strip()}
            ]
        }, ensure_ascii=False)

        # Write the JSON object to the .jsonl file
        with open(combined_jsonl_file_path, 'a', encoding='utf-8') as jsonl_file:
            jsonl_file.write(json_record + "\n")

print(f"JSON Lines file created at {combined_jsonl_file_path}.")
