from snowflake.snowpark import Session
import pandas as pd

def load_data(session: Session, table_name: str) -> pd.DataFrame:
    df = session.table(table_name)
    return df.to_pandas()