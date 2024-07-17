from xls_to_csv import run_cloudconvert_jobs
import pandas as pd
import re

def clean_value(value):
    if pd.isna(value):
        return value
    value = value.strip()
    value = value.replace(',', '')
    value = re.sub(r'\((.*?)\)', r'-\1', value)
    try:
        return float(value)
    except ValueError:
        return value

def csv_to_dataframe(file_path):
    df = pd.read_csv(file_path, header=None)
    years = df.iloc[0, 1:].tolist()
    df.columns = ['Description'] + years
    df = df.drop(0)
    df = df.dropna(how='all')
    df['Description'] = df['Description'].ffill()
    df['Description'] = df['Description'].str.strip()
    for col in years:
        df[col] = df[col].map(lambda x: clean_value(x))
    df.reset_index(drop=True, inplace=True)
    return df

def dataframe_to_dict(df, year):
    data = {}
    for index, row in df.iterrows():
        description = row['Description']
        value = row[year]
        data[description] = value
    return data

def create_formatted_dicts(df, statement_type):
    years = df.columns[1:]
    year_dicts = {}
    for year in years:
        data_dict = dataframe_to_dict(df, year)
        if statement_type == 'balance_sheet':
            formatted_dict = {
                'Total Assets': data_dict.get('Total Assets', 0),
                'Current Assets': data_dict.get('Total Current Assets', 0),
                'AR': data_dict.get('Accounts Receivable', 0),
                'Inventory': data_dict.get('Inventory', 0),
                'Total Liabilities': data_dict.get('Total Liabilities', 0),
                'Current Liabilities': data_dict.get('Total Current Liabilities', 0),
                'AP': data_dict.get('Accounts Payable', 0),
                'Total Equity': data_dict.get('Total Equity', 0),
            }
        elif statement_type == 'income_statement':
            formatted_dict = {
                'Revenue': data_dict.get('Revenue', 0),
                'Net Income': data_dict.get('Net Income', 0),
                'Net Interest Exp.': data_dict.get('Net Interest Exp.', 0),
                'Operating Expenses': data_dict.get('Operating Expenses', 0),
            }
        elif statement_type == 'cash_flow_statement':
            formatted_dict = {
                'Net Income': data_dict.get('Net Income', 0),
                'Depreciation and Amort., Total': data_dict.get('Depreciation & Amort., Total', 0),
                'Cash Flow from Operating Activities': data_dict.get('Cash from Ops.', 0),
                'Cash Flow from Investing Activities': data_dict.get('Cash from Investing', 0),
                'Cash Flow from Financing Activities': data_dict.get('Cash from Financing', 0),
            }
        year_dicts[year] = formatted_dict
    return year_dicts

def add_year_column(data_dicts):
    data = []
    for year, data_dict in data_dicts.items():
        data_dict['Year'] = year
        data.append(data_dict)
    return pd.DataFrame(data)

def calculate_gross_profit_margin(data):
    alternative_names = {
        'Revenue': ['Revenue', 'Sales'],
        'COGS': ['COGS', 'Cost of Goods Sold', 'Cost of Sales']
    }
    for account, alternatives in alternative_names.items():
        for alt_name in alternatives:
            if alt_name in data.columns:
                data.rename(columns={alt_name: account}, inplace=True)
                break
    data = data.dropna(subset=['Revenue', 'COGS'])
    if data.empty:
        print("No valid data remaining after dropping rows with missing values.")
        return None
    data['Gross Profit'] = data['Revenue'] - data['COGS']
    data['Gross Profit Margin'] = (data['Gross Profit'] / data['Revenue']) * 100
    gross_profit_margin_by_year = data.groupby('Year')['Gross Profit Margin'].mean().reset_index()
    gross_profit_margin_by_year['(% Change)'] = gross_profit_margin_by_year['Gross Profit Margin'].pct_change() * 100
    gross_profit_margin_by_year['(% Change)'] = gross_profit_margin_by_year['(% Change)'].fillna('')
    return gross_profit_margin_by_year

def calculate_net_profit_margin(data):
    data['Net Profit Margin'] = (data['Net Income'] / data['Revenue']) * 100
    net_profit_margin_by_year = data.groupby('Year')['Net Profit Margin'].mean().reset_index()
    net_profit_margin_by_year['(% Change)'] = net_profit_margin_by_year['Net Profit Margin'].pct_change() * 100
    net_profit_margin_by_year['(% Change)'] = net_profit_margin_by_year['(% Change)'].fillna('')
    return net_profit_margin_by_year

def calculate_operating_income_margin(data):
    alternative_names = {
        'Revenue': ['Revenue', 'Sales'],
        'COGS': ['COGS', 'Cost of Goods Sold', 'Cost of Sales'],
        'Operating Expenses': ['Operating Expenses', 'OpEx', 'Operating Costs']
    }
    for account, alternatives in alternative_names.items():
        for alt_name in alternatives:
            if alt_name in data.columns:
                data.rename(columns={alt_name: account}, inplace=True)
                break
    data['Operating Income'] = data['Revenue'] - data['COGS'] - data['Operating Expenses']
    data['Operating Income Margin'] = (data['Operating Income'] / data['Revenue']) * 100
    operating_income_margin_by_year = data.groupby('Year')['Operating Income Margin'].mean().reset_index()
    operating_income_margin_by_year['(% Change)'] = operating_income_margin_by_year['Operating Income Margin'].pct_change() * 100
    operating_income_margin_by_year['(% Change)'] = operating_income_margin_by_year['(% Change)'].fillna('')
    return operating_income_margin_by_year

def calculate_operating_expenses_ratio(data):
    alternative_names = {
        'Revenue': ['Revenue', 'Sales'],
        'Operating Expenses': ['Operating Expenses', 'OpEx', 'Operating Costs']
    }
    for account, alternatives in alternative_names.items():
        for alt_name in alternatives:
            if alt_name in data.columns:
                data.rename(columns={alt_name: account}, inplace=True)
                break
    data['Operating Expenses Ratio'] = (data['Operating Expenses'] / data['Revenue']) * 100
    operating_expenses_ratio_by_year = data.groupby('Year')['Operating Expenses Ratio'].mean().reset_index()
    operating_expenses_ratio_by_year['(% Change)'] = operating_expenses_ratio_by_year['Operating Expenses Ratio'].pct_change() * 100
    operating_expenses_ratio_by_year['(% Change)'] = operating_expenses_ratio_by_year['(% Change)'].fillna('')
    return operating_expenses_ratio_by_year

def calculate_current_ratio(data):
    data['Current Ratio'] = data['Current Assets'] / data['Current Liabilities']
    data['(% Change)'] = data['Current Ratio'].pct_change() * 100
    data['(% Change)'] = data['(% Change)'].fillna('')
    return data

def calculate_debt_ratio(data):
    if 'Total Debt' not in data.columns or 'Total Assets' not in data.columns:
        print("Error: 'Total Debt' or 'Total Assets' column missing.")
        return None
    data['Debt Ratio'] = data['Total Debt'] / data['Total Assets']
    data['(% Change)'] = data['Debt Ratio'].pct_change() * 100
    data['(% Change)'] = data['(% Change)'].fillna('')
    return data

def calculate_debt_to_equity_ratio(data):
    if 'Total Debt' not in data.columns or 'Total Equity' not in data.columns:
        print("Error: 'Total Debt' or 'Total Equity' column missing.")
        return None
    data['Debt to Equity Ratio'] = data['Total Debt'] / data['Total Equity']
    data['(% Change)'] = data['Debt to Equity Ratio'].pct_change() * 100
    data['(% Change)'] = data['(% Change)'].fillna('')
    return data

def calculate_interest_coverage_ratio(data):
    data['Interest Coverage Ratio'] = (data['Net Income'] + data['Interest Expense']) / data['Interest Expense']
    data['(% Change)'] = data['Interest Coverage Ratio'].pct_change() * 100
    data['(% Change)'] = data['(% Change)'].fillna('')
    return data

def calculate_asset_turnover_ratio(data):
    alternative_names = {
        'Revenue': ['Revenue', 'Sales'],
        'Total Assets': ['Total Assets', 'Assets']
    }
    for account, alternatives in alternative_names.items():
        for alt_name in alternatives:
            if alt_name in data.columns:
                data.rename(columns={alt_name: account}, inplace=True)
                break
    if 'Revenue' not in data.columns or 'Total Assets' not in data.columns:
        print("Error: 'Revenue' or 'Total Assets' column missing.")
        return None
    if data['Total Assets'].isnull().any() or (data['Total Assets'] == 0).any():
        print("Error: Missing or zero values in 'Total Assets' column.")
        return None
    data['Average Total Assets'] = (data['Total Assets'].shift(1) + data['Total Assets']) / 2
    data['Asset Turnover Ratio'] = data['Revenue'] / data['Average Total Assets']
    return data

def calculate_inventory_turnover_ratio(data):
    alternative_names = {
        'COGS': ['COGS', 'Cost of Goods Sold', 'Cost of Sales'],
        'Inventory': ['Inventory', 'Stock']
    }
    for account, alternatives in alternative_names.items():
        for alt_name in alternatives:
            if alt_name in data.columns:
                data.rename(columns={alt_name: account}, inplace=True)
                break
    if 'COGS' not in data.columns or 'Inventory' not in data.columns:
        print("Error: 'COGS' or 'Inventory' column missing.")
        return None
    if data['Inventory'].isnull().any() or (data['Inventory'] == 0).any():
        print("Error: Missing or zero values in 'Inventory' column.")
        return None
    data['Average Inventory'] = (data['Inventory'].shift(1) + data['Inventory']) / 2
    data['Inventory Turnover Ratio'] = data['COGS'] / data['Average Inventory']
    return data

def calculate_cash_conversion_cycle(data):
    data['Average Inventory'] = (data['Inventory'].shift(1) + data['Inventory']) / 2
    data['Average AR'] = (data['AR'].shift(1) + data['AR']) / 2
    data['Average AP'] = (data['AP'].shift(1) + data['AP']) / 2
    data['DIO'] = (data['Average Inventory'] / data['COGS']) * 365
    data['DSO'] = (data['Average AR'] / data['Revenue']) * 365
    data['DPO'] = (data['Average AP'] / data['COGS']) * 365
    data['Cash Conversion Cycle'] = data['DIO'] + data['DSO'] - data['DPO']
    return data

def calculate_quick_ratio(data):
    data['Quick Ratio'] = (data['Current Assets'] - data['Inventory']) / data['Current Liabilities']
    return data

def calculate_return_on_assets(data):
    data['Average Total Assets'] = (data['Total Assets'].shift(1) + data['Total Assets']) / 2
    data['Return on Assets'] = data['Revenue'] / data['Average Total Assets']
    return data

def calculate_return_on_equity(data):
    data['Average Total Equity'] = (data['Total Equity'].shift(1) + data['Total Equity']) / 2
    data['Return on Equity'] = data['Net Income'] / data['Average Total Equity']
    return data

def calculate_operating_cash_flows_ratio(data):
    data['Operating Cash Flows Ratio'] = data['Cash Flow from Operating Activities'] / data['Total Liabilities']
    return data

def calculate_cash_flow_to_net_income(data):
    data['Cash Flow to Net Income'] = data['Cash Flow from Operating Activities'] / data['Net Income']
    return data

def calculate_current_liability_coverage(data):
    data['Average Current Liabilities'] = (data['Current Liabilities'].shift(1) + data['Current Liabilities']) / 2
    data['Current Liability Coverage'] = data['Cash Flow from Operating Activities'] / data['Average Current Liabilities']
    return data

def run_analysis(data_dicts, statement_type):
    data = add_year_column(data_dicts)
    results = {}
    if statement_type == 'income_statement':
        gpm_result = calculate_gross_profit_margin(data)
        npm_result = calculate_net_profit_margin(data)
        oim_result = calculate_operating_income_margin(data)
        oer_result = calculate_operating_expenses_ratio(data)
        results = {
            'Gross Profit Margin': gpm_result,
            'Net Profit Margin': npm_result,
            'Operating Income Margin': oim_result,
            'Operating Expenses Ratio': oer_result
        }
    elif statement_type == 'balance_sheet':
        cr_result = calculate_current_ratio(data)
        dr_result = calculate_debt_ratio(data)
        der_result = calculate_debt_to_equity_ratio(data)
        results = {
            'Current Ratio': cr_result,
            'Debt Ratio': dr_result,
            'Debt to Equity Ratio': der_result
        }
    elif statement_type == 'cash_flow_statement':
        ocfr_result = calculate_operating_cash_flows_ratio(data)
        cfni_result = calculate_cash_flow_to_net_income(data)
        clc_result = calculate_current_liability_coverage(data)
        results = {
            'Operating Cash Flows Ratio': ocfr_result,
            'Cash Flow to Net Income': cfni_result,
            'Current Liability Coverage': clc_result
        }
    return results


balance_sheet_csv = run_cloudconvert_jobs()
income_statement_csv = run_cloudconvert_jobs()
cash_flow_statement_csv = run_cloudconvert_jobs()

df_income_statement = csv_to_dataframe(income_statement_csv)
formatted_dicts_income_statement = create_formatted_dicts(df_income_statement, 'income_statement')
analysis_results_income = run_analysis(formatted_dicts_income_statement, 'income_statement')

df_balance_sheet = csv_to_dataframe(balance_sheet_csv)
formatted_dicts_balance_sheet = create_formatted_dicts(df_balance_sheet, 'balance_sheet')
analysis_results_balance = run_analysis(formatted_dicts_balance_sheet, 'balance_sheet')

df_cash_flow_statement = csv_to_dataframe(cash_flow_statement_csv)
formatted_dicts_cash_flow_statement = create_formatted_dicts(df_cash_flow_statement, 'cash_flow_statement')
analysis_results_cash_flow = run_analysis(formatted_dicts_cash_flow_statement, 'cash_flow_statement')

print("Income Statement Analysis Results:", analysis_results_income)
print("Balance Sheet Analysis Results:", analysis_results_balance)
print("Cash Flow Statement Analysis Results:", analysis_results_cash_flow)
