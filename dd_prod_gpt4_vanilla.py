from csv_to_dataframe import ProcessAllSheets
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
from pyngrok import ngrok, conf, installer
from s3_algorithm import load_financial_data
from urllib.request import urlopen
import ast
import due_diligence_algorithm
import os
import pandas as pd
import re
import requests
import ssl

# Load environment variables
load_dotenv()

# Initialize the OpenAI client with your API key
client = openai.OpenAI()
client.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

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

def get_economic_indicators():
    api_key = os.getenv('FINANCIAL_MODELING_PREP_API_KEY')
    base_url = "https://financialmodelingprep.com/api/v4"
    base_url_v3 = "https://financialmodelingprep.com/api/v3"

    try:
        # today = datetime.now()
        # one_year_ago = today - timedelta(days=365)

        # # Format dates in 'YYYY-MM-DD' format
        # today_str = today.strftime('%Y-%m-%d')
        # one_year_ago_str = one_year_ago.strftime('%Y-%m-%d')
    
        # Expanded economic indicators
        gdp_url = f"{base_url}/economic?name=GDP&from=2023-07-01&to=2023-10-01&apikey={api_key}"
        unemployment_rate_url = f"{base_url}/economic?name=unemploymentRate&from=2023-09-01&to=2023-10-01&apikey={api_key}"
        inflation_rate_url = f"{base_url}/economic?name=inflationRate&from=2024-02-16&apikey={api_key}"
        interest_rate_url = f"{base_url}/treasury?from=2023-10-06&to=2023-10-11&apikey={api_key}"
        sector_performance_url = f"{base_url_v3}/sectors-performance?apikey={api_key}"
        consumer_confidence_url = f"{base_url}/economic?name=consumerSentiment&from=2023-12-01&apikey={api_key}"
        manufacturing_pmi_url = f"{base_url}/economic?name=industrialProductionTotalIndex&from=2023-10-01&to=2024-01-01&apikey={api_key}"

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

def extract_cim_relevant_text(cimtext):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", "content": "You are a helpful assistant capable of doing high level analysis and expert in financial study.",
                "content": [
                    {"type": "text", "text": "Extract and summarize the section related to Transaction Rationale page in less than 100 words, Highlight on statistical value."},
                    {
                        "type": "text",
                        "text": cimtext,
                    },
                ],
            }
        ],
        temperature=1,
        max_tokens=4095,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    if response.choices:
        report_content = response.choices[0].message.content.strip()
        return report_content
    else:
        return "No choices in the response"



# Flask route to get stock analysis
# @app.route('/generate_economic_report', methods=['GET'])
def generate_economic_report(cim_summary, analysis_results):
    openai.api_key = os.getenv('OPENAI_API_KEY')

    economic_indicators = get_economic_indicators()
    # analysis_results = perform_analysis(load_financial_data(ProcessAllSheets('balSheet.csv','incStatement.csv','cfStatement.csv')))
    thesis_prompt_text = request.args.get('thesis_prompt_text')

    # user_message_content = f"Generate a structured and comprehensive due-diligence report suitable for finance professionals (at least 2000 words), for the following company, following this provided format:\n\n" \
    #     f"1. Executive Summary (200 words): Provide an overview of the company, including a summary of key findings from the due-diligence analysis. Highlight the primary opportunities and risks associated with the company, with a brief mention of the economic indicators that could impact the company's performance. For instance, GDP growth at {economic_indicators['GDP']}%, Unemployment Rate at {economic_indicators['Unemployment Rate']}%, and Inflation Rate at {economic_indicators['Inflation Rate']}%.\n" \
    #     "2. Company Overview (250 words): Generate a detailed overview of the company including its founding year, founders, headquarters location, number of employees, and key business areas.\n" \
    #     "3. Financial Analysis (400 words): Summarize the last five years of the company's financial statements, including income statements, balance sheets, and cash flow statements. Identify any major financial risks or anomalies in the financial data provided. Highlight the economic context by mentioning relevant indicators, such as GDP growth at " + f"{economic_indicators['GDP']}%" + " and inflation rates at " + f"{economic_indicators['Inflation Rate']}%" + ", to provide context to the financial analysis.\n" \
    #     "4. Market and Industry Analysis (500 words): Describe the current market environment of the industry, including major competitors, market trends, and the company's market share. Evaluate the company’s competitive position and its strategy for maintaining or improving this position. Include description on how broader economic indicators like sector performance at " + f"{economic_indicators['Sector Performance']}" + " and consumer confidence at " + f"{economic_indicators['Consumer Confidence']}" + " may influence the market landscape.\n" \
    #     "5. Risk Management (500 words): Detail the risk management strategies employed by the company, including financial, operational, and strategic risk controls. Identify any operational and/or human resources-related risks that can affect the company's competitive position if possible. Discuss how external economic factors, such as changes in the Manufacturing PMI at " + f"{economic_indicators['Manufacturing PMI']}" + " or unemployment rates at " + f"{economic_indicators['Unemployment Rate']}%" + ", could impact the risk management strategies.\n" \
    #     "6. Legal Compliance (250 words): List all known legal disputes the company is currently involved in or has been involved in the past five years. Provide an analysis of compliance with relevant industry regulations and any potential legal liabilities.\n" \
    #     "7. Strategic Positioning and Future Outlook (400 words): Perform a SWOT analysis to assess the company's strategic positioning, identifying strengths, weaknesses, opportunities, and threats in relation to current market dynamics. Discuss the company's strategic plans, focusing on growth opportunities, innovation strategies, and potential market expansion. \n" \
    #     "8. Sustainability and Corporate Responsibility (200 words): Analyze the company’s sustainability initiatives, including environmental impact reduction, resource management, and community engagement. Evaluate the company's corporate responsibility practices, looking at how it addresses ethical issues, stakeholder engagement, and its impact on local and global communities.\n\n" \
    #     "9. Conclusion (200 words): Based on the analysis provided, outline any recommendations for potential investors or stakeholders. Summarize the key findings and the overall investment risk associated with the company.\n" \
    #     "All the sections should collectively present a comprehensive analysis, expanding on the key points highlighted in the executive summary.\n" \
    #     "Make extensive use of the following data to construct the report. This information will provide a backdrop for understanding the company's financial health, market position, and potential risks, offering a holistic view of its current status and future prospects. Make sure to use the thesis to better align the report with the user's needs. Ensure that the report is at least 2000 words.\n\n" \

    user_message_content = f"Generate a structured and comprehensive due-diligence report suitable for finance professionals (at least 2000 words), for the following company, following this provided format:\n\n" \
        f"1. Executive Summary (200 words): Provide an overview of the company, including a summary of key findings from the due diligence analysis. Highlight the primary opportunities and risks associated with the company, with a brief mention of the economic indicators that could impact the company's performance. Identify key KPIs that are pertinent to the specific industry.\n" \
        "2. Company Overview (250 words): Generate a detailed overview of the company including its founding year, founders, headquarters location, number of employees, and key comparable companies. Identify the industry in which the company operates and provide some overview of the growth potential within that vertical.\n" \
        "3. Financial Analysis (400 words): Summarize the last five years of the company's financial statements, including income statements, balance sheets, and cash flow statements. Identify any major financial risks or anomalies in the financial data provided and interpret them through the context of the industry the company operates in.\n" \
        "4. Market and Industry Analysis (500 words): Describe the current market environment of the industry, including major competitors, market trends, and the company's market share. Evaluate the company’s competitive position and its strategy for maintaining or improving this position and potential for growth and potential risks to growth within the industry.\n" \
        "5. Risk Management (500 words): Detail the risk management strategies employed by the company, including financial, operational, and strategic risk controls. Identify any operational and/or human resources-related risks that can affect the company's competitive position if possible.\n" \
        "6. Legal Compliance (250 words): List all known legal disputes the company is currently involved in or has been involved in the past five years. Provide an analysis of compliance with relevant industry regulations and any potential legal liabilities.\n" \
        "7. Strategic Positioning and Future Outlook (400 words): Perform a SWOT analysis to assess the company's strategic positioning, identifying strengths, weaknesses, opportunities, and threats about current market dynamics. Discuss the company's strategic plans, focusing on growth opportunities, innovation strategies, and potential market expansion.\n" \
        "8. Sustainability and Corporate Responsibility (200 words): Analyze the company’s sustainability initiatives, including environmental impact reduction, resource management, and community engagement. Evaluate the company's corporate responsibility practices, looking at how it addresses ethical issues, stakeholder engagement, and its impact on local and global communities.\n\n" \
        "9. Conclusion (200 words): Based on the analysis provided and the investment thesis of the company, would the company fit into the criteria? If so, summarize key findings, if not summarize the rationale behind not moving forward.\n" \
        "All the sections should collectively present a comprehensive analysis, expanding on the key points highlighted in the executive summary.\n" \
        "Make extensive use of the following data to construct the report. This information will provide a backdrop for understanding if a firm should provide a venture capital investment. Make sure to use the thesis to better align the report with the user's needs and provide a summary of the report. Ensure that the report is at least 2000 words.\n\n" \


    user_message_content += f"Gross Profit Margin: {analysis_results['gross_profit_margin']}\n"
    user_message_content += f"Net Profit Margin: {analysis_results['net_profit_margin']}\n"
    user_message_content += f"Operating Income Margin: {analysis_results['operating_income_margin']}\n"
    user_message_content += f"Operating Expenses Ratio: {analysis_results['operating_expenses_ratio']}\n"
    user_message_content += f"Current Ratio: {analysis_results['current_ratio']}\n"
    user_message_content += f"Debt Ratio: {analysis_results['debt_ratio']}\n"
    user_message_content += f"Debt-to-Equity ratio: {analysis_results['debt_to_equity_ratio']}\n"
    user_message_content += f"Interest Coverage Ratio: {analysis_results['interest_coverage_ratio']}\n"
    user_message_content += f"Asset Turnover Ratio: {analysis_results['asset_turnover_ratio']}\n"
    user_message_content += f"Inventory Turnover Ratio: {analysis_results['inventory_turnover_ratio']}\n"
    user_message_content += f"Cash Conversion Cycle: {analysis_results['cash_conversion_cycle']}\n"
    user_message_content += f"Quick Ratio: {analysis_results['quick_ratio']}\n"
    user_message_content += f"Return on Assets: {analysis_results['return_on_assets']}\n"
    user_message_content += f"Return on Equity: {analysis_results['return_on_equity']}\n"
    user_message_content += f"Operating Cash Flows Ratio: {analysis_results['operating_cash_flows_ratio']}\n"
    user_message_content += f"Cash Flow-to-Net Income Ratio: {analysis_results['cash_flow_to_net_income']}\n"
    user_message_content += f"Current Liability Coverage: {analysis_results['current_liability_coverage']}\n\n"
    user_message_content += f"Transaction Rationale Summary:{cim_summary}\n\n"
    user_message_content += f"Thesis Statement: {thesis_prompt_text}"
    
    # Print the user message content for testing
    print("User Message Content:", user_message_content)


    # Generate the chat completion
    response = client.chat.completions.create(
        # model=os.getenv("OPENAI_MODEL"),
        model="gpt-4o",
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

    return response

    # # Check the response and render the report using a template
    # if response.choices:
    #     report_content = response.choices[0].message.content.strip()
    #     return render_template('dd_analysis.html', economic_indicators=economic_indicators, analysis_results=analysis_results, thesis_prompt_text = thesis_prompt_text, report_content=report_content)
    # else:
    #     return send_response(500, message="No choices in the response")

# This regex finds text enclosed in double or single asterisks
def bold_text(text):
    bolded_text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    bolded_text = re.sub(r'\*([^*]+)\*', r'<strong>\1</strong>', bolded_text)
    return bolded_text

app.jinja_env.filters['bold_text'] = bold_text

# Standard response format function
def send_response(status_code, data=None, message=None):
    response = {
        'status': 'success' if status_code == 200 else 'error',
        'data': data,
        'message': message
    }
    return jsonify(response), status_code


if __name__ == '__main__':
    port = 9999

    # Configure SSL context for bypassing SSL verification
    myssl = ssl.create_default_context()
    myssl.check_hostname = False
    myssl.verify_mode = ssl.CERT_NONE

    # Get the default pyngrok configuration
    pyngrok_config = conf.get_default()

    # Install ngrok with the custom SSL context if ngrok is not already installed
    if not os.path.exists(pyngrok_config.ngrok_path):
        installer.install_ngrok(pyngrok_config.ngrok_path, context=myssl)

    # Set the ngrok auth token and establish a tunnel
    ngrok.set_auth_token(os.getenv('NGROK_AUTH_TOKEN'))
    reserved_domain = "equitary-reports.ngrok.io"
    
    try:
        # Connect to ngrok and create a tunnel
        public_url = ngrok.connect(port, hostname=reserved_domain)
        print(f"Public URL: {public_url}")
    except ngrok.PyngrokNgrokHTTPError as e:
        if "already bound to another tunnel session" in str(e):
            print(f"The domain '{reserved_domain}' is already in use. Attempting to release and retry.")
        
            # Attempt to kill the existing tunnel session
            tunnels = ngrok.get_tunnels()
            for tunnel in tunnels:
                if tunnel.public_url == f"https://{reserved_domain}.ngrok.io":
                    ngrok.disconnect(tunnel.public_url)
        
            # Retry creating the tunnel
            try:
                public_url = ngrok.connect(port, hostname=reserved_domain)
                print(f"Public URL: {public_url}")
            except Exception as retry_exception:
                print(f"Retry failed: {retry_exception}")
                # Optionally, fall back to a random subdomain
                public_url = ngrok.connect(port)
                print(f"Fallback Public URL: {public_url}")
        else:
            print(f"Failed to start ngrok tunnel: {e}")
    
    print(f'ngrok tunnel "{public_url}" -> "http://127.0.0.1:{port}"')

    # Start the Flask app
    app.run(port=port)
