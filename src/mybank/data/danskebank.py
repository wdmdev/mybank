import os
import glob
import pandas as pd

from typing import Optional

def get_csv_bank_statements(folder_path:str, account_owner:Optional[str]=None) -> pd.DataFrame:
    """ Read all bank statements csv files in a folder and concatenate them into a single dataframe

    csv files are expected to be in the Danske Bank format 
    used when exporting bank statements from their online banking platform:
    - They are expected to have headers
    - They are expected to be separated by semicolons
    - They are expected to be encoded in latin1
    - They are expected to use comma as decimal separator
    - They are expected to include the columns 'Dato'(Date), 'Text'(Tekst) and 'Beløb'(Amount) values
        - Columns names will be converted to English
    - All columns uses Danish formats i.e. 
        - 'Date' is in 'dd-mm-yyyy' format
        - 'Text' can include Danish characters
        - 'Amount' is in 'x.xxx,xx' format

    Args:
    --------
    folder_path: str
        Path to the folder containing csv files.
    account_owner: Optional[str]
        Name of the account owner. If not provided, it will be included in the dataframe.

    Returns:
    --------
    pd.DataFrame
        A dataframe of the csv files.
        Contains the columns 'Date'(datetime), 'Text'(utf-8), 'Amount'(float), 'Bank'(str) and 'Account Owner'(str) (if provided).
    
    """
    files = glob.glob(os.path.join(folder_path, "*.csv"))
    df = pd.concat([pd.read_csv(f, encoding='latin1', sep=';', decimal=',') for f in files])
    # Remove rows where 'Status' is not 'Udført'
    df = df[df['Status'] == 'Udført']
    # Select only the required columns
    df = df[['Dato', 'Tekst', 'Beløb']]
    df = df.iloc[:, :3].rename(columns={'Dato':'Date', 'Tekst':'Text', 'Beløb':'Amount'})
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
    df['Amount'] = df['Amount'].str.replace('.', '').str.replace(',', '.').astype(float)
    df['Bank'] = 'Danske Bank'
    if account_owner:
        df['Account Owner'] = account_owner

    return df