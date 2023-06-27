import requests
from dotenv import load_dotenv
import os

load_dotenv()
X_API_KEY = os.getenv('X_API_KEY')
# SDS_filename = "CATALYST Carulite-200-granular-catalyst SDS"
SDS_filenames = ["CLEANER,  BioRem-2000-Surface-Cleaner SDS", "CRC SP-350 MSDS"]

import glob
#single_sds\CRC SILICONE SPRAY 03030 MSDS.pdf

folders = glob.glob("G:\My Drive\Inteplast\SDS\*.pdf")

# print(folders[0])
# filename_w_ext = os.path.basename(folders[0])
# filename = os.path.splitext(filename_w_ext)[0]
# print(filename)

for path in folders:
    # file_w_ext = os.path.basename(file)
    # file = os.path.splitext(filename_w_ext)[0]

    # path = f'G:\My Drive\Inteplast\SDS\{file}.pdf'
    # path = file
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