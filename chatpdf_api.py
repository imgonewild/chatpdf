import requests
from dotenv import load_dotenv
import os

load_dotenv()
X_API_KEY = os.getenv('X_API_KEY')
headers = {
    "x-api-key": X_API_KEY,
    "Content-Type": "application/json",
}
url = "https://api.chatpdf.com/v1/chats/message"

def api_ask_question(source_id, question):
    data = {
        "stream": True,
        "sourceId": source_id,
        "messages": [
            {
                "role": "user",
                "content": question
            },
        ],
    }

    try:        
        response = requests.post(url, json=data, headers=headers, stream=True)
        response.raise_for_status()
        answer = response.text
        return answer  
    except Exception as e:
        return e  

def api_upload_file(path):
    print(path)
    
    file = os.path.splitext(os.path.basename(path))[0] 
    #the symbol [,- %] would make .env malfunction
    SDS = file.replace(", ", "_").replace("-", "_").replace(" ", "_").replace("%", "_").upper()

    files = [
        ('file', ('file', open(path , 'rb'), 'application/octet-stream'))
    ]

    headers = {
        'x-api-key': X_API_KEY
    }

    response = requests.post(
        'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

    if response.status_code == 200:
        source_id = response.json()['sourceId']
        os.environ[SDS] = source_id

        with open(".env", "a") as f:
            f.write(f"\n{SDS} = \"{source_id}\"")   

        msg = f"{SDS} uploaded to chatPDF.com successfully. source_id is: \"{source_id}\" and stored to .env"
        print(msg)
        return msg         
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
        return response.status_code + ', ' + response.text