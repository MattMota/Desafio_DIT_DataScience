import pandas as pd
import re
from python.constants import DECODED_CHARS, CONFORMED_BOOLEANS


def correct_encoding(broken_df: pd.DataFrame) -> pd.DataFrame:
    '''
    Converts poorly encoded characters from UTF-8 (Latin-1 supplement) with
    Portuguese diacritical accents into their correct counterparts.

    Arguments:
        broken_df (pandas.DataFrame): A DataFrame suffering from the above issue.
    
    Returns:
        corrected_df (pandas.DataFrame): A copy of `broken_df` with the
            characters correctly encoded.
    '''

    escaped_dict = {re.escape(k): v for k, v in DECODED_CHARS.items()}

    corrected_df = broken_df.replace(escaped_dict, regex=True)

    return corrected_df


def conform_booleans(column: pd.Series) -> pd.Series:
    '''
    Conforms boolean-like values for a pandas Series.
    Keeps other values as such.

    Arguments:
        column (pandas.Series): A Series with possible boolean-like values.
    
    Returns:
        bool_column (pandas.Series): A copy of `column` with boolean-like
            values converted to their respective counterparts, according to
            `constants.CONFORMED_BOOLEANS`.
    '''

    def conform_value(val) -> int:

        if isinstance(val, str):
            val = val.strip().lower()

        for k, v in CONFORMED_BOOLEANS.items():
            if val in k:
                return v
        
        return val

    bool_column = column.apply(
        lambda val: conform_value(val)
    )

    return bool_column