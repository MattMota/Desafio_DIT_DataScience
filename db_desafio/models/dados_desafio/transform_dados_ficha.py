import pandas as pd
import dbt 

def model(dbt, session):

    # Load the seeded data
    df = dbt.ref("dados_ficha_a_desafio").to_pandas()

    return df
