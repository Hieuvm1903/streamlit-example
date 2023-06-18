
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

rows = run_query("select * from dbo.account where username = 'hieuvm1903'")
st.write(rows)

# Print results.
def login(username, password):
    if run_query("SELECT * FROM dbo.account WHERE dbo.account.username = '" +username+"' AND dbo.account.password = '"+password+"'"):
                
        return True
    return False

# Streamlit app layout


st.title('Login Form')

# Input fields for username and password
username = st.text_input('Username')
password = st.text_input('Password', type='password')

# Login button
if st.button('Login'):
    if login(username, password):
        st.success('Logged in successfully!')
        # Add your redirect or logic after successful login here
    else:
        st.error('Invalid username or password.')