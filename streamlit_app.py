
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
        Trusted_Connection="Yes",
        Driver='{ODBC Driver 17 for SQL Server}',
    Server=st.secrets.servers.Server,
    Database=st.secrets.servers.Database
    )

conn = init_connection()


cursor = conn.cursor()
cursor.execute("SELECT * FROM account")
rows = cursor.fetchall()
st.write(rows[0])
