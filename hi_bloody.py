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





def get_gemini_response(text):
    try :
        
        csv_format = "\nTest,Result,Biological Reference Interval\nESR,13 mm/hr,0 - 20\nHAEMOGLOBIN,14.1 g/dL,13.0-17.0\nHAEMATOCRIT,38.6 %,40.0-50.0\nRBC COUNT,4.75 x 10^6/µL,4.5-5.5\nMCV,81.1 fl,83-101\nMCH,29.6 pg,27-32\nMCHC,36.5 g/dL,31.5-34.5\nRDW,13.6 %,11.6-14.0\nPLATELET COUNT,19.0 x 10³/µL,150 - 400\nTOTAL WBC,3.9 x 10³/µL,4.0-10.0\nMPV,9.7 fL,7.5 - 11\nPCT,0.018 %,0.15 - 0.5\nPDW,17.0 %,11 - 18\nPROTHROMBIN TIME (PT),16.8 Sec,9.5 - 12.6\nINR,1.57\nAPTT,38.7 Sec,27.1 - 34.2"


        data = ""
        response = model.generate_content(f"gather the important test results from the below data  and give it in a csv file(just give me the csv with columns Test,Result,Unit,Biological Reference ) \n  \n\n\n\n\n{text}")

        print(response.text)

           
        data = response.text
        data = data.replace("'''","")
        data = data.replace("'''csv","")
        data =  data.replace("csv","")


        return data







 


    except Exception as e:
        logs_errors(f"\n[-]get_gemini_response | {e} ")
        print(f"[-]Error at get_gemini_ressponse : {e} ")
        return ("errorcodered")



def get_sample_ID(text):
    try:
        response = model.generate_content(f"get the sample Id from the text below (just give me the sample id o need of any other data )\n  \n\n\n\n\n{text}")

        print(response.text)

           
        data = response.text
        data = data.replace("'''","")
        head, sep, tail = data.partition('/')
        if head == data.replace("/",""):
            return data
        else:    
            return head 




    except Exception as e:
        logs_errors(f"\n[-]get_sample_ID | {e} ")
        print(f"[-]Error at get_sample_ID : {e} ")
        return ("errorcodered")







def logs_errors(e):
    print(f"[*]Loging error : {e}")
    
    with open(error_log_path, 'a') as f:
        f.write(f"|{now} | {e} |dir_path =  {dir_path} | pdf_path = {txt_path} | pdf_name = {txt_name}")
        f.close()
    


#***********************************************8Driver*********************************************
error_log_path = f"errorlogCreateDataset[{now}].txt" 
with open(error_log_path, 'a') as f:
        f.write(f"{now}")
        f.close()


dir_path = ["text/Leptospirosis/","text/ScrubTyphus/"]
csv_path = ["csv/secondary/Leptospirosis/","csv/secondary/ScrubTyphus/"]
txt_path = ""
txt_name = ""
query= "give the response in .csv ,ignore the name field, any notes and other stuffs in the report, only consider the tests from hematology report with the format of "
i = 1
for k in range(2):
    for txt_name in os.listdir(dir_path[k]):
        try:
        
            print(f"[!]Starting the Extraction Process : {i}")
            txt_path = dir_path[k] + txt_name
    
            print(f"[$]Variable names | dir_path = {dir_path[k]} | pdfpath = {txt_path} | pdfname = {txt_name}")
            print("[!]Calling the Gemeni function")


            c = open(txt_path, "r")
            a = c.read() 
            #print(a)
            c.close()



    
            bloody_csv = get_gemini_response(a)
        
            sample_id = get_sample_ID(a)

            if(bloody_csv != "errorcodered"):
    
                filename = (f"{csv_path[k]}{Path(txt_path).stem}-{sample_id}.csv")
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







    

















