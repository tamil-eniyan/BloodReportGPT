
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



dir_path = "images/Datasets/Leptospirosis/Leptospirosis/"
pdf_path = ""
pdf_name = ""
i = 0
query= "give the response in .csv ,ignore the name field, any notes and other stuffs in the report, only consider the tests from hematology report with the format of "
filname = int(input("Enter the file no : "))
no_f = 0
for pdf_name in os.listdir(dir_path):
    no_f = no_f+1



i=0
for pdf_name in os.listdir(dir_path):
    try:
        print(pdf_name + "  | no :   " +str(i))
        i = i+1
        if(i == filname):
            print(f"Complited : {round(100 - (((no_f-i)/no_f)*100),2)}%")
            break



    except Exception as e:
        logs_errors(f"\n[-]main | {e} ")
        pass

#dataframe_management()






    


















