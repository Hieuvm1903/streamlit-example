import streamlit as st
import numpy as np
import pandas as pd
from supabase import create_client, Client
from encript import *
from light import Light_Street
from mqtt_tls import *

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
def control_generate(i, b = True):
    if b:
        st.header("Lamp " +str(i)+" :bulb:")
    else:
        st.header("All" + ":bulb:")
        #brightness modification 
    key = "slider"+str(i)    
    def bright_change():
       bright_client(str(i)+" "+ str(st.session_state[key]))
    def slide_change(value):
        st.session_state[key] = value
    if key not in st.session_state:
        st.session_state[key] = 100   
    bright = st.slider("🔆Brightness",min_value=0, max_value=100,value= 100,step = 5,key = key,on_change = bright_change)   
    lamp1_state = st.button("⚙️ On/Off  ", on_click=slide_change,kwargs={"value":100 if bright ==0 else 0},key = "turn"+str(i))
    st.write("---")
    if lamp1_state:
        if st.session_state[key] > 0:
            
            on_off_client(s = str(i)+" 0")
        else:
            
            on_off_client(s = str(i)+" 1")

        #setting time control
    
    with st.container():
        def format(s):
            if s == '1':
                return 'On'
            else:
                return 'Off'
        time = st.button(":clock1:" , on_click=style_button_row, kwargs={
            'clicked_button_ix': 2, 'n_buttons': 6 },key = "time"+str(i))
        t1 = st.time_input('🕐Time',step = 300, key = str(i)+'time1')
        t2 = st.time_input('🕐Time',step = 300, key = str(i)+'time2')
        t3 = st.time_input('🕐Time',step = 300, key = str(i)+'time3')
        t4 = st.time_input('🕐Time',step = 300, key = str(i)+'time4')
        if time:
            time_setting(str(i)+" "+ t1.strftime("%H %M")+ " "+ t2.strftime("%H %M")+" "+ t3.strftime("%H %M")+" "+ t4.strftime("%H %M"))
            
    #st.metric("Temperature", "72 °F", "1.5 °F")
    #st.metric("Wind", "9 mph", "-5%")
    #st.metric("Humidity", "86%", "6%")
