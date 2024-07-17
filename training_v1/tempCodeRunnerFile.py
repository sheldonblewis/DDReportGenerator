import os
import pandas as pd
import json
from dotenv import load_dotenv
from SP500_ticker_list import ticker_symbols

load_dotenv()

excel_files_directory = os.getenv('EXCEL_FILES_DIRECTORY')
output_directory = os.getenv('OUTPUT_DIRECTORY')
output_file_name = os.getenv('OUTPUT_FILE_NAME')
column_label = os.getenv('COLUMN_LABEL')

os.makedirs(output_directory, exist_ok=True)

jsonl_file_path = os.path.join(output_directory, output_file_name)

with open(jsonl_file_path, 'w', encoding='utf-8') as jsonl_file:
    for file_name in os.listdir(excel_files_directory):
        file_path = os.path.join(excel_files_directory, file_name)
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            df = pd.read_excel(file_path, usecols=[column_label])
            text_block = '\n'.join(df[column_label].astype(str)).strip()  # Ensure no leading/trailing whitespace
            
            # Search for any S&P 500 ticker in the text block
            ticker_found = None
            for ticker in ticker_symbols:
                if ticker in text_block:
                    ticker_found = ticker
                    break
            
            if ticker_found:
                ticker = ticker_found
            else:
                ticker = 'UnknownTicker'  # Default if no ticker is found
            
            json_record = json.dumps({
                "messages": [
                    {"role": "system", "content": "A report-style equity analysis is produced per ticker."},
                    {"role": "user", "content": ticker},  # Use the found ticker
                    {"role": "assistant", "content": text_block}
                ]
            }, ensure_ascii=False)
            
            jsonl_file.write(json_record + '\n')

print(f"JSON Lines file created at {jsonl_file_path}.")
