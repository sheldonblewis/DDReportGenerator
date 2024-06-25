import pandas as pd
import re

def clean_value(value):
    """
    Cleans and converts a string value to float.
    Handles parentheses for negative values and strips extra spaces.
    """
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
    """
    Reads a CSV file and processes it into a pandas DataFrame.
    Cleans and structures the data for further analysis.
    """
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

# Process all 3 sheets
def ProcessAllSheets(balance_sheet_csv, income_statement_csv, cash_flow_statement_csv):
    df_balance_sheet = csv_to_dataframe(balance_sheet_csv)
    df_income_statement = csv_to_dataframe(income_statement_csv)
    df_cash_flow_statement = csv_to_dataframe(cash_flow_statement_csv)
    formatted_alldicts_balance_sheet = create_all_sheets_formatted_dicts([df_balance_sheet, df_income_statement, df_cash_flow_statement])
    data = add_year_column(formatted_alldicts_balance_sheet)
    return data
    # save_dicts_to_text_file(formatted_alldicts_balance_sheet, all_sheets_formatted_output)
    # print(f"Formatted balance sheet dictionaries have been saved to {all_sheets_formatted_output}")
    # return all_sheets_formatted_output

def dataframe_to_dict(df, year):
    """
    Converts a DataFrame row to a dictionary for a specific year.
    """
    data = {}
    for index, row in df.iterrows():
        description = row['Description']
        value = row[year]
        data[description] = value
    return data


def create_all_sheets_formatted_dicts(df):
    """
    Creates formatted dictionaries for each year from the DataFrame based on the statement type.
    """
    years = df[0].columns[1:]  
    year_dicts = {}

    for year in years:
        data_dict_0 = dataframe_to_dict(df[0], year)
        data_dict_1 = dataframe_to_dict(df[1], year)
        data_dict_2 = dataframe_to_dict(df[2], year)


        # if statement_type == 'balance_sheet':
        formatted_dict = {
                'Total Assets': data_dict_0.get('Total Assets', 0),
                'Current Assets': data_dict_0.get('Total Current Assets', 0),
                'AR': data_dict_0.get('Accounts Receivable', 0),
                'Inventory': data_dict_0.get('Inventory', 0),
                'Total Liabilities': data_dict_0.get('Total Liabilities', 0),
                'Current Liabilities': data_dict_0.get('Total Current Liabilities', 0),
                'AP': data_dict_0.get('Accounts Payable', 0),
                'Total Equity': data_dict_0.get('Total Equity', 0),
                'Revenue': data_dict_1.get('Revenue', 0),
                'Net Income': data_dict_1.get('Net Income', 0),
                'Net Interest Exp.': data_dict_1.get('Net Interest Exp.', 0),
                'Operating Expenses': data_dict_1.get('Operating Expenses', 0),
                'Depreciation and Amort., Total': data_dict_2.get('Depreciation & Amort., Total', 0),
                'Cash Flow from Operating Activities': data_dict_2.get('Cash from Ops.', 0),
                'Cash Flow from Investing Activities': data_dict_2.get('Cash from Investing', 0),
                'Cash Flow from Financing Activities': data_dict_2.get('Cash from Financing', 0),
                'Cost of Sales': data_dict_2.get('Cash from Financing', 0),
            }
        year_dicts[year] = formatted_dict

    return year_dicts

def add_year_column(data_dicts):
    data = []
    for year, data_dict in data_dicts.items():
        data_dict['Year'] = year
        data.append(data_dict)
    return pd.DataFrame(data)

# def save_dicts_to_text_file(formatted_dicts, output_file):
#     """
#     Saves the formatted dictionaries to a text file.
#     """
#     with open(output_file, 'w') as file:
#         for year, formatted_dict in formatted_dicts.items():
#             file.write(f"{year}:\n")
#             file.write("{\n")
#             for key, value in formatted_dict.items():
#                 file.write(f"    '{key}': {value},\n")
#             file.write("}\n\n")

# # File paths
# balance_sheet_file = 'balance_sheet.csv'
# income_statement_file = 'income_statement.csv'
# cash_flow_statement_file = 'cash_flow_statement.csv'

# # Output files
# balance_sheet_output = 'formatted_balance_sheets.txt'
# income_statement_output = 'formatted_income_statements.txt'
# cash_flow_statement_output = 'formatted_cash_flow_statements.txt'
all_sheets_formatted_output = 'formatted_all_sheet_statements.txt'

