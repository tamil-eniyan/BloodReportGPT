
import csv
from PIL import Image
import base64
from io import BytesIO
import pandas as pd
import fitz
import google.generativeai as genai
import tempfile
import os
import pandas as pd
from pathlib import Path
import PIL
import datetime
from pypdf import PdfReader 



now = datetime.datetime.now()


GEMINI_API = "AIzaSyCc0VUQrDJexePvOcz0A9-GEzAB7K6kt88"





generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,

}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel('gemini-pro',safety_settings=safety_settings,generation_config=generation_config)





directory = Path('csv/secondary/Dengue/')
df_list = []
# Get a list of files in the directory and sort them alphabetically
files = sorted(directory.iterdir())

# Iterate over sorted files in the directory
for file_path in files:
    print(file_path)
    try:
        df_list.append(pd.read_csv(file_path))
    except Exception as e:
        print(f"{e}\n")

final = pd.DataFrame()


print(df_list)




print("*************************")
 
final = pd.concat(df_list).reset_index().drop(columns=['index'])



print("******************************8")

print(final)
final.to_csv("csv/one.csv", index=False)












