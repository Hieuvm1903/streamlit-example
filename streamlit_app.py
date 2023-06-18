
import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
import streamlit as st

#conn =  pyodbc.connect(
#    Trusted_Connection='Yes',
#    Driver='{ODBC Driver 17 for SQL Server}',
#    Server='EVOL',
#    Database='BKLIGHT'
#)


@st.cache_resource
def init_connection():
    return pyodbc.connect(
        
        Driver='{ODBC Driver 17 for SQL Server}',
    Server='mssql-132219-0.cloudclusters.net,10005',
    Database='BKLIGHT',
    uid = 'EVOL',
    pwd = 'Evolut10n',
    
    )

conn = init_connection()


@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from account;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
