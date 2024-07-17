from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
from urllib.request import urlopen
import certifi
from flask_cors import CORS
import re

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
    base_url_v4 = "https://financialmodelingprep.com/api/v4"

    try:
        key_metrics_url = f"{base_url}/key-metrics/{ticker}?period=annual&apikey={api_key}"
        ratios_url = f"{base_url}/ratios/{ticker}?period=quarter&apikey={api_key}"
        financial_score_url = f"{base_url_v4}/score?symbol={ticker}&apikey={api_key}"
        enterprise_values_url = f"{base_url}/enterprise-values/{ticker}?period=quarter&apikey={api_key}"
        income_stmt_url = f"{base_url}/income-statement/{ticker}?limit=5&apikey={api_key}"
        balance_sheet_url = f"{base_url}/balance-sheet-statement/{ticker}?limit=5&apikey={api_key}"
        cash_flow_url = f"{base_url}/cash-flow-statement/{ticker}?limit=5&apikey={api_key}"
        analyst_rec_url = f"{base_url}/analyst-stock-recommendations/{ticker}?apikey={api_key}"
        analyst_est_url = f"{base_url}/analyst-estimates/{ticker}?apikey={api_key}"

        key_metrics_data = requests.get(key_metrics_url).json()
        ratios_data = requests.get(ratios_url).json()
        financial_score_data = requests.get(financial_score_url).json()
        enterprise_values_data = requests.get(enterprise_values_url).json()
        income_stmt_res = requests.get(income_stmt_url).json()
        balance_sheet_res = requests.get(balance_sheet_url).json()
        cash_flow_res = requests.get(cash_flow_url).json()
        analyst_rec_res = requests.get(analyst_rec_url).json()
        analyst_est_res = requests.get(analyst_est_url).json()

        financial_info = {
            "key_metrics": key_metrics_data,
            "ratios": ratios_data,
            "financial_score": financial_score_data,
            "enterprise_values": enterprise_values_data,
            "income_statement": income_stmt_res,
            "balance_sheet": balance_sheet_res,
            "cash_flow": cash_flow_res,
            "analyst_recommendations": analyst_rec_res,
            "analyst_estimates": analyst_est_res
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
    investment_criteria = request.args.get('investment_criteria', '')

    # Fetch financial data and press releases for the specified ticker
    financial_data = get_financial_data(ticker)
    press_releases = get_press_releases(ticker)

    if not financial_data:
        return send_response(404, message=f"Could not retrieve financial data for ticker: {ticker}")

    # Construct the message for the OpenAI API call
    user_message_content = f"Generate a structured and comprehensive report suitable for finance professionals (at least 2000 words), for the stock of {ticker} following this provided format:\n\n" \
                            f"1. Thesis Statement (200 words): Provide a brief overview and thesis statement for the overall analysis, including a buy/sell recommendation, encapsulating the key findings and insights from the report, and specifically addressing how the company aligns with the investment criteria: '{investment_criteria}'. Highlight the primary reasons for the recommendation. \n" \
                            # "2. Key News Highlights (400 words): Reflect on recent news impacting the stock, including market reactions. Cover major headlines like product launches, leadership changes, regulatory updates, or macroeconomic events. \n \"
                            "3. Recent Company Announcements (400 words): Discuss the significance of recent events and their potential impact. This includes quarterly earnings calls, strategic initiatives, partnerships, and other corporate announcements. Analyze how these events align with the company’s long-term strategy and objectives. \n" \
                            "4. Insights from Latest Earnings Reports (600 words): Analyze financial trends, growth potential, and profitability. Provide an in-depth review of the most recent earnings report, including revenue, net income, earnings per share (EPS), and other key financial metrics. Discuss year-over-year performance, and quarter-over-quarter trends, and compare actual results to analysts' expectations. \n" \
                            "5. Analysis of Current Analyst Ratings (600 words): Summarize consensus and divergent views from financial analysts. Include ratings from major investment banks and financial institutions, highlighting buy, sell, and hold recommendations. Discuss the rationale behind these ratings and any significant changes or trends in analyst opinions. \n" \
                            "6. Overview of Recent M&A Activity (300 words): Detail any mergers or acquisitions and their strategic importance. Explain how these activities could enhance the company's market position, operational capabilities, or financial performance. Discuss any synergies, cost savings, or revenue growth opportunities expected from these transactions. \n" \
                            "7. Other Relevant Information (300 words): Include factors such as market trends, competitor analysis, and industry outlook impacting the stock valuation and market performance. Discuss broader economic indicators, technological advancements, regulatory changes, and other external factors that could influence the company's future prospects. \n\n" \
                            "All the sections should expand on the brief points highlighted in the thesis statement.\n" \
                            "Make extensive use of the following data to construct the report:\n\n" \

    # Adding enterprise values
    if financial_data['enterprise_values']:
        latest_ev = financial_data['enterprise_values'][0]  # Assuming the most recent data
        user_message_content += f"\n--- Enterprise Values ---\n" \
                                f"Date: {latest_ev['date']}\n" \
                                f"Stock Price: {latest_ev['stockPrice']}\n" \
                                f"Number of Shares: {latest_ev['numberOfShares']}\n" \
                                f"Market Capitalization: {latest_ev['marketCapitalization']}\n" \
                                f"Cash and Cash Equivalents: {latest_ev['minusCashAndCashEquivalents']}\n" \
                                f"Total Debt: {latest_ev['addTotalDebt']}\n" \
                                f"Enterprise Value: {latest_ev['enterpriseValue']}\n" \
                                "Analyze these values to assess the company's total valuation.\n"
        
    # Adjusting key metrics
    if financial_data['key_metrics']:
        latest_key_metrics = financial_data['key_metrics'][0]
        user_message_content += f"\n--- Key Metrics ---\n" \
                                f"Market Cap: {latest_key_metrics['marketCap']}\n" \
                                f"PE Ratio: {latest_key_metrics['peRatio']}\n" \
                                f"Price to Sales Ratio: {latest_key_metrics['priceToSalesRatio']}\n" \
                                f"ROE: {latest_key_metrics['roe']}\n" \
                                f"Debt to Equity: {latest_key_metrics['debtToEquity']}\n" \
                                f"Current Ratio: {latest_key_metrics['currentRatio']}\n" \
                                f"Free Cash Flow Yield: {latest_key_metrics['freeCashFlowYield']}\n" \
                                f"Revenue Per Share: {latest_key_metrics['revenuePerShare']}\n" \
                                f"Net Income Per Share: {latest_key_metrics['netIncomePerShare']}\n" \
                                f"Free Cash Flow Per Share: {latest_key_metrics['freeCashFlowPerShare']}\n" \
                                "Analyze these metrics to provide insight into the company's valuation, profitability, financial health, and investment potential.\n"

    # Adding financial ratios
    if financial_data['ratios']:
        latest_ratios = financial_data['ratios'][0]  # Assuming the most recent data
        user_message_content += f"\n--- Financial Ratios ---\n" \
                                f"PE Ratio: {latest_ratios['priceEarningsRatio']}\n" \
                                f"Current Ratio: {latest_ratios['currentRatio']}\n" \
                                f"Return on Equity: {latest_ratios['returnOnEquity']}\n" \
                                "Include an analysis of these ratios to evaluate the financial health and performance of the company.\n"

    # Adding financial score
    if financial_data['financial_score']:
        latest_score = financial_data['financial_score'][0]  # Assuming the most recent data
        user_message_content += f"\n--- Financial Score ---\n" \
                                f"Altman Z-Score: {latest_score['altmanZScore']}\n" \
                                f"Piotroski Score: {latest_score['piotroskiScore']}\n" \
                                f"Working Capital: {latest_score['workingCapital']}\n" \
                                f"EBIT: {latest_score['ebit']}\n" \
                                "This section provides an overall assessment of the company's financial stability and risk profile based on various scoring models.\n"


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

    if financial_data['analyst_recommendations']:
        latest_recommendation = financial_data['analyst_recommendations'][0]
        user_message_content += f"\n--- Analyst Recommendations ---\n" \
                                f"Date: {latest_recommendation['date']}, " \
                                f"Buy: {latest_recommendation['analystRatingsbuy']}, " \
                                f"Hold: {latest_recommendation['analystRatingsHold']}, " \
                                f"Sell: {latest_recommendation['analystRatingsSell']}, " \
                                f"Strong Sell: {latest_recommendation['analystRatingsStrongSell']}, " \
                                f"Strong Buy: {latest_recommendation['analystRatingsStrongBuy']}\n"

    if financial_data['analyst_estimates']:
        latest_estimate = financial_data['analyst_estimates'][0]
        user_message_content += f"\n--- Analyst Estimates ---\n" \
                                f"Date: {latest_estimate['date']}\n" \
                                f"Estimated Revenue Low: {latest_estimate['estimatedRevenueLow']}\n" \
                                f"Estimated Revenue High: {latest_estimate['estimatedRevenueHigh']}\n" \
                                f"Estimated Revenue Avg: {latest_estimate['estimatedRevenueAvg']}\n" \
                                f"Estimated EBITDA Low: {latest_estimate['estimatedEbitdaLow']}\n" \
                                f"Estimated EBITDA High: {latest_estimate['estimatedEbitdaHigh']}\n" \
                                f"Estimated EBITDA Avg: {latest_estimate['estimatedEbitdaAvg']}\n" \
                                f"Estimated EBIT Low: {latest_estimate['estimatedEbitLow']}\n" \
                                f"Estimated EBIT High: {latest_estimate['estimatedEbitHigh']}\n" \
                                f"Estimated EBIT Avg: {latest_estimate['estimatedEbitAvg']}\n" \
                                f"Estimated Net Income Low: {latest_estimate['estimatedNetIncomeLow']}\n" \
                                f"Estimated Net Income High: {latest_estimate['estimatedNetIncomeHigh']}\n" \
                                f"Estimated Net Income Avg: {latest_estimate['estimatedNetIncomeAvg']}\n" \
                                f"Estimated SGA Expense Low: {latest_estimate['estimatedSgaExpenseLow']}\n" \
                                f"Estimated SGA Expense High: {latest_estimate['estimatedSgaExpenseHigh']}\n" \
                                f"Estimated SGA Expense Avg: {latest_estimate['estimatedSgaExpenseAvg']}\n" \
                                f"Estimated EPS Avg: {latest_estimate['estimatedEpsAvg']}\n" \
                                f"Estimated EPS High: {latest_estimate['estimatedEpsHigh']}\n" \
                                f"Estimated EPS Low: {latest_estimate['estimatedEpsLow']}\n" \
                                f"Number of Analysts Estimating Revenue: {latest_estimate['numberAnalystEstimatedRevenue']}\n" \
                                f"Number of Analysts Estimating EPS: {latest_estimate['numberAnalystsEstimatedEps']}\n"

    if press_releases:
        latest_release = press_releases[0]
        user_message_content += f"\n--- Most Recent Press Release ---\n" \
                                f"Date: {latest_release['date']}\n" \
                                f"Title: {latest_release['title']}\n" \
                                f"Details: {latest_release['text']}\n"

    # Print the user message content for testing
    print("User Message Content:", user_message_content)

    # Generate the chat completion
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a highly advanced equity research bot that generates report-style equity analyses using the user-provided financial data, with each section being intricate and detailed."},
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
        return render_template('analysis.html', financial_data=financial_data, report_content=report_content)
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
