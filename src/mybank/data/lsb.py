import os
import glob
import pandas as pd

from typing import Optional

def get_csv_bank_statements(folder_path:str, account_owner:Optional[str]=None) -> pd.DataFrame:
    """ Read all bank statements csv files in a folder and concatenate them into a single dataframe

    csv files are expected to be in the lsb (Lån & Spar Bank) format 
    used when exporting bank statements from their online banking platform:
    - They are expected to have no headers
    - They are expected to be separated by semicolons
    - They are expected to be encoded in utf-8
    - They are expected to use comma as decimal separator
    - The first three columns are expected to be 'Date', 'Text' and 'Amount' values
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
    files = glob.glob(os.path.join(folder_path, '*.csv'))
    df = pd.concat([pd.read_csv(f, encoding='utf-8', sep=';', decimal=',', header=None) for f in files])
    df = df.iloc[:, :3].rename(columns={0:'Date', 1:'Text', 2:'Amount'})
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    df['Amount'] = df['Amount'].str.replace('.', '').str.replace(',', '.').astype(float)
    df['Bank'] = 'LSB'
    if account_owner:
        df['Account Owner'] = account_owner

    return df