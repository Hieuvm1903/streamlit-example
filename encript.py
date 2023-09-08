
from cryptography.fernet import Fernet
import streamlit as st

import pandas as pd
import data 
key = Fernet.generate_key()

fernet = Fernet(key)

def encodef(stringt):  
    return fernet.encrypt(stringt.encode())
def decodef(stringt):
    return fernet.decrypt(stringt).decode()
@st.cache_resource
def login(username, password):
    username = decodef(encodef(username))
    if pd.DataFrame(data.supabase.table('Account').select("*").eq('user',username).eq('password',password).execute().data).empty:
        name = ""
        return False, name
    name = pd.DataFrame(data.supabase.table('Account').select("*").eq('user',username).eq('password',password).execute().data).user[0]
    return True, name
