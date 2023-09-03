
import pyodbc 
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import pandas as pd
import plotly.express as px
import folium
import supabase as sb
from supabase import create_client, Client
from streamlit_folium import st_folium, folium_static

import noti
from encript import *
from light import Light_Street
import map
from map import *
import mqtt_tls
from mqtt_tls import *
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


sheet_id = "1XqOtPkiE_Q0dfGSoyxrH730RkwrTczcRbDeJJpqRByQ"
sheet_name ="sample_1"
urlsheet = "https://docs.google.com/spreadsheets/d/1zu6W388L9CaLzzrbQtkgbQQwj0-CmwiEO1hwvF4D4m0/edit#gid=0"
url_1 = urlsheet.replace('/edit#gid=', '/export?format=csv&gid=')
sheetbase = pd.read_csv(url_1)


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

    



def style_button_row(clicked_button_ix, n_buttons):

    def get_button_indices(button_ix):
        return {
            'nth_child': button_ix,
            'nth_last_child': n_buttons - button_ix + 1
        }

    clicked_style = """
    div[data-testid*="stHorizontalBlock"] > div:nth-child(%(nth_child)s):nth-last-child(%(nth_last_child)s) button {
        border-color: rgb(255, 75, 75);
        color: rgb(255, 75, 75);
        box-shadow: rgba(255, 75, 75, 0.5) 0px 0px 0px 0.2rem;
        outline: currentcolor none medium;
    }
    """
    unclicked_style = """
    div[data-testid*="stHorizontalBlock"] > div:nth-child(%(nth_child)s):nth-last-child(%(nth_last_child)s) button {
        pointer-events: none;
        cursor: not-allowed;
        opacity: 0.65;
        filter: alpha(opacity=65);
        -webkit-box-shadow: none;
        box-shadow: none;
    }
    """
    style = ""
    for ix in range(n_buttons):
        ix += 1
        if ix == clicked_button_ix:
            style += clicked_style % get_button_indices(ix)
        else:
            style += unclicked_style % get_button_indices(ix)
    st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)
if 'user' not in st.session_state:
    st.session_state.user = False
if 'username' not in st.session_state:
    st.session_state.username = ""

with st.sidebar:
    choose = option_menu("BKLIGHT", ["Home", "Devices", "Controls", "Notifications", "Login"],key="home1",
                         icons=['house', 'lightbulb', 'menu-button', 'bell','door-open'],
                         menu_icon="app-indicator", default_index=0,
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
        st.write(sheetbase)    
    
elif choose == "Devices":
    show()
    
elif choose == "Notifications":
    test()   
    #print("true")
    
elif choose == "Controls":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Lamp 1a :bulb:")
        st.slider("brightness",min_value=0, max_value=100,value= 100,step = 5, key = 0)
        st.button(":gear:", on_click=style_button_row, kwargs={
       'clicked_button_ix': 1, 'n_buttons': 6 },key = 1)
        st.button(":clock1:", on_click=style_button_row, kwargs={
       'clicked_button_ix': 2, 'n_buttons': 6 },key = 2)
        st.metric("Temperature", "72 °F", "1.5 °F")
        st.metric("Wind", "9 mph", "-5%")
        st.metric("Humidity", "86%", "6%")
        

    with col2:
        st.header("Lamp 2 :bulb:")
        st.slider("brightness",min_value=0, max_value=100,value= 100,step = 5, key = 'sl2')
        st.button(":gear:", on_click=style_button_row, kwargs={
       'clicked_button_ix': 3, 'n_buttons': 6 },key = 3)
        st.button(":clock1:", on_click=style_button_row, kwargs={
       'clicked_button_ix': 4, 'n_buttons': 6 },key = 4)
        st.metric("Temperature", "70 °F", "1.2 °F")
        st.metric("Wind", "9 mph", "-8%")
        st.metric("Humidity", "86%", "4%")
        

    

    with col3:
        st.header("Lamp 3 :bulb:")
        st.slider("brightness",min_value=0, max_value=100,value= 100,step = 5,key = 'st3')
        st.button(":gear:", on_click=style_button_row, kwargs={
       'clicked_button_ix': 5, 'n_buttons': 6 },key = 5)
        st.button(":clock1:", on_click=style_button_row, kwargs={
       'clicked_button_ix': 6, 'n_buttons': 6 }, key =6)
        st.metric("Temperature", "71 °F", "1.2 °F")
        st.metric("Wind", "9 mph", "-7%")
        st.metric("Humidity", "86%", "5%")
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







            
                       

                        
    

            
    
        