import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def statistics():
    cnx = sqlite3.connect('D:\Ribhav language\python_class\python_class_project\Test-2\instance\db.sqlite3')
    df = pd.read_sql_query("SELECT * FROM owner", cnx)
    a=df['customer_username'].nunique()
    b=len(df)
    c=df['customer_product_heading'].value_counts().sort_values().head(7).index
    df['customer_product_price']=pd.to_numeric(df['customer_product_price'])
    d=df['customer_product_price'].sum()
    return a,b,c,d

def dgraph1():
    cnx = sqlite3.connect('D:\Ribhav language\python_class\python_class_project\Test-2\instance\db.sqlite3')
    df = pd.read_sql_query("SELECT * FROM owner", cnx)
    df['customer_product_price']=pd.to_numeric(df['customer_product_price'])
    table = pd.pivot_table(df, values='customer_product_price', index=['customer_product_category_page'],aggfunc=np.sum)
    table=table.sort_values(by="customer_product_price",ascending=False)
    return table