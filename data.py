from supabase import create_client, Client
import streamlit as st
import pandas as pd
url= "https://uzgwhrmgbnvebgshvkfi.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV6Z3docm1nYm52ZWJnc2h2a2ZpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODgwNjU5NTgsImV4cCI6MjAwMzY0MTk1OH0.QogXPI4YOBnZTYTHeM5b1Zurnuu-VYsXmhRBssMW47c"
supabase = create_client(url, key)

def get_noti():
    data1 = pd.DataFrame(supabase.table("Events").select("*").execute().data)
    data1['timestamp'] = pd.to_datetime(data1["timestamp"])
    data1.sort_values(by='timestamp',ascending=False)   
    st.write(data1.head(5))

    node1 = pd.DataFrame(supabase.table("NodeDeath").select("*").execute().data)
    node1['time'] = pd.to_datetime(node1["time"])
    node1.sort_values(by='time',ascending=False)   
    node1 = node1.head(10)
    for i in node1.iterrows():
     
        if int(i[1].status) == 1:
            st.warning("Lamp {} is dead at {}".format(i[1].address,i[1].time))


    gate = pd.DataFrame(supabase.table("GateAlive").select("*").execute().data)
    gate['time'] = pd.to_datetime(gate["time"])
    gate.sort_values(by='time',ascending=False)   
    gate = gate.head(10)
    for i in gate.iterrows():
        if int(i[1].status) == 1:
            st.warning("Node is dead at {}".format(i[1].time))
        

    
light =  pd.DataFrame(supabase.table("Light").select("*").execute().data)
        