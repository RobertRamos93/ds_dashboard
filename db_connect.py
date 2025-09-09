# db_connect.py
import pandas as pd
from sqlalchemy import create_engine

def load_data():
    try:
        engine = create_engine("postgresql://postgres:Stray@localhost:5432/dashboard_db", client_encoding="utf8")
        df = pd.read_sql_query("SELECT * FROM visa", engine)
        df["importe"] = df["importe"].astype(float)
        text_cols = ["sucursal", "concepto", "mes", "tipo", "estado"]
        for col in text_cols:
            df[col] = df[col].astype(str)
        return df
    except Exception as e:
        print(f"Database connection failed: {e}")
        return pd.DataFrame() 

