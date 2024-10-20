# MailStyler
Transform Your Emails: Craft Impactful Templates in Seconds!

## Description
Introducing MailStyler, the app that revolutionizes your email communication! With MailStyler, users can effortlessly generate professional email templates tailored to various contexts—be it business inquiries, follow-ups, or personal messages. Say goodbye to bland, text-heavy emails and hello to visually appealing, well-structured templates that leave a lasting impression. Customize your Mails with your branding, and enhance your communication effectiveness. Whether you're a busy professional or a student, MailStyle helps you stand out in any inbox!

## Installation
1. Clone the repository:
```
   git clone https://github.com/username/repo.git
```
2. Navigate to the project directory:
```
   cd MailStyler
```
3. Install dependencies:
```
   $ pip install -r requirements.txt
```
4. Add credentilas inside ->
.streamlit/secrets.toml
```
[password]
app_password = "YOUR_APP_PASSWORD_FOR_GMAIL"

[mail]
e_mail= "YOUR_EMAIL"

[api_keys]
api_key= "open_ai_api_key"


[connections.gsheets]
spreadsheet = "<spreadsheet-name-or-url>"
worksheet = "<worksheet-gid-or-folder-id>"  # worksheet GID is used when using Public Spreadsheet URL, when usign service_account it will be picked as folder_id
type = ""  # leave empty when using Public Spreadsheet URL, when using service_account -> type = "service_account"
project_id = ""
private_key_id = ""
private_key = ""
client_email = ""
client_id = ""
auth_uri = ""
token_uri = ""
auth_provider_x509_cert_url = ""
client_x509_cert_url = ""


```

6. Run the app

```
   $ streamlit run streamlit_app.py
 ```
<br>
If you dont want to use Google sheets to store data just comment out **line 86** and you are good to go <br>
Similary you can comment out **line no 76** if you don't want to send email preview
<br>

# To play with it Visit
https://mailstyler.streamlit.app/
