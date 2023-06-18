
import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance

conn =  pyodbc.connect(
    Trusted_Connection='Yes',
    Driver='{ODBC Driver 17 for SQL Server}',
    Server='EVOL',
    Database='BKLIGHT'
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM account")
rows = cursor.fetchall()
print(rows[0][0])
