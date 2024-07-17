from dotenv import load_dotenv
import os
from openai import OpenAI
import excel_to_jsonl as ej

load_dotenv()

client = OpenAI()
client.api_key = os.getenv('OPENAI_API_KEY')

client.files.create(
    file=open(ej.jsonl_file_path, "rb"),
    purpose="fine-tune"
)