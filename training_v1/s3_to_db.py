import csv
import os
import mysql.connector
import boto3
import botocore
from io import StringIO
import uuid
from dotenv import load_dotenv

def process_and_clean_up_s3():
    load_dotenv()

    # AWS S3 setup
    AWS_ACCESS_KEY_ID = os.getenv('AWS_S3_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_S3_SECRET_ACCESS_KEY')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    db_config = {
        'user': os.getenv('AWS_DB_USER'),
        'password': os.getenv('AWS_DB_PASSWORD'),
        'host': os.getenv('AWS_DB_HOST'),
        'database': os.getenv('AWS_DATABASE'),
    }

    def download_file_from_s3(bucket_name, file_name):
        try:
            file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_name)
            return StringIO(file_obj['Body'].read().decode('utf-8'))
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "NoSuchKey":
                print(f"The file {file_name} does not exist in the bucket {bucket_name}.")
            else:
                raise

    # csv to df conversion function
    #   call from csv_to_dataframe.py

    # df to formatted dicts conversion function
    #   create_formatted_dicts() from csv_to_dataframe.py

    # dicts link to algorithm, algorithm -> LLM

    ## may be unnecessary
    # def csv_to_single_line(bucket_name, file_name):
    #    """Convert a CSV file from S3 to a single line of text."""
    #    csv_file = download_file_from_s3(bucket_name, file_name)
    #    reader = csv.reader(csv_file)
    #    single_line = ' '.join([' '.join(row) for row in reader])
    #    return single_line

    ## may be unnecessary
    # def insert_into_database(data):
    #     """Insert processed data into the MySQL database."""
    #     try:
    #         conn = mysql.connector.connect(**db_config)
    #         cursor = conn.cursor()
    #         query = (
    #             "INSERT INTO csvReports.reports (_id, cfStatement, balSheet, incStatement) "
    #             "VALUES (%s, %s, %s, %s)"
    #         )
    #         cursor.execute(query, data)
    #         conn.commit()
    #         print(f"Inserted data into database successfully: {data[0]}")
    #     except mysql.connector.Error as err:
    #         print(f"Failed to insert data into database: {err}")
    #     finally:
    #         if conn.is_connected():
    #             cursor.close()
    #             conn.close()

    def delete_all_files_in_bucket(bucket_name):
        """Delete all files in the specified S3 bucket."""
        objects_to_delete = s3_client.list_objects_v2(Bucket=bucket_name)
        deletion_ids = [{'Key': obj['Key']} for obj in objects_to_delete.get('Contents', [])]

        if deletion_ids:
            s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': deletion_ids})
            print("Deleted all files in bucket.")
        else:
            print("No files to delete in the bucket.")

    # Document file names to be processed
    documents = {
        'balSheet': 'balSheet.csv',
        'cfStatement': 'cfStatement.csv',
        'incStatement': 'incStatement.csv',
    }

    # Unique report ID for database insertion
    unique_report_id = str(uuid.uuid4())

    # Convert CSV files to single-line text and prepare data for database insertion
    data_to_insert = [unique_report_id]
    for doc_key, filename in documents.items():
        single_line_text = csv_to_single_line(S3_BUCKET_NAME, filename)
        data_to_insert.append(single_line_text)

    # Insert the processed data into the MySQL database
    insert_into_database(tuple(data_to_insert))

    # After database operations are finished, delete all files from the S3 bucket
    delete_all_files_in_bucket(S3_BUCKET_NAME)

if __name__ == '__main__':
    process_and_clean_up_s3()