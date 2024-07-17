from flask import Flask, request, redirect, url_for, jsonify, render_template
from flask_cors import CORS
import mysql.connector
import boto3
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
import time
import ssl
from pyngrok import ngrok, conf, installer
from xls_to_csv import run_cloudconvert_jobs
from training_v1.s3_to_db import process_and_clean_up_s3

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

# AWS S3 setup
AWS_ACCESS_KEY_ID = os.getenv('AWS_S3_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_S3_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

# Initialize the S3 client
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files_uploaded_successfully = True
        file_renames = {
            'balSheet': 'balSheet.xlsx',
            'incStatement': 'incStatement.xlsx',
            'cfStatement': 'cfStatement.xlsx'
        }
        for file_key in file_renames:
            file = request.files.get(file_key)
            if not file or file.filename == '':
                files_uploaded_successfully = False
                return f"{file_key} is missing or no file selected", 400

            if file:
                filename = secure_filename(file_renames[file_key])

                try:
                    s3_client.upload_fileobj(file, S3_BUCKET_NAME, filename)
                    print(f"{filename} uploaded to S3 bucket {S3_BUCKET_NAME}")
                except Exception as e:
                    files_uploaded_successfully = False
                    print(f"Failed to upload {filename} to S3 bucket. Error: {e}")
                    return "File upload to S3 failed", 500

        # If all files were uploaded successfully, run the CloudConvert job
        if files_uploaded_successfully:
            run_cloudconvert_jobs()
            time.sleep(5)
            process_and_clean_up_s3()

        return redirect(url_for('upload_file'))
    
    return render_template('s3_upload.html')

@app.route('/get-latest-report', methods=['GET'])
def get_latest_report():
    # Database connection and query logic
    # Make sure to adjust this part with your actual database connection
    conn = mysql.connector.connect(user=os.getenv('AWS_DB_USER'), password=os.getenv('AWS_DB_PASSWORD'), host=os.getenv('AWS_DB_HOST'), database=os.getenv('AWS_DATABASE'))
    cursor = conn.cursor()
    query = "SELECT incStatement, balSheet, cfStatement FROM csvReports.reports ORDER BY _createdDate DESC LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        return jsonify({
            'incStatement': result[0],
            'balSheet': result[1],
            'cfStatement': result[2]
        })
    else:
        return jsonify({'error': 'No data found'}), 404

def send_response(status_code, data=None, message=None):
    response = {
        'status': 'success' if status_code == 200 else 'error',
        'data': data,
        'message': message
    }
    return jsonify(response), status_code


if __name__ == '__main__':
    app.run(debug=True)
