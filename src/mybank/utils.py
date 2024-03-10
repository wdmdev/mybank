from typing import List
from pandas import DataFrame

def filter_payments_by_text(df: DataFrame, include: List[str] = [], exclude: List[str] = [], 
                case_include: bool = False, case_exclude: bool = False) -> DataFrame:
    """ Filter a payments dataframe based on the text in the 'Text' column
    
    Args:
    --------
    df: DataFrame
        A dataframe of payments.
    include: List[str]
        List of strings to include in the filtering.
    exclude: List[str]
        List of strings to exclude in the filtering.
    case_include: bool
        Whether to consider case when including strings.
    case_exclude: bool
        Whether to consider case when excluding strings.

    Returns:
    --------
    DataFrame
        A dataframe of the filtered payments.     
    """
    if include and exclude:
        return df[(df["Text"].str.contains("|".join(include), case=case_include) &
                    ~df["Text"].str.contains("|".join(exclude), case=case_exclude))]
    elif include and not exclude:
        return df[df["Text"].str.contains("|".join(include), case=case_include)]
    elif not include and exclude:
        return df[~df["Text"].str.contains("|".join(exclude), case=case_exclude)]
    
    return df