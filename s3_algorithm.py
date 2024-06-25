import dotenv
import pdfminer.high_level
import os
import boto3
import botocore
import due_diligence_algorithm
import csv_to_dataframe

dotenv.load_dotenv()

# AWS S3 setup
AWS_ACCESS_KEY_ID = os.getenv('AWS_S3_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_S3_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def get_most_recent_file(bucket_name, prefix):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        files = response.get('Contents', [])
        if not files:
            raise FileNotFoundError(f"No files found with prefix {prefix} in bucket {bucket_name}")
        most_recent_file = max(files, key=lambda x: x['LastModified'])
        return most_recent_file['Key']
    except botocore.exceptions.ClientError as e:
        raise e

def download_file_from_s3(bucket_name, file_name):
    try:
        print(f"Attempting to download {file_name} from bucket {bucket_name}")
        file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        s3_client.download_file(S3_BUCKET_NAME,file_name,file_name)

        return file_name
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            raise FileNotFoundError(f"The file {file_name} does not exist in the bucket {bucket_name}.")
        else:
            raise
    except Exception as e:
        raise ValueError(f"Failed to decode the file {file_name}. Error: {str(e)}")

def load_financial_data():
    balance_sheet_key = get_most_recent_file(S3_BUCKET_NAME, 'balSheet')
    income_statement_key = get_most_recent_file(S3_BUCKET_NAME, 'incStatement')
    cash_flow_statement_key = get_most_recent_file(S3_BUCKET_NAME, 'cfStatement')

    balance_sheet_filepath = download_file_from_s3(S3_BUCKET_NAME, balance_sheet_key)
    income_statement_filepath = download_file_from_s3(S3_BUCKET_NAME, income_statement_key)
    cash_flow_statement_filepath = download_file_from_s3(S3_BUCKET_NAME, cash_flow_statement_key)
    balance_sheet_filepath = 'balSheet.csv'
    income_statement_filepath = 'incStatement.csv'
    cash_flow_statement_filepath = 'cfStatement.csv'

    # Assuming csv_to_dataframe.ProcessAllSheets is a function that processes these files
    all_sheets_formatted_dataframe = csv_to_dataframe.ProcessAllSheets(balance_sheet_filepath, income_statement_filepath, cash_flow_statement_filepath)

    return all_sheets_formatted_dataframe

def load_extract_cim_data():
    cim_file_name = 'cimFile.pdf'
    cim_file_name = get_most_recent_file(S3_BUCKET_NAME, 'cimFile')
    cim_filepath = download_file_from_s3(S3_BUCKET_NAME, cim_file_name)
    text = ""
    images = []

    try:
        text = pdfminer.high_level.extract_text(cim_filepath)
        # doc = fitz.open(cim_filepath)
        # for page_num in range(doc.page_count):
        #     page = doc.load_page(page_num)
        #     text += page.get_text("text")
                
            # image_list = page.get_images(full=True)
            # for img_index, img in enumerate(image_list):
            #     xref = img[0]
            #     base_image = doc.extract_image(xref)
            #     image_bytes = base_image["image"]
            #     image = Image.open(io.BytesIO(image_bytes))
            #     images.append(image)
        # return text, images
        return text
    except:
        text = ""
        return text




def perform_analysis(data):
    gross_profit_margin = due_diligence_algorithm.calculate_gross_profit_margin(data)
    net_profit_margin = due_diligence_algorithm.calculate_net_profit_margin(data)
    operating_income_margin = due_diligence_algorithm.calculate_operating_income_margin(data)
    operating_expenses_ratio = due_diligence_algorithm.calculate_operating_expenses_ratio(data)
    current_ratio = due_diligence_algorithm.calculate_current_ratio(data)
    debt_ratio = due_diligence_algorithm.calculate_debt_ratio(data)
    debt_to_equity_ratio = due_diligence_algorithm.calculate_debt_to_equity_ratio(data)
    interest_coverage_ratio = due_diligence_algorithm.calculate_interest_coverage_ratio(data)
    asset_turnover_ratio = due_diligence_algorithm.calculate_asset_turnover_ratio(data)
    inventory_turnover_ratio = due_diligence_algorithm.calculate_inventory_turnover_ratio(data)
    cash_conversion_cycle = due_diligence_algorithm.calculate_cash_conversion_cycle(data)
    quick_ratio = due_diligence_algorithm.calculate_quick_ratio(data)
    return_on_assets = due_diligence_algorithm.calculate_return_on_assets(data)
    return_on_equity = due_diligence_algorithm.calculate_return_on_equity(data)
    operating_cash_flows_ratio = due_diligence_algorithm.calculate_operating_cash_flows_ratio(data)
    cash_flow_to_net_income = due_diligence_algorithm.calculate_cash_flow_to_net_income(data)
    current_liability_coverage = due_diligence_algorithm.calculate_current_liability_coverage(data)

    analysis_results = {
        'gross_profit_margin': gross_profit_margin,
        'net_profit_margin': net_profit_margin,
        'operating_income_margin': operating_income_margin,
        'operating_expenses_ratio': operating_expenses_ratio,
        'current_ratio': current_ratio,
        'debt_ratio': debt_ratio,
        'debt_to_equity_ratio': debt_to_equity_ratio,
        'interest_coverage_ratio': interest_coverage_ratio,
        'asset_turnover_ratio': asset_turnover_ratio,
        'inventory_turnover_ratio': inventory_turnover_ratio,
        'cash_conversion_cycle': cash_conversion_cycle,
        'quick_ratio': quick_ratio,
        'return_on_assets': return_on_assets,
        'return_on_equity': return_on_equity,
        'operating_cash_flows_ratio': operating_cash_flows_ratio,
        'cash_flow_to_net_income': cash_flow_to_net_income,
        'current_liability_coverage': current_liability_coverage
    }
    return analysis_results

def process_and_clean_up_s3():
    data = load_financial_data()
    cimtext = load_extract_cim_data()
    analysis_results = perform_analysis(data)
    return cimtext, analysis_results
