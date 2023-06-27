import requests
import os
from dotenv import load_dotenv

load_dotenv()
X_API_KEY = os.getenv('X_API_KEY')

headers = {
  'x-api-key': X_API_KEY,
  'Content-Type': 'application/json'
}
data = {'url': "https://carleton.ca/mae/wp-content/uploads/Antifreeze1.pdf"}

response = requests.post(
    'https://api.chatpdf.com/v1/sources/add-url', headers=headers, json=data)

if response.status_code == 200:
    print('Source ID:', response.json()['sourceId'])
else:
    print('Status:', response.status_code)
    print('Error:', response.text)