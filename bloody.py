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
model = genai.GenerativeModel('gemini-pro-vision',safety_settings=safety_settings,generation_config=generation_config)





def get_gemini_response(pdf_path,questions):
    try :

        blood_report = pdf2img(pdf_path)
   
        format = Image.open("images/format.jpg")
        response = model.generate_content([f"here you have a blood report , {questions} {format}" ,blood_report])
        return response.text

    except Exception as e:
        logs_errors(f"\n[-]get_gemini_response | {e} ")
        print(f"[-]Error at get_gemini_ressponse : {e} ")
        return ("errorcodered")


def pdf2img(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)
        image_list = []

        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            image_list.append(page.get_pixmap())

        pdf_document.close()

        images = [
            Image.frombytes("RGB", (image.width, image.height), image.samples)
            for image in image_list
        ]

        # Combine all images vertically
        combined_image = Image.new(
            "RGB", (images[0].width, sum(image.height for image in images))
        )
        offset = 0

        for image in images:
            combined_image.paste(image, (0, offset))
            offset += image.height

        # Save the combined image
        combined_image.save("combinedimage_temp.jpeg", "JPEG")
        return combined_image

    except Exception as e:
        logs_errors(f"\n[-]pdf2img | {e} ")

        print(f"[-]Error during image conversion detection: {str(e)}")



def dataframe_management():
    bloody_df = pd.read_csv("bloody_csv.csv")
    print (bloody_df)

    bloody_df = bloody_df.reindex(columns=['Test', 'd', 'c', 'a'])

#def get_hospitalname():
 
  #      report = Image.open("combinedimage_temp.jpeg")
    
   #     response = model.generate_content([f"just Extract the hospitel name and northing else  ",report])
    
    #    return response.text

    
def get_sampleid():
    
    try: 
        report = Image.open("combinedimage_temp.jpeg")

        response = model.generate_content(["just extract sample id and northing else",report])

        return response.text

    except Exception as e:
        logs_errors(f"\n[-]get_sampleid | {e} ")
        return "errorcodered"


def logs_errors(e):
    print(f"[*]Loging error : {e}")
    
    with open(error_log_path, 'a') as f:
        f.write(f"|{now} | {e} |dir_path =  {dir_path} | pdf_path = {pdf_path} | pdf_name = {pdf_name}")
        f.close()
    


#***********************************************8Driver*********************************************
error_log_path = f"errorlogLeptospirosis[{now}].txt" 
with open(error_log_path, 'a') as f:
        f.write(f"{now}")
        f.close()


dir_path = "images/Datasets/Leptospirosis/Leptospirosis/"
pdf_path = ""
pdf_name = ""
query= "give the response in .csv ,ignore the name field, any notes and other stuffs in the report, only consider the tests from hematology report with the format of "
i = 1
for pdf_name in os.listdir(dir_path):
    try:
        
        print(f"[!]Starting the Extraction Process : {i}")
        pdf_path = dir_path + pdf_name
    
        print(f"[$]Variable names | dir_path = {dir_path} | pdfpath = {pdf_path} | pdfname = {pdf_name}")
        print("[!]Calling the Gemeni function")
    
        bloody_csv = (get_gemini_response(pdf_path,query)).replace(" HEMATOLOGY REPORT,","")
        bloody_csv = bloody_csv.replace("'''csv","")
        bloody_csv = bloody_csv.replace("'''","")
   
        print(bloody_csv)
        print("[!]Getting the File name variables")
    
        pdf_name = pdf_name.replace(".pdf","")
        sample_id = get_sampleid()
        sample_id = sample_id.replace("/","")
        if(sample_id != "errorcodered" or bloody_csv != "errorcodered"):
    
            filename = (f"csv/Leptospirosis/primary/{pdf_name}--{sample_id}_hemo.csv")
            
            filename = filename.replace(" ","")
    
            filename = filename.replace("0","")
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

#dataframe_management()






    

















