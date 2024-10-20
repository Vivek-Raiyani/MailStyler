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

st.title("MailStyler")

# Initialize session state variables if not already present
if "prompt_history" not in st.session_state:
    st.session_state.prompt_history = []
if "iteration" not in st.session_state:
    st.session_state.iteration = 3
if "template_history" not in st.session_state:
    st.session_state.template_history = []
if "messages_history" not in st.session_state:
    st.session_state.messages_history = [
        {"role": "system", "content": "You are a Expert in generating HTML Email Template"},
    ]
conn = st.connection("gsheets", type=GSheetsConnection)

# email section
email, btn = st.columns(2, gap='large')
with email:
    mail = st.text_input("Email to get your Template")

with btn:
    mail_btn = st.button("Get Template")

st.write("----------------------------")
# main section
prompt, display = st.columns(2, gap="medium")

with prompt:
    if is_valid_email(mail):
        if st.session_state.iteration > 0:
            # Display prompt history
            st.write("History")
            for history in st.session_state.prompt_history:
                st.write(history)

            st.write("------------------------------------")
            prompt_input = st.text_area(label="Enter the style you want for your mail")

            if st.button("Submit"):
                if prompt_input and prompt_input not in st.session_state.prompt_history:
                    # Append the prompt to prompt history
                    st.session_state.prompt_history.append(prompt_input)
                    st.session_state.iteration -= 1  # Decrement iteration count

                    # Call the LLM function and update template and messages_history
                    template, updated_messages = llm_call(prompt_input, st.session_state.messages_history)

                    # Persist the updated message history
                    st.session_state.messages_history = updated_messages

                    # Add the generated template to template history
                    st.session_state.template_history.append(template)

                    if st.session_state.iteration == 0:
                        st.rerun()  # Rerun the app if iteration limit is reached

        else:
            st.write("You have reached the maximum number of iterations.")
    else:
        st.error("Please enter a valid email address to use the site.")

with display:
    if is_valid_email(mail):
        length = len(st.session_state.template_history)
        if length:
            iteam = length - 1
            latest_template = st.session_state.template_history[iteam]

            # Streamlit input fields
            email_sender = st.secrets['mail']['e_mail']
            email_receiver = mail
            subject = 'Email template'
            body = latest_template
            password = st.secrets['password']['app_password']

            if mail_btn and st.session_state.iteration < 3:
                try:
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
                    st.cache_data.clear()
                    # adding the email, timestamp, and HTML content to Google Sheets
                    df = conn.read(worksheet='User')
                    print('-----------------------------------')
                    print(df)
                    timestamp = date.datetime.now()
                    new_user = {
                        'Email': mail, 
                        'Timestamp': timestamp, 
                        'Html': latest_template  # Store the HTML template content
                    }
                    new_user_df = pd.DataFrame([new_user])
                    print('-------------------------------------')
                    # Append new user to the existing DataFrame
                    df = pd.concat([df, new_user_df], ignore_index=True)
                    print(df)
                    conn.update(worksheet='User', data=df)

                except Exception as e:
                    st.error(f"Error sending email: {e}")

            # Display the latest generated template
            iteam = length - 1
            latest_template = st.session_state.template_history[iteam]
            st.markdown(latest_template, unsafe_allow_html=True)

    else:
        st.write("Sample preview")
        st.markdown("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f4f4f4;
        }

        .signature {
            width: 100%;
            max-width: 600px;
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            display: flex;
            align-items: center;
            font-size: 16px;
        }

        .avatar {
            flex-shrink: 0;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            overflow: hidden;
            margin-right: 20px;
        }

        .avatar img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .info {
            flex-grow: 1;
        }

        .name {
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin: 0;
        }

        .title {
            font-size: 16px;
            color: #666;
            margin: 5px 0;
        }

        .contact {
            font-size: 14px;
            color: #999;
            margin: 3px 0;
        }

        .social {
            margin-top: 10px;
        }

        .social a {
            text-decoration: none;
            color: #007AFF;
            margin-right: 10px;
        }
    </style>
</head>

<body>
    <div class="signature">
        <div class="avatar">
            <img src="[Your Photo URL]" alt="[Your Name]">
        </div>
        <div class="info">
            <p class="name">[Your Name]</p>
            <p class="title">[Your Job Title]</p>
            <p class="contact">[Your Company Name]</p>
            <p class="contact">Email: <a href="mailto:[Your Email]">[Your Email]</a></p>
            <p class="contact">Phone: [Your Phone Number]</p>
            <div class="social">
                <a href="[LinkedIn URL]">LinkedIn</a>
                <a href="[Twitter URL]">Twitter</a>
                <a href="[Facebook URL]">Facebook</a>
            </div>
        </div>
    </div>
</body>

</html>
    """,
    unsafe_allow_html=True)
