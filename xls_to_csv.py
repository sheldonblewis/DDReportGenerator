import requests
import os
from dotenv import load_dotenv

def run_cloudconvert_jobs():
    load_dotenv()

    API_KEY = os.getenv('CLOUDCONVERT_API_KEY')
    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-type": "application/json",
    }

    # List of document file names to be processed
    documents = ['balSheet.xlsx', 'incStatement.xlsx', 'cfStatement.xlsx']

    def create_cloudconvert_job(file_name):
        sanitized_file_name = file_name.replace('.', '_')
        aws_s3_region = os.getenv('AWS_S3_REGION')
        # Configure S3 paths for import and export
        s3_import_key = file_name
        s3_export_key = file_name.replace('.xlsx', '.csv')

        # Import from S3 task configuration
        s3_import_config = {
            "operation": "import/s3",
            "access_key_id": os.getenv('AWS_S3_ACCESS_KEY_ID'),
            "secret_access_key": os.getenv('AWS_S3_SECRET_ACCESS_KEY'),
            "bucket": os.getenv('S3_BUCKET_NAME'),
            "region": aws_s3_region,
            "key": s3_import_key,
        }

        # Convert task configuration
        convert_task_config = {
            "operation": "convert",
            "input_format": "xlsx",
            "output_format": "csv",
            "engine": "libreoffice",
            "input": f"import_my_file_{sanitized_file_name}",
        }

        # Export to S3 task configuration
        s3_export_config = {
            "operation": "export/s3",
            "input": f"convert_my_file_{sanitized_file_name}",
            "access_key_id": os.getenv('AWS_S3_ACCESS_KEY_ID'),
            "secret_access_key": os.getenv('AWS_S3_SECRET_ACCESS_KEY'),
            "bucket": os.getenv('S3_BUCKET_NAME'),
            "region": aws_s3_region,
            "key": s3_export_key,
        }

        # Combine tasks into a job payload
        job_payload = {
            "tasks": {
                f"import_my_file_{sanitized_file_name}": s3_import_config,
                f"convert_my_file_{sanitized_file_name}": convert_task_config,
                f"export_my_file_{sanitized_file_name}": s3_export_config,
            }
        }

        response = requests.post("https://api.cloudconvert.com/v2/jobs", headers=HEADERS, json=job_payload)

        if response.status_code == 200:
            print(f"Job for {file_name} created successfully.")
            print(response.json())
        else:
            print(f"Failed to create job for {file_name}.")
            print(response.text)

    # Process each document
    for document in documents:
        print(f"Processing conversion for {document}")
        create_cloudconvert_job(document)

if __name__ == '__main__':
    run_cloudconvert_jobs()