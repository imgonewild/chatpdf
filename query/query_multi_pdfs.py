import requests
import os
from dotenv import load_dotenv
import time
import json

load_dotenv()
X_API_KEY = os.getenv('X_API_KEY')
headers = {
    "x-api-key": X_API_KEY,
    "Content-Type": "application/json",
}
url = "https://api.chatpdf.com/v1/chats/message"

# multi_SDS = ['FUEL_DIESEL_FUEL_ALL_GRADES_SDS']
# multi_SDS = ['ACCU_DYNE_TEST_FLUIDS_SDS','ADHESIVE_3M_SPRAY_ADHESIVE_90_MULTI_PURPOSE_SDS','ANTIFREEZE_PETRO_CANADA_SDS','AVERY_MARKS_A_LOT_BLACK_PERMANENT_MARKER_MSDS','CATALYST_CARULITE_200_GRANULAR_CATALYST_SDS','FUEL_DIESEL_FUEL_ALL_GRADES_SDS','CRC_SP_350_MSDS','HYDRAULIC_OIL_AW_68_MSDS','GOJO_ANTIBACTERIAL_PLUM_FOAM_HANDWASH_MSDS']
multi_SDS =['GOJO_ANTIBACTERIAL_PLUM_FOAM_HANDWASH_MSDS']
# multi_SDS = ['CRC_SP_350_MSDS','HYDRAULIC_OIL_AW_68_MSDS','GOJO_ANTIBACTERIAL_PLUM_FOAM_HANDWASH_MSDS']

for SDS in multi_SDS:
    SOURCE_ID = os.getenv(SDS)

    try:
        cnt = 1
        output = ''
        print(f"{SDS}")

        for line in open('./prompt_db.jsonl', 'r'):
            question = json.loads(line)['prompt']

            output += f"{cnt}. {question}\n"    
            print(output)                    
            asking_time = time.time()

            data = {
                "stream": True,
                "sourceId": SOURCE_ID,
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    },
                ],
            }
            response = requests.post(url, json=data, headers=headers, stream=True)
            response.raise_for_status()
            answer = response.text
            output += f"Answer({round(time.time() - asking_time, 2)}s): {answer}\n"

            if response.iter_content == False:
                print("No data received")
                raise Exception("No data received")
            
            output+= "----------------------------------------------------------\n"
            print(answer)
            print("----------------------------------------------------------")
            cnt+=1

        if not os.path.exists(f"output"):
            os.makedirs(f"output")

        with open(f'./output/{SDS}.txt', 'wb') as f:
            f.write(output)
        
    except requests.exceptions.RequestException as error:
        print("Error:", error)