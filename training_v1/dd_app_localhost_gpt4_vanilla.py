from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI
from flask_cors import CORS
import requests
import re
# from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Initialize the OpenAI client with your API key
client = OpenAI()
client.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

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

# Flask route to get stock analysis
@app.route('/generate_economic_report', methods=['GET'])
def generate_economic_report():
    economic_indicators = get_economic_indicators()
    income_statement_text = request.args.get('income_statement_text')
    balance_sheet_text = request.args.get('balance_sheet_text')
    cash_flow_statement_text = request.args.get('cash_flow_statement_text')
    thesis_prompt_text = request.args.get('thesis_prompt_text')

    user_message_content = f"Generate a structured and comprehensive due-diligence report suitable for finance professionals (at least 2000 words), for the following company, following this provided format:\n\n" \
        f"1. Executive Summary (200 words): Provide an overview of the company, including a summary of key findings from the due-diligence analysis. Highlight the primary opportunities and risks associated with the company, with a brief mention of the economic indicators that could impact the company's performance. For instance, GDP growth at {economic_indicators['GDP']}%, Unemployment Rate at {economic_indicators['Unemployment Rate']}%, and Inflation Rate at {economic_indicators['Inflation Rate']}%.\n" \
        "2. Company Overview (400 words): Detail the company's history, business model, core products or services, market positioning, and how economic trends may impact its operations or sector. Consider the interest rates currently at " + f"{economic_indicators['Interest Rate']}%" + ", affecting financing and investment decisions. Discuss the company's strategic goals, target market, and any significant milestones or achievements.\n" \
        "3. Financial Analysis (400 words): Evaluate the company's financial health by analyzing the income statement, balance sheet, and cash flow statement. Discuss liquidity, solvency, profitability, and operating efficiency. Highlight the economic context by mentioning relevant indicators, such as GDP growth at " + f"{economic_indicators['GDP']}%" + " and inflation rates at " + f"{economic_indicators['Inflation Rate']}%" + ", to provide context to the financial analysis. Include key financial ratios and trends over recent periods.\n" \
        "4. Market and Competitor Analysis (600 words): Analyze the company's market share, competitive landscape, and industry trends. Assess how the company is positioned relative to its competitors and how broader economic indicators like sector performance at " + f"{economic_indicators['Sector Performance']}" + " and consumer confidence at " + f"{economic_indicators['Consumer Confidence']}" + " may influence the market landscape. Identify the main competitors, market trends, and potential barriers to entry.\n" \
        "5. Risk Assessment (600 words): Identify and evaluate potential risks, including market risks, operational risks, legal risks, and financial risks. Discuss how external economic factors, such as changes in the Manufacturing PMI at " + f"{economic_indicators['Manufacturing PMI']}" + " or unemployment rates at " + f"{economic_indicators['Unemployment Rate']}%" + ", could impact these risk factors. Include an analysis of risk mitigation strategies the company employs and their effectiveness.\n" \
        "6. Legal and Compliance Review (300 words): Overview of the company's legal standings, regulatory compliance issues, and any ongoing litigations. Consider the impact of economic policies and regulations on compliance requirements, reflecting on how changes in economic indicators influence legal landscapes. Highlight any significant legal challenges the company has faced or is currently facing and their potential implications.\n" \
        "7. Management and Governance (300 words): Analyze the company's leadership, corporate governance practices, and any noteworthy executive decisions or changes. Reflect on how economic trends could influence management strategies and governance practices, considering the broader economic indicators provided. Evaluate the effectiveness of the board of directors, the experience of the executive team, and any recent management changes.\n\n" \
        "All the sections should collectively present a comprehensive analysis, expanding on the key points highlighted in the executive summary.\n" \
        "Make extensive use of the following data to construct the report. This information will provide a backdrop for understanding the company's financial health, market position, and potential risks, offering a holistic view of its current status and future prospects.\n\n" \

    # user_message_content = f"Generate a structured and comprehensive due-diligence report suitable for finance professionals, for the following company, following this provided format:\n\n" \
    #     f"1. Executive Summary (200 words): Provide an overview of the company, including a summary of key findings from the due-diligence analysis. Highlight the primary opportunities and risks associated with the company, with a brief mention of the economic indicators that could impact the company's performance.\n" \
    #     "2. Company Overview (400 words): Detail the company's history, business model, core products or services, market positioning, and how economic trends may impact its operations or sector.\n" \
    #     "3. Financial Analysis (400 words): Evaluate the company's financial health by analyzing the income statement, balance sheet, and cash flow statement. Discuss liquidity, solvency, profitability, and operating efficiency. Highlight the economic context by mentioning relevant indicators.\n" \
    #     "4. Market and Competitor Analysis (600 words): Analyze the company's market share, competitive landscape, and industry trends. Assess how the company is positioned relative to its competitors and how broader economic indicators like sector performance may influence the market landscape.\n" \
    #     "5. Risk Assessment (600 words): Identify and evaluate potential risks, including market risks, operational risks, legal risks, and financial risks. Discuss how external economic factors could impact these risk factors.\n" \
    #     "6. Legal and Compliance Review (300 words): Overview of the company's legal standings, regulatory compliance issues, and any ongoing litigations. Consider the impact of economic policies and regulations on compliance requirements, reflecting on how changes in economic indicators influence legal landscapes.\n" \
    #     "7. Management and Governance (300 words): Analyze the company's leadership, corporate governance practices, and any noteworthy executive decisions or changes. Reflect on how economic trends could influence management strategies and governance practices, considering the broader economic indicators provided.\n\n" \
    #     "All the sections should collectively present a comprehensive analysis, expanding on the key points highlighted in the executive summary.\n" \
    #     "Make extensive use of the provided income statement, balance sheet and cash/flow statement provided below and make sure to reference any significant data found in these reports: \n\n" \

    user_message_content += "Income Statement: " \
                            f"{income_statement_text}\n\n"
    
    user_message_content += "Balance Sheet: " \
                            f"{balance_sheet_text}\n\n"
    
    user_message_content += "Cash/Flow Statement: " \
                            f"{cash_flow_statement_text}\n\n"
    
    user_message_content += f"{thesis_prompt_text}"
    
    # Print the user message content for testing
    print("User Message Content:", user_message_content)


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
        # Pass all necessary variables to the template
        return render_template('dd_analysis.html', economic_indicators=economic_indicators, income_statement_text=income_statement_text, balance_sheet_text=balance_sheet_text, cash_flow_statement_text=cash_flow_statement_text, report_content=report_content)
    else:
        return send_response(500, message="No choices in the response")

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
    app.run(debug=True)
