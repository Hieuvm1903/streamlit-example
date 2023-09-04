
import pyodbc 
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import pandas as pd
import plotly.express as px
import folium
from supabase import create_client, Client
from streamlit_folium import st_folium, folium_static

from encript import *
from light import Light_Street
from map import *
from mqtt_tls import *
from control import *
from data import *
#conn =  pyodbc.connect(
#    Trusted_Connection='Yes',
#    Driver='{ODBC Driver 17 for SQL Server}',
#    Server='EVOL',
#    Database='BKLIGHT'
#)
#conn =  pyodbc.connect(
#    Trusted_Connection='Yes',
#    Driver='{ODBC Driver 17 for SQL Server}',
#    Server='EVOL',
#    Database='BKLIGHT'
#)
# def init_connection():
#     return pyodbc.connect(
#     Trusted_Connection='Yes',
#     Driver='{ODBC Driver 17 for SQL Server}',
#     Server='EVOL',
#     Database='BKLIGHT'
# )
# def init_connection():
#    return pyodbc.connect(       
#    Driver='{ODBC Driver 17 for SQL Server}',
#    Server='mssql-132219-0.cloudclusters.net,10005',
#    Database='BKLIGHT',
#    uid = 'EVOL',
#    pwd = 'Evolut10n',   
#    )
# conn = init_connection()
# def run_query(query):
#     with conn.cursor() as cur:
#         cur.execute(query)
#         return cur.fetchall()
# # Print results.
# def login(username, password):
#     if run_query("SELECT * FROM dbo.account WHERE dbo.account.username = '" +username+"' AND dbo.account.password = '"+password+"'"):               
#         return True
#     return False 
#Streamlit app layout


# sheet_id = "1XqOtPkiE_Q0dfGSoyxrH730RkwrTczcRbDeJJpqRByQ"
# sheet_name ="sample_1"
# urlsheet = "https://docs.google.com/spreadsheets/d/1zu6W388L9CaLzzrbQtkgbQQwj0-CmwiEO1hwvF4D4m0/edit#gid=0"
# url_1 = urlsheet.replace('/edit#gid=', '/export?format=csv&gid=')
# sheetbase = pd.read_csv(url_1)


url= "https://uzgwhrmgbnvebgshvkfi.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV6Z3docm1nYm52ZWJnc2h2a2ZpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODgwNjU5NTgsImV4cCI6MjAwMzY0MTk1OH0.QogXPI4YOBnZTYTHeM5b1Zurnuu-VYsXmhRBssMW47c"
supabase = create_client(url, key)

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


if 'user' not in st.session_state:
    st.session_state.user = False
if 'username' not in st.session_state:
    st.session_state.username = ""
stop()
with st.sidebar:
    choose = option_menu("BKLIGHT", ["Home", "Devices", "Controls", "Notifications", "Login"],
                         icons=['house', 'lightbulb', 'menu-button', 'bell','door-open'],
                         menu_icon="app-indicator", default_index=0,key='menu_4',
                         styles={
        "container": {"padding": "5!important", "background-color": "#0c0c0c"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"}
    }
    )

     
if choose == "Home":
    col1, col2 = st.columns( [0.5, 0.5])
    with col1:
        st.markdown('<p style="text-align: center;">Introduce</p>',unsafe_allow_html=True)
        
    with col2:
        st.markdown('<p style="text-align: center;">BKLIGHT</p>',unsafe_allow_html=True)  
    
elif choose == "Devices":
    if st.session_state.user:
        show()
    
elif choose == "Notifications":
    if st.session_state.user:
        #start()
        get_noti()
          
        
    #print("true")
    
elif choose == "Controls":   
    if st.session_state.user: 
        i = 0
        for col in st.columns(5):
            i = i+1
            with col:
              control_generate(i)
   
elif choose == "Login":          
        with st.form("Login"):            
            if not st.session_state.user:
                st.title('Login Form')
                # Input fields for username and password
                username = st.text_input('Username')
                password = st.text_input('Password', type='password')
                submitted = st.form_submit_button("Login")
                if (submitted or password) and username:                    
                    st.session_state.user = login(username, password)[0]
                    st.session_state.username = login(username, password)[1]                    
                    st.success('Logged in successfully!')
                    st.experimental_rerun()
            else:                    
                    st.title("Welcome " +st.session_state.username)
                    logout = st.form_submit_button("Logout")
                    if logout:
                        st.session_state.user = False
                        st.session_state.username = ""
                        st.experimental_rerun()







            
                       

                        
    

            
    
        