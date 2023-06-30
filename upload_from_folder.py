import requests
from dotenv import load_dotenv
import os

load_dotenv()
X_API_KEY = os.getenv('X_API_KEY')

import glob
#single_sds\CRC SILICONE SPRAY 03030 MSDS.pdf

folders = glob.glob("G:\My Drive\Inteplast\SDS\*.pdf")

for path in folders:
    file = os.path.splitext(os.path.basename(path))[0] 
    SDS = file.replace(", ", "_").replace("-", "_").replace(" ", "_").upper()

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
        os.putenv(SDS, source_id)
        print(f"{SDS} uploaded to chatPDF.com successfully. source_id is: \"{source_id}\" and stored to .env")

        with open(".env", "a") as f:
            f.write(f"\n{SDS} = \"{source_id}\"")
            
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)