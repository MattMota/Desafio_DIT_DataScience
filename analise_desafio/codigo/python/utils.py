import ast
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


def extract_unique_values(mv_att: pd.Series) -> pd.Series:
    '''
    Receives a pandas Series representing multivalued attributes in either
    `["item1", "item2"]` or `item1, item2` format, and gets each unique value.

    Arguments:
        mv_att (pandas.Series): A Series representing a multivalued attribute.
    
    Returns:
        result (pandas.Series): A Series containing only one copy of each value.

    '''

    unique_values = set()
    
    for value in mv_att.dropna():

        if isinstance(value, str):

            if value.startswith('[') and value.endswith(']'):

                try:

                    parsed_list = ast.literal_eval(value)

                    if isinstance(parsed_list, list):

                        unique_values.update(
                            str(item).strip() for item in parsed_list
                        )

                except (ValueError, SyntaxError):
                    pass  # Ignore malformed strings

            else:
                unique_values.update(
                    chunk.strip() for chunk in value.split(',')
                )

        elif isinstance(value, list):
            unique_values.update(
                str(val).strip() for val in value
            )
    
    result = pd.Series(sorted(unique_values)).reset_index(drop=True)

    return result


def build_bridge_table(
    dimension_column: pd.Series,
    fact_table: pd.DataFrame,
    fact_id_column: str,
    fact_multival_column: str
) -> pd.DataFrame:
    '''
    Creates bridge tables for multivalued attributes based
    on their respective dimension column tables.

    Arguments:
        dimension_column (pandas.Series): The column from the dimension table
            with unique values for `fact_multival_column`.
        fact_table (pandas.DataFrame): The fact table with multivalued data.
        fact_id_column (str): Name of the fact table column that will serve as foreign key
            for the bridge table.
        fact_multival_column (str): Name of the multivalued fact table column.

    Returns:
        bridge_table (pandas.DataFrame): The resulting bridge table, linking each value
            from the fact table's `fact_id_column` to their respective values
            in `dimension_column`.
    '''

    id_dimension_column = 'id_' + dimension_column.name

    bridge_table = pd.DataFrame(columns = [fact_id_column, id_dimension_column])

    fact_multival_rows = []

    for _, fact_row in fact_table.iterrows():

        fact_id = fact_row[fact_id_column]
        fact_multival = fact_row[fact_multival_column]

        dimension_ids = list(
            # Removes duplicates
            set(
                dim_index
                for dim_index, dim_value in dimension_column.items()
                if dim_value in fact_multival
            )
        )

        fact_multival_rows.append(
            pd.DataFrame(
                data = {
                    fact_id_column : [fact_id] * len(dimension_ids),
                    id_dimension_column : dimension_ids
                },
                columns = [fact_id_column, id_dimension_column]
            ).astype(
                {id_dimension_column : "int64"}
            )
        )

    bridge_table = pd.concat(
        objs = fact_multival_rows,
        ignore_index = True 
    )

    return bridge_table


def drop_by_index(
    series: pd.Series,
    index_list: list[int],
    dropna: bool = True
) -> pd.Series:
    '''
    Removes elements from a Series by their index. Can also remove NaN values.

    Arguments:
        series (pandas.Series): The original Series object to have elements removed from.
        index_list (list[int]): The lsit of indices to be removed from `series`.
        dropna (bool): Defaults to `True`. If it should also remove NaN values.
    
    Returns:
        new_series (pandas.Series): The `series` object with all requested elements removed.
    '''

    new_series = series.drop(index_list).reset_index(drop = True)

    if dropna:
        new_series = new_series.dropna(ignore_index = True)

    return new_series


def replace_dimensions_with_ids(
    fact_table: pd.DataFrame,
    dimension_tables: list[pd.Series]
) -> pd.DataFrame:
    '''
    Replaces elements in a fact table with their IDs (indices) from their respective dimension
    tables, replacing unexpected values with None. Note that, in order to work, the Series
    dimensions must have the same name as the DataFrame column they reference.

    Arguments:
        fact_table (pandas.DataFrame): A DataFrame representing a fact table.
        dimension_tables (list[pandas.Series]): A list of all dimensions with which
            to replace columns in `fact_table`.

    Returns:
        new_fact_table (pandas.DataFrame): The fact table with dimension elements replaced
            by their respective IDs.
    '''

    new_fact_table = fact_table.copy(deep = True)

    renamed_id_columns = {}

    for dimension in dimension_tables:

        new_fact_table[dimension.name] = new_fact_table[dimension.name].apply(
            lambda value:
                dimension.index[dimension == value][0]
                if value in dimension.values
                else pd.NA
        ).astype(pd.Int64Dtype())

        renamed_id_columns[dimension.name] = 'id_' + dimension.name

    new_fact_table = new_fact_table.rename(
        columns = renamed_id_columns
    )
    
    return new_fact_table


def write_to_csv(
    data_object: pd.Series | pd.DataFrame,
    destination_path: str,
    file_name: str | None = None,
    prefix: str = "",
    index_label: str | None = None
):
    '''
    Wrapper function for `pandas.[Series|DataFrame].to_csv()`,
    adding the option for a prefix and building the file name
    according to the data object's name. Has no return value.

    Arguments:
        data_object (pd.Series | pd.DataFrame): The data object to be
            exported to the CSV file.
        destination_path (str): The path to the folder to which the file
            will be exported.
        file_name (str): The desired file name. Does not need to include
            the `".csv"` extension.
        index_label (str | None): Same usage as in
            `pandas.[Series|DataFrame].to_csv()`.
        prefix (str): Defaults to `""`. Optional file name prefix.
    '''

    path = destination_path + prefix + file_name + ".csv"

    data_object.to_csv(
        path_or_buf = path,
        index_label = index_label
    )


def conform_multival_series(series: pd.Series) -> pd.Series:
    '''
    Conforms elements from multivalued attributes into list-like objects.
    E.g., a value `"apple, banana"` for a "favorite fruits" attribute will
    be converted into `["apple", "banana"]`. Single objects are placed
    into a list (`"apple"` becomes `["apple"]`), and empty or null-like
    values are replaced by an empty list `[]`.

    Useful for data lake architectures with multivalued attributes.

    Arguments:
        series (pandas.Series): A Series with possible multivalued attributes.

    Returns:
        conformed_series (pandas.Series): The Series object with multivalued
        elements conformed into a list-like value.
    '''

    def parse_value(value):

        if isinstance(value, str):

            if value.startswith("[") and value.endswith("]"):

                try:
                    parsed_list = ast.literal_eval(value)

                    if isinstance(parsed_list, list):
                        return [str.strip(str(item)) for item in parsed_list]

                except (ValueError, SyntaxError):
                    pass

            return [str.strip(item) for item in value.split(',')]

        elif isinstance(value, list):
            return [str.strip(str(item)) for item in value]

        return []
    
    conformed_series = series.apply(parse_value).fillna([])

    return conformed_series
