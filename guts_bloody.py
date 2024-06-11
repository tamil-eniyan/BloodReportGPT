from pathlib import Path
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





def get_gemini_response(pdf_path,query):
    try :
        text = ""
        reader = PdfReader(pdf_path) 
        no_page = len(reader.pages)
        print(no_page)
        for i in range(no_page):
            text = f"{text}\n{reader.pages[i].extract_text()}" 
            print(text) 
           
        #response = model.generate_content([f"here you have a blood report , {query} {format}" ,blood_report])
        return text







 


    except Exception as e:
        logs_errors(f"\n[-]get_gemini_response | {e} ")
        print(f"[-]Error at get_gemini_ressponse : {e} ")
        return ("errorcodered")



    



def logs_errors(e):
    print(f"[*]Loging error : {e}")
    
    with open(error_log_path, 'a') as f:
        f.write(f"|{now} | {e} |dir_path =  {dir_path} | pdf_path = {pdf_path} | pdf_name = {pdf_name}")
        f.close()
    


#***********************************************8Driver*********************************************
error_log_path = f"errorlogCreateDataset[{now}].txt" 
with open(error_log_path, 'a') as f:
        f.write(f"{now}")
        f.close()


dir_path = ["images/Datasets/Malaria/Malaria/", "images/Datasets/Dengue/Dengue/","images/Datasets/Leptospirosis/Leptospirosis/","images/Datasets/ScrubTyphus/ScrubTyphus/"]
text_path = ["text/Malaria/","text/Dengue/","text/Leptospirosis/","text/ScrubTyphus/"]
pdf_path = ""
pdf_name = ""
query= "give the response in .csv ,ignore the name field, any notes and other stuffs in the report, only consider the tests from hematology report with the format of "
i = 1
for k in range(4):
    for pdf_name in os.listdir(dir_path[k]):
        try:
        
            print(f"[!]Starting the Extraction Process : {i}")
            pdf_path = dir_path[k] + pdf_name
    
            print(f"[$]Variable names | dir_path = {dir_path[k]} | pdfpath = {pdf_path} | pdfname = {pdf_name}")
            print("[!]Calling the Gemeni function")
    
            bloody_csv = (get_gemini_response(pdf_path,query))
        
            if(bloody_csv != "errorcodered"):
    
                filename = (f"{text_path[k]}{Path(pdf_path).stem}.txt")
                print(f"Saving to file name : {filename}")

                file = open(filename,"w")
                file.writelines(bloody_csv)
                file.close()
                print(f"[+]Extraction process Finished : {i}")
            else:
                pass
            i=i+1



            
        except Exception as e:
            logs_errors(f"\n[-]main | {e} ")
            i=i+1
            pass







    

















