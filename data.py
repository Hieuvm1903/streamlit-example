from supabase import create_client, Client
import streamlit as st
import pandas as pd
import pytz
import datetime

url= "https://uzgwhrmgbnvebgshvkfi.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV6Z3docm1nYm52ZWJnc2h2a2ZpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODgwNjU5NTgsImV4cCI6MjAwMzY0MTk1OH0.QogXPI4YOBnZTYTHeM5b1Zurnuu-VYsXmhRBssMW47c"
supabase = create_client(url, key)
timezone = pytz.timezone("Asia/Ho_Chi_Minh")  # Replace with your desired timezone
def get_noti():
    col1,col2 = st.columns(2)
    with col1:

        data1 = pd.DataFrame(supabase.table("Events").select("*").execute().data)
        if  not data1.empty:
            
            data1['timestamp'] = pd.to_datetime(data1["timestamp"])
            data1['timestamp'] = data1.apply(lambda row: row['timestamp'].astimezone(timezone), axis = 1)
            df = data1.sort_values(by='timestamp',ascending=False)
            sorted_df = df.sort_values(by=['lampid', 'timestamp'], ascending=[True, False])

        # Select the first row within each 'lampid' group (the one with the latest timestamp)
            latest_rows = sorted_df.groupby('lampid')[ 'timestamp'].idxmax()        
            st.title('Real Data')
            st.write(df.loc[latest_rows].set_index(['lampid']).drop(['id'],axis='columns'))
    with col2:
        fake = pd.DataFrame(supabase.table("Fake").select("*").execute().data)
        if  not fake.empty:
            
            fake['timestamp'] = pd.to_datetime(fake["timestamp"])
            fake['timestamp'] = fake.apply(lambda row: row['timestamp'].astimezone(timezone), axis = 1)
            df = fake.sort_values(by='timestamp',ascending=False)
            sorted_df = df.sort_values(by=['lampid', 'timestamp'], ascending=[True, False])

        # Select the first row within each 'lampid' group (the one with the latest timestamp)
            latest_rows = sorted_df.groupby('lampid')[ 'timestamp'].idxmax()        
            st.title('Demo Data')
            st.write(df.loc[latest_rows].set_index(['lampid']).drop(['id'],axis='columns'))



        gate = pd.DataFrame(supabase.table("GateAlive").select("*").execute().data)
        if (not gate.empty):
            gate['time'] = pd.to_datetime(gate["time"])
            gate = gate.sort_values(by='time',ascending=False)   
            datime = datetime.datetime.now().astimezone(tz= timezone)
            maxtime = max(gate["time"]).astimezone(tz = timezone)
            diff = datime - maxtime
            if diff.total_seconds() >=120:
                st.error("Gateway was dead at {}".format(maxtime.strftime("%Y-%m-%d %H:%M:%S %z")))
    
    node1 = pd.DataFrame(supabase.table("NodeDeath").select("*").execute().data)
    if not node1.empty:
        node1['time'] = pd.to_datetime(node1["time"])
        node1 = node1.sort_values(by='time',ascending=False)   
        node1 = node1.head(10)      
        for i in node1.iterrows():    
            dt = i[1].time.astimezone(tz=timezone)
            if int(i[1].status) == 0:
                st.warning("Lamp {} was dead at {}: lost connection".format(i[1].address,dt.strftime("%Y-%m-%d %H:%M:%S %z")))

            elif int(i[1].status) == 1:
                st.warning("Lamp {} was dead at {}: current too low".format(i[1].address,i[1].time.strftime("%Y-%m-%d %H:%M:%S %z")))

            elif int(i[1].status) == 1:
                st.warning("Lamp {} was dead at {}: current too high".format(i[1].address,i[1].time.strftime("%Y-%m-%d %H:%M:%S %z")))

    
                
        

    
light =  pd.DataFrame(supabase.table("Light").select("*").execute().data)
        