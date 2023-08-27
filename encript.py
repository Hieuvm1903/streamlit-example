
from cryptography.fernet import Fernet
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
import streamlit_app as sa
message = "hello geeks"
key = Fernet.generate_key()

fernet = Fernet(key)

def encodef(stringt):  
    return fernet.encrypt(stringt.encode())
def decodef(stringt):
    return fernet.decrypt(stringt).decode()
@st.cache_resource
def login(username, password):
    username = decodef(encodef(username))
    if pd.DataFrame(sa.supabase.table('Account').select("*").eq('user',username).eq('password',password).execute().data).empty:
        name = ""
        return False, name
    name = pd.DataFrame(sa.supabase.table('Account').select("*").eq('user',username).eq('password',password).execute().data).user[0]
    return True, name
