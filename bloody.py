
import csv
from PIL import Image
import base64
from io import BytesIO
import pandas as pd
import fitz
import google.generativeai as genai
import tempfile
import os
from pathlib import Path
import PIL

GEMINI_API = "AIzaSyCtQ914aymvoEhR07yzd9wB0EnkGBCK8JY"


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

def get_gemini_response(pdf_path,questions):
    try :

        blood_report = pdf2img(pdf_path)
        # blood_report_1 = Image.open("images/img4.jpeg")
        # blood_report_2 = Image.open("images/img3.jpeg")
        # blood_report_3 = Image.open("images/img2.jpeg")
        # blood_report_4 = Image.open("images/img1.jpeg")
        format = Image.open("images/format.jpg")
        genai.configure(api_key=GEMINI_API)
        model = genai.GenerativeModel('gemini-pro-vision',safety_settings=safety_settings,generation_config=generation_config)
        response = model.generate_content([f"here you have a blood report , {questions} {format}" ,blood_report])
        return response.text

    except Exception as e:
        return (f"[-]error : {e}")


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
        print(f"[-]Error during image conversion detection: {str(e)}")





pdf_path = "images/PDF1.pdf"
questions= "give the response in .csv ,ignore the name field, any notes and other stuffs in the report, only consider the tests and start from hematology report with the format of "
# going for snack brb

bloody_json= get_gemini_response(pdf_path,questions)
print(bloody_json)

with open('report.csv', 'w') as file:
    csv_writer = csv.writer(file)
    csv_writer.write(bloody_json)

    





