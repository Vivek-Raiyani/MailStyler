import streamlit as st
from utility import llm_call
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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

prompt, display = st.columns(2, gap="medium")

with prompt:
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

with display:
    length = len(st.session_state.template_history)
    if length:
        iteam= length -1
        latest_template = st.session_state.template_history[iteam]

        # Streamlit input fields
        email_sender = st.secrets['mail']['e_mail']
        email_receiver = st.text_input('Your Email')
        subject = 'Email template'
        body = latest_template
        password = st.secrets['password']['app_password']
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg", "jpeg", "docx"])  # File uploader for attachments

        if st.button("Send Email"):
            try:
            # Create the MIMEMultipart object
                msg = MIMEMultipart()
                msg['From'] = email_sender
                msg['To'] = email_receiver
                msg['Subject'] = subject

                # Attach the HTML content to the message
                msg.attach(MIMEText(body, 'html'))  # Attach the HTML body as 'html'

                # Handling file attachment
                if uploaded_file is not None:
                    file_name = uploaded_file.name

                    # Read file data
                    file_data = uploaded_file.read()

                    #   Create a MIMEBase object and set its payload to the file data
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(file_data)
            
                    # Encode the file data to base64
                    encoders.encode_base64(part)
            
                    # Add the header with the file name
                    part.add_header('Content-Disposition', f'attachment; filename="{file_name}"')

                    # Attach the file part to the message
                    msg.attach(part)

                # SMTP server setup and sending the email
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()  # Secure the connection
                server.login(email_sender, password)  # Login using provided credentials
                server.sendmail(email_sender, email_receiver, msg.as_string())  # Send the email
                server.quit()  # Terminate the SMTP session

                # Success message
                st.success('Email sent successfully with attachment!')

            except Exception as e:
                # Error message
                st.error(f"Error sending email: {e}")



        # Display the latest generated template
        iteam= length - 1
        latest_template = st.session_state.template_history[iteam]
        st.markdown(latest_template, unsafe_allow_html=True)
