from supabase import create_client, Client
import streamlit as st
import pandas as pd
url= "https://uzgwhrmgbnvebgshvkfi.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV6Z3docm1nYm52ZWJnc2h2a2ZpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODgwNjU5NTgsImV4cCI6MjAwMzY0MTk1OH0.QogXPI4YOBnZTYTHeM5b1Zurnuu-VYsXmhRBssMW47c"
supabase = create_client(url, key)

def get_noti():
    data = pd.DataFrame(supabase.table("Events").select("*").execute().data)
    data['timestamp'] = pd.to_datetime(data["timestamp"])
    data.sort_values(by='timestamp',ascending=False)

    st.write(data.head(5))
        
        