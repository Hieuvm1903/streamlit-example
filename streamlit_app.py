
import pyodbc 
import streamlit as st

#conn =  pyodbc.connect(
#    Trusted_Connection='Yes',
#    Driver='{ODBC Driver 17 for SQL Server}',
#    Server='EVOL',
#    Database='BKLIGHT'
#)

hide_streamlit_style = """
            <style>
            header {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
	content:'Made by EVOL'; 
	visibility: visible;
	display: block;
	position: relative;
	#background-color: red;
	padding: 5px;
	top: 2px;
}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 



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
# Print results.
st.write(run_query("SELECT * FROM dbo.account "))

def login(username, password):
    if run_query("SELECT * FROM dbo.account WHERE dbo.account.username = '" +username+"' AND dbo.account.password = '"+password+"'"):
                
        return True
    return False

# Streamlit app layout

with st.form("Login"):
    st.title('Login Form')

    # Input fields for username and password
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    submitted = st.form_submit_button("Login")
    if (submitted or password) and username:
        
        if login(username, password):
            st.success('Logged in successfully!')
            # Add your redirect or logic after successful login here
        else:
            st.error('Invalid username or password.')
