
import pyodbc 
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import cv2
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import io 
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

#conn =  pyodbc.connect(
#    Trusted_Connection='Yes',
#    Driver='{ODBC Driver 17 for SQL Server}',
#    Server='EVOL',
#    Database='BKLIGHT'
#)

@st.cache_resource
def init_connection():
    return pyodbc.connect(
    Trusted_Connection='Yes',
    Driver='{ODBC Driver 17 for SQL Server}',
    Server='EVOL',
    Database='BKLIGHT'
)
  #  return pyodbc.connect(       
 #   Driver='{ODBC Driver 17 for SQL Server}',
 #   Server='mssql-132219-0.cloudclusters.net,10005',
#    Database='BKLIGHT',
 #   uid = 'EVOL',
#    pwd = 'Evolut10n',
 #   
#    )
conn = init_connection()

def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
# Print results.

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
def login(username, password):
    if run_query("SELECT * FROM dbo.account WHERE dbo.account.username = '" +username+"' AND dbo.account.password = '"+password+"'"):
                
        return True
    return False

# Streamlit app layout


with st.sidebar:
    choose = option_menu("BKLIGHT", ["Home", "Devices", "Controls", "Notifications", "Login"],
                         icons=['house', 'lightbulb', 'menu-button', 'bell','door-open'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#0c0c0c"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )
if 'user' not in st.session_state:
    st.session_state.user = False
if choose == "Home":
    col1, col2 = st.columns( [0.5, 0.5])
    with col1:
        st.markdown('<p style="text-align: center;">Introduce</p>',unsafe_allow_html=True)
    with col2:
        st.markdown('<p style="text-align: center;">BKLIGHT</p>',unsafe_allow_html=True)      
elif choose == "Devices":
    Lights = pd.DataFrame([[21.0043061,105.8373198],[21.0004175,105.839110],[20.9975346,105.844127]], columns= ['lat','lon'])
    st.map(Lights) 
elif choose == "Controls":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Lamp 1")
        st.button(":arrow_left:", on_click=style_button_row, kwargs={
       'clicked_button_ix': 1, 'n_buttons': 5 })
        st.button(":bulb:", on_click=style_button_row, kwargs={
       'clicked_button_ix': 2, 'n_buttons': 5 })
        st.button(":arrow_right:", on_click=style_button_row, kwargs={
       'clicked_button_ix': 3, 'n_buttons': 5 })
        st.button(":gear:", on_click=style_button_row, kwargs={
       'clicked_button_ix': 4, 'n_buttons': 5 })
        st.button(":clock1:", on_click=style_button_row, kwargs={
       'clicked_button_ix': 5, 'n_buttons': 5 })
        
        


        
        st.metric("Temperature", "70 °F", "1.2 °F")
        st.metric("Wind", "9 mph", "-8%")
        st.metric("Humidity", "86%", "4%")
        

    with col2:
        st.header("Lamp 2")
        st.button("◀", on_click=style_button_row, kwargs={
       'clicked_button_ix': 3, 'n_buttons': 4 })
        

    

    with col3:
        st.header("Lamp 3")
        st.image("https://static.streamlit.io/examples/owl.jpg")
elif choose == "Login":   
        
        with st.form("Login"):
            
            if not st.session_state.user:
                st.title('Login Form')

                # Input fields for username and password
                username = st.text_input('Username')
                password = st.text_input('Password', type='password')
                submitted = st.form_submit_button("Login")
                if (submitted or password) and username:
                    
                    st.session_state.user = login(username, password)
                    st.success('Logged in successfully!')
                    st.experimental_rerun()
            else:
                    logout = st.form_submit_button("Logout")
                    if logout:
                        st.session_state.user = False
                        st.experimental_rerun()

                    
            
                       

                        
    

            
    
        