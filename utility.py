from openai import OpenAI
import streamlit as st
import re
import os
import tempfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from streamlit_gsheets import GSheetsConnection

client = OpenAI(api_key=st.secrets['api_keys']['api_key'])
conn = st.connection("gsheets", type=GSheetsConnection)

def html_parse(content):
    html_content=content.split("html",maxsplit=1)
    html_content=html_content[1]
    html_content=html_content.split("```")
    print(html_content[0])
    return html_content[0]


def llm_call(query , messages_history):
    prompt={"role": "user", "content": f"{query}"}
    messages_history.append(prompt)
    print(messages_history)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_history
    )

    #print(completion.choices[0].message.content)
    content=html_parse(completion.choices[0].message.content)
    messages_history.append({
        "role" : "assistant",
        "content" : content
    })    
    print(messages_history)
    return content,messages_history

def is_valid_email(email):
    """Check if the email is valid using a simple regex pattern."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def update_sheets(user_dic):              
    new_user_df=pd.DataFrame([user_dic])
    df = conn.read(worksheet='User')
    df = pd.concat([df, new_user_df], ignore_index=True)
    conn.update(worksheet='User', data=df)

def send_mail(mail,latest_template):
    email_sender = st.secrets['mail']['e_mail']
    email_receiver = mail
    subject = 'Email template'
    body = latest_template
    password = st.secrets['password']['app_password']
    # Create the MIMEMultipart object
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject

    # Attach the HTML content to the message as HTML body
    msg.attach(MIMEText(body, 'html'))

    # Create temporary HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
        tmpfile.write(body.encode('utf-8'))
        temp_html_file_path = tmpfile.name

    # Attach the HTML file to the email
    with open(temp_html_file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="template.html"')
        msg.attach(part)

    # SMTP server setup and sending the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Secure the connection
    server.login(email_sender, password)  # Login using provided credentials
    server.sendmail(email_sender, email_receiver, msg.as_string())  # Send the email
    server.quit()  # Terminate the SMTP session

    # Success message
    st.success('Email sent successfully with the HTML attachment!')

    # Clean up temporary HTML file
    os.remove(temp_html_file_path)