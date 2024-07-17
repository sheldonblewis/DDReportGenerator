import subprocess

# Start the s3_upload.py script
s3_upload_process = subprocess.Popen(['python', 's3_upload.py'])

# Start the dd_prod_gpt4_vanilla.py script
dd_prod_gpt4_vanilla_process = subprocess.Popen(['python', 'dd_prod_gpt4_vanilla.py'])

# Wait for both processes to complete
s3_upload_process.wait()
dd_prod_gpt4_vanilla_process.wait()