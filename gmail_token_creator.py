
# gmail_api.py
from google_apis import create_service

client_secret_file = 'client_secret.json'
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

# Add an identifier for each account, like the email address
email_identifier = 'harshavardhan.sai.m@gmail.com'  # Change this for each account
#krishna369.m@gmail.com
#harshavardhan.sai.m@gmail.com
#hvm@umich.edu
#harsha.machineni.17ece@bml.edu.in
#harshavardhansai.career@gmail.com

# Pass the email identifier as a prefix to create unique token files
service = create_service(client_secret_file, API_SERVICE_NAME, API_VERSION, SCOPES, prefix=f'_{email_identifier}')
#print(dir(service))