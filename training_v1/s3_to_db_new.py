import csv
import os
import pandas as pd
import ast
import requests
import mysql.connector
import boto3
import botocore
from io import StringIO
import uuid
import due_diligence_algorithm

from openai import OpenAI
import csv_to_dataframe
from dotenv import load_dotenv

load_dotenv()

# AWS S3 setup
AWS_ACCESS_KEY_ID = os.getenv('AWS_S3_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_S3_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Initialize the OpenAI client with your API key
client = OpenAI()
client.api_key = os.getenv('OPENAI_API_KEY')

# File paths
balance_sheet_file = 'balance_sheet.csv'
income_statement_file = 'income_statement.csv'
cash_flow_statement_file = 'cash_flow_statement.csv'

# Document file names to be processed
documents = {
    'balSheet': 'balSheet.csv',
    'cfStatement': 'cfStatement.csv',
    'incStatement': 'incStatement.csv',
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

def csv_to_single_line(bucket_name, file_name):
        """Convert a CSV file from S3 to a single line of text."""
        csv_file = download_file_from_s3(bucket_name, file_name)
        reader = csv.reader(csv_file)
        single_line = ' '.join([' '.join(row) for row in reader])
        return single_line


# Call the method which converts the Csv file to dataframe. For this use method from csv_to_dataframe.py and it returns the filename
all_sheets_formatted_output = csv_to_dataframe.ProcessAllSheets(balance_sheet_file,income_statement_file,cash_flow_statement_file)

# Function to read and parse the text file
def load_financial_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    
    # Split the data into individual dictionary strings
    dict_strings = data.strip().split('\n\n')
    
    # Parse each dictionary string into a dictionary
    data_dicts = [ast.literal_eval(d) for d in dict_strings]
    
    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(data_dicts)
    return df

data = load_financial_data(all_sheets_formatted_output)


#TODO: all_sheets_formatted_output will be file name .load this file and send it to the next step perform analysis. ALso instead of filenam.. we could actually send the data directly from the csv_to_dataframe.py 

#now send the output dataframes to the algorithm to do further calculations
def perform_analysis(data):
    # Call all individual analysis methods
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

    # Store results in a dictionary
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

analysis_results = perform_analysis(data)


def get_economic_indicators():
    api_key = os.getenv('FINANCIAL_MODELING_PREP_API_KEY')
    base_url = "https://financialmodelingprep.com/api/v3"

    try:
        # Expanded economic indicators
        gdp_url = f"{base_url}/gdp?apikey={api_key}"
        unemployment_rate_url = f"{base_url}/historical-unemployment-rate?apikey={api_key}"
        inflation_rate_url = f"{base_url}/inflation-rate?apikey={api_key}"
        interest_rate_url = f"{base_url}/historical-interest-rate?apikey={api_key}"
        sector_performance_url = f"{base_url}/sector-performance?apikey={api_key}"
        consumer_confidence_url = f"{base_url}/consumer-confidence?apikey={api_key}"
        manufacturing_pmi_url = f"{base_url}/manufacturing-pmi?apikey={api_key}"
        
        # Fetching data
        gdp_data = requests.get(gdp_url).json()
        unemployment_rate_data = requests.get(unemployment_rate_url).json()
        inflation_rate_data = requests.get(inflation_rate_url).json()
        interest_rate_data = requests.get(interest_rate_url).json()
        sector_performance_data = requests.get(sector_performance_url).json()
        consumer_confidence_data = requests.get(consumer_confidence_url).json()
        manufacturing_pmi_data = requests.get(manufacturing_pmi_url).json()

        economic_indicators = {
            "GDP": gdp_data,
            "Unemployment Rate": unemployment_rate_data,
            "Inflation Rate": inflation_rate_data,
            "Interest Rate": interest_rate_data,
            "Sector Performance": sector_performance_data,
            "Consumer Confidence": consumer_confidence_data,
            "Manufacturing PMI": manufacturing_pmi_data,
        }
        return economic_indicators
    except Exception as e:
        print(f"An error occurred while fetching economic indicators: {e}")
        return None
    

economic_indicators = get_economic_indicators()

#Now send this to llm and get the response 
user_message_content = f"Generate a structured and comprehensive due-diligence report suitable for finance professionals (at least 2000 words), for the following company, following this provided format:\n\n" \
        f"1. Executive Summary (200 words): Provide an overview of the company, including a summary of key findings from the due-diligence analysis. Highlight the primary opportunities and risks associated with the company, with a brief mention of the economic indicators that could impact the company's performance. For instance, GDP growth at {economic_indicators['GDP']}%, Unemployment Rate at {economic_indicators['Unemployment Rate']}%, and Inflation Rate at {economic_indicators['Inflation Rate']}%.\n" \
        "2. Company Overview (400 words): Detail the company's history, business model, core products or services, market positioning, and how economic trends may impact its operations or sector. Consider the interest rates currently at " + f"{economic_indicators['Interest Rate']}%" + ", affecting financing and investment decisions.\n" \
        "3. Financial Analysis (400 words): Evaluate the company's financial health by analyzing the income statement, balance sheet, and cash flow statement. Discuss liquidity, solvency, profitability, and operating efficiency. Highlight the economic context by mentioning relevant indicators, such as GDP growth at " + f"{economic_indicators['GDP']}%" + " and inflation rates at " + f"{economic_indicators['Inflation Rate']}%" + ", to provide context to the financial analysis.\n" \
        "4. Market and Competitor Analysis (600 words): Analyze the company's market share, competitive landscape, and industry trends. Assess how the company is positioned relative to its competitors and how broader economic indicators like sector performance at " + f"{economic_indicators['Sector Performance']}" + " and consumer confidence at " + f"{economic_indicators['Consumer Confidence']}" + " may influence the market landscape.\n" \
        "5. Risk Assessment (600 words): Identify and evaluate potential risks, including market risks, operational risks, legal risks, and financial risks. Discuss how external economic factors, such as changes in the Manufacturing PMI at " + f"{economic_indicators['Manufacturing PMI']}" + " or unemployment rates at " + f"{economic_indicators['Unemployment Rate']}%" + ", could impact these risk factors.\n" \
        "6. Legal and Compliance Review (300 words): Overview of the company's legal standings, regulatory compliance issues, and any ongoing litigations. Consider the impact of economic policies and regulations on compliance requirements, reflecting on how changes in economic indicators influence legal landscapes.\n" \
        "7. Management and Governance (300 words): Analyze the company's leadership, corporate governance practices, and any noteworthy executive decisions or changes. Reflect on how economic trends could influence management strategies and governance practices, considering the broader economic indicators provided.\n\n" \
        "All the sections should collectively present a comprehensive analysis, expanding on the key points highlighted in the executive summary.\n" \
        "Make extensive use of the following data to construct the report. This information will provide a backdrop for understanding the company's financial health, market position, and potential risks, offering a holistic view of its current status and future prospects.\n\n" \

# user_message_content += f"analysis_results: {analysis_results}\n\n"

# Convert CSV files to single-line text and prepare data for database insertion
data_to_insert = []
for doc_key, filename in documents.items():
    single_line_text = csv_to_single_line(S3_BUCKET_NAME, filename)
    data_to_insert.append(single_line_text)

# Generate the chat completion
response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a highly advanced due-diligence research bot that generates report-style due-diligence analyses using the user-provided financial data, with each section being intricate and detailed."},
            {"role": "user", "content": user_message_content}
        ],
        temperature=1,
        max_tokens=4095,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Check the response and render the report using a template
if response.choices:
    report_content = response.choices[0].message.content.strip()
#      return render_template('dd_analysis.html', economic_indicators=economic_indicators, income_statement_text=income_statement_text, balance_sheet_text=balance_sheet_text, cash_flow_statement_text=cash_flow_statement_text, report_content=report_content)
# else:
#     return send_response(500, message="No choices in the response")
