from supabase import create_client, Client
import streamlit as st
import pandas as pd
import pytz
import datetime

url= "https://uzgwhrmgbnvebgshvkfi.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV6Z3docm1nYm52ZWJnc2h2a2ZpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODgwNjU5NTgsImV4cCI6MjAwMzY0MTk1OH0.QogXPI4YOBnZTYTHeM5b1Zurnuu-VYsXmhRBssMW47c"
supabase = create_client(url, key)

def get_noti():

    data1 = pd.DataFrame(supabase.table("Events").select("*").execute().data)
    if  not data1.empty:
        data1['timestamp'] = pd.to_datetime(data1["timestamp"])
        df = data1.sort_values(by='timestamp',ascending=False)
        sorted_df = df.sort_values(by=['lampid', 'timestamp'], ascending=[True, False])

    # Select the first row within each 'lampid' group (the one with the latest timestamp)
        latest_rows = sorted_df.groupby('lampid').head(1)
        

        st.write(latest_rows)

    
    node1 = pd.DataFrame(supabase.table("NodeDeath").select("*").execute().data)
    if not node1.empty:
        node1['time'] = pd.to_datetime(node1["time"])
        node1 = node1.sort_values(by='time',ascending=False)   
        node1 = node1.head(10)
        
        for i in node1.iterrows():    
            if int(i[1].status) == 1:
                st.warning("Lamp {} is dead at {}".format(i[1].address,i[1].time))


    gate = pd.DataFrame(supabase.table("GateAlive").select("*").execute().data)
    if (not gate.empty):
        gate['time'] = pd.to_datetime(gate["time"])
        gate = gate.sort_values(by='time',ascending=False)   
        gate = gate.head(10)
        for i in gate.iterrows():
            if int(i[1].status) == 1:
                st.error("Gateway was dead at {}".format(i[1].time))
        

    
light =  pd.DataFrame(supabase.table("Light").select("*").execute().data)
        