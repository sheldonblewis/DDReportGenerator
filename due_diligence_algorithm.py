import pandas as pd
import numpy as np

def rename_columns(data, alternative_names):
    for account, alternatives in alternative_names.items():
        for alt_name in alternatives:
            if alt_name in data.columns:
                data.rename(columns={alt_name: account}, inplace=True)
                break

def calculate_gross_profit_margin(data):
    
    alternative_names = {
        'Revenue': ['Revenue', 'Sales'],
        'COGS': ['COGS', 'Cost of Goods Sold', 'Cost of Sales']
    }

    rename_columns(data, alternative_names)
    
    data = data.dropna(subset=['Revenue', 'COGS'])
    if data.empty:
        print("No valid data remaining after dropping rows with missing values.")
        return pd.DataFrame()

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

    rename_columns(data, alternative_names)
    
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

    rename_columns(data, alternative_names)
    
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
        return pd.DataFrame()

    data['Debt Ratio'] = data['Total Debt'] / data['Total Assets']
    data['(% Change)'] = data['Debt Ratio'].pct_change() * 100
    data['(% Change)'] = data['(% Change)'].fillna('')

    return data

def calculate_debt_to_equity_ratio(data):
    
    if 'Total Debt' not in data.columns or 'Total Assets' not in data.columns:
        print("Error: 'Total Debt' or 'Total Assets' column missing.")
        return pd.DataFrame()
    
    data['Debt to Equity Ratio'] = data['Total Debt'] / (data['Total Assets'] - data['Total Debt'])
    data['(% Change)'] = data['Debt to Equity Ratio'].pct_change() * 100
    data['(% Change)'] = data['(% Change)'].fillna('')

    return data

def calculate_interest_coverage_ratio(data):
    
    data['Interest Coverage Ratio'] = (data['Net Income'] + data['Net Interest Exp.']) / data['Net Interest Exp.']
    data['(% Change)'] = data['Interest Coverage Ratio'].pct_change() * 100
    data['(% Change)'] = data['(% Change)'].fillna('')

    return data

def calculate_asset_turnover_ratio(data):
    
    alternative_names = {
        'Revenue': ['Revenue', 'Sales'],
        'Total Assets': ['Total Assets', 'Assets']
    }

    rename_columns(data, alternative_names)
    
    if 'Revenue' not in data.columns or 'Total Assets' not in data.columns:
        print("Error: 'Revenue' or 'Total Assets' column missing.")
        return pd.DataFrame()

    if data['Total Assets'].isnull().any() or (data['Total Assets'] == 0).any():
        print("Error: Missing or zero values in 'Total Assets' column.")
        return pd.DataFrame()

    data['Average Total Assets'] = (data['Total Assets'].shift(1) + data['Total Assets']) / 2
    data['Asset Turnover Ratio'] = data['Revenue'] / data['Average Total Assets']

    return data

def calculate_inventory_turnover_ratio(data):
    
    alternative_names = {
        'COGS': ['COGS', 'Cost of Goods Sold', 'Cost of Sales'],
        'Inventory': ['Inventory', 'Stock']
    }

    rename_columns(data, alternative_names)
    
    if 'COGS' not in data.columns or 'Inventory' not in data.columns:
        print("Error: 'COGS' or 'Inventory' column missing.")
        return pd.DataFrame()

    if data['Inventory'].isnull().any() or (data['Inventory'] == 0).any():
        print("Error: Missing or zero values in 'Inventory' column.")
        return pd.DataFrame()

    data['Average Inventory'] = (data['Inventory'].shift(1) + data['Inventory']) / 2
    data['Inventory Turnover Ratio'] = data['COGS'] / data['Average Inventory']

    return data

def calculate_cash_conversion_cycle(data):
    
    data['Average Inventory'] = (data['Inventory'].shift(1) + data['Inventory']) / 2
    data['Average AR'] = (data['AR'].shift(1) + data['AR']) / 2
    data['Average AP'] = (data['AP'].shift(1) + data['AP']) / 2
    data['DIO'] = (data['Average Inventory'] / data['Operating Expenses']) * 365
    data['DSO'] = (data['Average AR'] / data['Revenue']) * 365
    data['DPO'] = (data['Average AP'] / data['Operating Expenses']) * 365
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
