
import pyodbc 
import streamlit as st
st.set_page_config(page_icon="random",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"})    
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
import numpy as np
import pandas as pd

from encript import *
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
    
    
    html.html("""
<iframe src="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Fphoto%2F%3Ffbid%3D207126528879455%26set%3Dgm.6181781221870440%26idorvanity%3D1418821624833114&width=750&show_text=true&height=692&appId" width="750" height="692" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowfullscreen="true" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"></iframe>

""",height = 700)
    
    html.html("""
<div id="fb-root"></div>
<script async defer crossorigin="anonymous" src="https://connect.facebook.net/vi_VN/sdk.js#xfbml=1&version=v17.0" nonce="Ik00TEAa"></script>
                                   
<div class="fb-comments" data-href="https://iot-bklight.streamlit.app" data-width="750" data-numposts="5"></div>          
          
          """,
    height=500,width=900)       
    
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
        light = data.light.sort_values("id")
        a = light.shape[0]//3
        b = light.shape[0]%3
        for i in range(a):
            with st.container():
                j = 0
                for col in st.columns(3,gap = 'medium'):                   
                    l = light.iloc[i*3+j]
                    j = j+1
                    with col:
                        control_generate(int(l.id))
            "---"
                
        if b>0:
            with st.container(): 
                j = 0
                for col in st.columns(3,gap='medium'):
                    l = light.iloc[a*3+j]
                    j = j+1
                    with col:
                        control_generate(int(l.id))
                    if j == b:
                        break
                    
                    

        
   
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







            
                       

                        
    

            
    
        