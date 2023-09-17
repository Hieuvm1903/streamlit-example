
import streamlit as st
import binascii
import os
import pandas as pd
import data 
import struct, os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
encoding = 'utf-8'
key = ('abcd'*8).encode('utf-8')
with open('key.txt', 'rb') as key_file:
    nonce = key_file.read()
    if not nonce :
        nonce = os.urandom(8)       
        with open('key.txt', 'wb') as key_file:
            key_file.write(nonce)   
counter = 0
full_nonce = struct.pack("<Q", counter) + nonce
algorithm = algorithms.ChaCha20(key, full_nonce)
cipher = Cipher(algorithm, mode=None)
encryptor = cipher.encryptor()
decryptor = cipher.decryptor()
def encodef(stringt):  
    str = binascii.unhexlify((stringt).encode(encoding))
    str = encryptor.update(str)
    str = binascii.hexlify(str)
    return str.decode(encoding)
def decodef(stringt):
    str = binascii.unhexlify(stringt.encode(encoding)) 
    str = decryptor.update(str)
    str = binascii.hexlify(str)
    return str.decode(encoding)
df = pd.DataFrame(data.supabase.table('Account').select("*").execute().data)
for row in df.iterrows():
    #data.supabase.table('Account').update({'encript':encodef(row[1]['password'])}).eq('id',row[1]['id']).execute()
    row
@st.cache_resource

def login(username, password):
    #pw = decodef(encodef(password))
    if pd.DataFrame(data.supabase.table('Account').select("*").eq('user',username).eq('password',password).execute().data).empty:
        name = ""
        return False, name
    name = pd.DataFrame(data.supabase.table('Account').select("*").eq('user',username).eq('password',password).execute().data).user[0]
    return True, name
