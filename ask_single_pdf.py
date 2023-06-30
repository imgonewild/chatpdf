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

multi_sds = ['GOJO_ANTIBACTERIAL_PLUM_FOAM_HANDWASH_MSDS']

query_jsonl = './SDS_17_Qs.jsonl'
# multi_sds = ['HYDRAULIC_OIL_AW_68_MSDS','GOJO_ANTIBACTERIAL_PLUM_FOAM_HANDWASH_MSDS']

def auto_query():
    for line in open(query_jsonl, 'r'):
        question = json.loads(line)['prompt']

        output += f"{cnt}. {question}\n"    
        print(output)       

        asking_time = time.time()
        answer = api(question)

        output += f"Answer({round(time.time() - asking_time, 2)}s): {answer}\n"        
        output += "----------------------------------------------------------\n"
        print(answer)
        print("----------------------------------------------------------")
        cnt+=1 

def write_output_txt():
    if not os.path.exists(f"output"):
        os.makedirs(f"output")

    with open(f'./output/{SDS}.txt', 'w') as f:
        f.write(output)    

def api(question):
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

    if response.iter_content == False:
        print("No data received")
        raise Exception("No data received")

    return answer  

def ask_manually():
    while 1:
        print("\nQuestion:")
        question = input()
        print(api(question))

for SDS in multi_sds:
    SOURCE_ID = os.getenv(SDS)
    try:
        cnt = 1
        output = ''
        print(f"{SDS}")
        ask_manually()
        # auto_query()
        # write_output_txt()
        
    except requests.exceptions.RequestException as error:
        print("Error:", error)