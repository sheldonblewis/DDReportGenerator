from flask import Flask, request, redirect, url_for, jsonify, render_template
from flask_cors import CORS
from pyngrok import ngrok, conf, installer
from werkzeug.utils import secure_filename
from xls_to_csv import run_cloudconvert_jobs
from dotenv import load_dotenv
from s3_algorithm import process_and_clean_up_s3
import dd_prod_gpt4_vanilla
import boto3
import mysql.connector
import os
import requests
import ssl
import time

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

def notify_backend(most_recent_files):
    url = "http://localhost:5000/get-latest-report"  # URL to your backend endpoint
    response = requests.post(url, json=most_recent_files)
    if response.status_code == 200:
        print("Backend notified successfully.")
    else:
        print("Failed to notify backend.")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files_uploaded_successfully = True
        file_renames = {
            'balSheet': 'balSheet.xlsx',
            'incStatement': 'incStatement.xlsx',
            'cfStatement': 'cfStatement.xlsx',
            'cimFile': 'cimFile.pdf'
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
            cim_text, alg_results = process_and_clean_up_s3()
            cim_summary = dd_prod_gpt4_vanilla.extract_cim_relevant_text(cim_text)
            print(dd_prod_gpt4_vanilla.generate_economic_report(cim_summary, alg_results))
            # db_config = {
            #     'user': os.getenv('AWS_DB_USER'),
            #     'password': os.getenv('AWS_DB_PASSWORD'),
            #     'host': os.getenv('AWS_DB_HOST'),
            #     'database': os.getenv('AWS_DATABASE'),
            # }

        return redirect(url_for('upload_file'))
    
    return render_template('s3_upload.html')

@app.route('/get-latest-report', methods=['GET'])
def get_latest_report():
    # Database connection and query logic
    # Make sure to adjust this part with your actual database connection
    conn = mysql.connector.connect(user=os.getenv('AWS_DB_USER'), password=os.getenv('AWS_DB_PASSWORD'), host=os.getenv('AWS_DB_HOST'), database=os.getenv('AWS_DATABASE'))
    cursor = conn.cursor()
    query = "SELECT incStatement, balSheet, cfStatement, cimFile FROM csvReports.reports ORDER BY _createdDate DESC LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        return jsonify({
            'incStatement': result[0],
            'balSheet': result[1],
            'cfStatement': result[2],
            'cimFile': result[3]
        })
    else:
        return jsonify({'error': 'No data found'}), 404

if __name__ == '__main__':
    port = 9998
    myssl = ssl.create_default_context()
    myssl.check_hostname = False
    myssl.verify_mode = ssl.CERT_NONE
    pyngrok_config = conf.get_default()
    if not os.path.exists(pyngrok_config.ngrok_path):
        installer.install_ngrok(pyngrok_config.ngrok_path, context=myssl)
    ngrok.set_auth_token(os.getenv('NGROK_AUTH_TOKEN'))
    reserved_domain = "equitary-uploads.ngrok.io"
    public_url = ngrok.connect(port, hostname=reserved_domain)
    print(f'ngrok tunnel "{public_url}" -> "http://127.0.0.1:{port}"')

    # Start the Flask app
    app.run(port=port)