import datetime as date
import pandas as pd
import streamlit as st
from utility import llm_call, is_valid_email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from streamlit_gsheets import GSheetsConnection
import tempfile
import os
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(worksheet='User')
print('-----------------------------------')
print(df)
timestamp = date.datetime.now()
new_user = {
    'Email': "mail", 
    'Timestamp': timestamp, 
    'Html': "html"  # Store the HTML template content
}
new_user_df = pd.DataFrame([new_user])
print('-------------------------------------')
# Append new user to the existing DataFrame
df = pd.concat([df, new_user_df], ignore_index=True)
print(df)
conn.update(worksheet='User', data=df)