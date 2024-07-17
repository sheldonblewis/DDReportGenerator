from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI()
client.api_key = os.getenv('OPENAI_API_KEY')

client.fine_tuning.jobs.create(
    training_file="file-cXB5CwHsH5rkUlWjEYI36JiB", 
    model="gpt-3.5-turbo"
)