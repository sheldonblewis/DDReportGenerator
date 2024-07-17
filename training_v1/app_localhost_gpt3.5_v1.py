from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
from urllib.request import urlopen
import certifi
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Initialize the OpenAI client with your API key
client = OpenAI()
client.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

# Function to fetch financial data
def get_financial_data(ticker):
    api_key = os.getenv('FINANCIAL_MODELING_PREP_API_KEY')
    base_url = "https://financialmodelingprep.com/api/v3"

    try:
        # Fetching basic financial data
        profile_url = f"{base_url}/profile/{ticker}?apikey={api_key}"
        profile_res = requests.get(profile_url)
        profile_data = profile_res.json()[0]

        # Fetching historical data (income statement, balance sheet, cash flow)
        income_stmt_url = f"{base_url}/income-statement/{ticker}?limit=5&apikey={api_key}"
        balance_sheet_url = f"{base_url}/balance-sheet-statement/{ticker}?limit=5&apikey={api_key}"
        cash_flow_url = f"{base_url}/cash-flow-statement/{ticker}?limit=5&apikey={api_key}"

        income_stmt_res = requests.get(income_stmt_url).json()
        balance_sheet_res = requests.get(balance_sheet_url).json()
        cash_flow_res = requests.get(cash_flow_url).json()

        financial_info = {
            "latest_price": profile_data.get('price', 'N/A'),
            "market_cap": profile_data.get('mktCap', 'N/A'),
            "beta": profile_data.get('beta', 'N/A'),
            "sector": profile_data.get('sector', 'N/A'),
            "income_statement": income_stmt_res,
            "balance_sheet": balance_sheet_res,
            "cash_flow": cash_flow_res,
        }
        return financial_info
    except Exception as e:
        print(f"An error occurred while fetching financial data for {ticker}: {e}")
        return None

# Function to fetch recent press releases for a stock
def get_press_releases(ticker):
    api_key = os.getenv('FINANCIAL_MODELING_PREP_API_KEY')
    base_url = "https://financialmodelingprep.com/api/v3"

    try:
        press_releases_url = f"{base_url}/press-releases/{ticker}?page=0&apikey={api_key}"
        response = urlopen(press_releases_url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        press_releases_data = json.loads(data)
        return press_releases_data
    except Exception as e:
        print(f"An error occurred while fetching press releases for {ticker}: {e}")
        return []

# Flask route to get stock analysis
@app.route('/get_stock_analysis', methods=['GET'])
def get_stock_analysis():
    ticker = request.args.get('ticker', '').upper()

    # Fetch financial data and press releases for the specified ticker
    financial_data = get_financial_data(ticker)
    press_releases = get_press_releases(ticker)

    if not financial_data:
        return send_response(404, message=f"Could not retrieve financial data for ticker: {ticker}")

    # Construct the message for the OpenAI API call
    user_message_content = f"Generate a structured and comprehensive report suitable for finance professionals, focusing on the following analysis points for the stock of {ticker}:\n\n" \
                            "1. Key News Highlights: Reflect on recent news impacting the stock, including market reactions.\n" \
                            "2. Recent Company Announcements: Discuss the significance of recent events and their potential impact.\n" \
                            "3. Insights from Latest Earnings Reports: Analyze financial trends, growth potential, and profitability.\n" \
                            "4. Analysis of Current Analyst Ratings: Summarize consensus and divergent views from financial analysts.\n" \
                            "5. Overview of Recent M&A Activity: Detail any mergers or acquisitions and their strategic importance.\n" \
                            "6. Other Relevant Information: Include factors such as market trends, competitor analysis, and industry outlook impacting the stock valuation and market performance.\n\n" \
                            "Based on these points, analyze the following data:\n\n" \
                            "--- Basic Financial Data ---\n" \
                            f"Latest Price: {financial_data['latest_price']}\n" \
                            f"Market Cap: {financial_data['market_cap']}\n" \
                            f"Beta: {financial_data['beta']}\n" \
                            f"Sector: {financial_data['sector']}\n"

    # Adding a concise summary of historical financial data
    if financial_data['income_statement']:
        latest_income_statement = financial_data['income_statement'][0]
        user_message_content += f"--- Historical Financials ---\n" \
                                f"Latest Income Statement: Date: {latest_income_statement['date']}, Revenue: {latest_income_statement['revenue']}, Net Income: {latest_income_statement['netIncome']}\n"

    if financial_data['balance_sheet']:
        latest_balance_sheet = financial_data['balance_sheet'][0]
        user_message_content += f"Latest Balance Sheet: Date: {latest_balance_sheet['date']}, Total Assets: {latest_balance_sheet['totalAssets']}, Total Liabilities: {latest_balance_sheet['totalLiabilities']}\n"

    if financial_data['cash_flow']:
        latest_cash_flow = financial_data['cash_flow'][0]
        user_message_content += f"Cash Flow Statement as of {latest_cash_flow['date']}:\n" \
                                f"  Operating Cash Flow: {latest_cash_flow.get('operatingCashFlow', 'N/A')}\n" \
                                f"  Capital Expenditure: {latest_cash_flow.get('capitalExpenditure', 'N/A')}\n" \
                                f"  Free Cash Flow: {latest_cash_flow.get('freeCashFlow', 'N/A')}\n" \
                                f"  Investments in Property, Plant, and Equipment: {latest_cash_flow.get('investmentsInPropertyPlantAndEquipment', 'N/A')}\n" \
                                f"  Acquisitions, Net: {latest_cash_flow.get('acquisitionsNet', 'N/A')}\n" \
                                f"  Purchases of Investments: {latest_cash_flow.get('purchasesOfInvestments', 'N/A')}\n" \
                                f"  Sales/Maturities of Investments: {latest_cash_flow.get('salesMaturitiesOfInvestments', 'N/A')}\n" \
                                f"  Other Investing Activities: {latest_cash_flow.get('otherInvestingActivites', 'N/A')}\n"

    # Adding the most recent press release data
    if press_releases:
        latest_release = press_releases[0]
        user_message_content += f"\n--- Most Recent Press Release ---\n" \
                                f"Date: {latest_release['date']}\n" \
                                f"Title: {latest_release['title']}\n" \
                                f"Details: {latest_release['text']}\n"

    user_message_content += "\nPlease limit your response to 5000 characters."

    # Print the user message content for testing
    print("User Message Content:", user_message_content)

    # Generate the chat completion
    response = client.chat.completions.create(
        model=os.getenv('OPENAI_MODEL'),
        messages=[
            {"role": "system", "content": "You are a highly advanced equity research bot that generates a report-style equity analysis using the user-provided financial data."},
            {"role": "user", "content": user_message_content}
        ],
        temperature=0.82,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0.25,
        presence_penalty=0
    )

    # Check the response and render the report using a template
    if response.choices:
        report_content = response.choices[0].message.content.strip()
        # Render an HTML template and pass the report content to it
        return render_template('analysis.html', report_content=report_content)
    else:
        return send_response(500, message="No choices in the response")

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
