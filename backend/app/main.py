

import os
import numpy as np
import cv2
from os import remove, rename, path
from pdf2image import convert_from_path, convert_from_bytes
from PyPDF2 import PdfFileReader
from typing import Union
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import platform
import os.path

image_dir = os.path.join("./files/")
testpdf =  "test.pdf"
page0 =  "page0.jpg"
CroppedImage =  "CroppedImage.jpg"
Document011 =  "Document.011.png"
js =  "js.png"
getFinal=  "getFinal.png"



testpdf = os.path.join(image_dir, testpdf)
page0 = os.path.join(image_dir,page0 )
CroppedImage = os.path.join(image_dir,CroppedImage)
Document011 = os.path.join(image_dir, Document011)
js = os.path.join(image_dir, js)
getFinal = os.path.join(image_dir, getFinal)




"""     remove("../files/test.pdf")
        remove("../files/page0.jpg")
        remove("../files/CroppedImage.jpg")
        remove("../files/Document.011.png")
        remove("../files/js.png")
        remove("../files/getFinal.png") """



app = FastAPI()

def functio7():
    javaOrder = []
    # Get text
    name = []
    pdf = PdfFileReader(testpdf)
    page_1_object = pdf.getPage(0)
    page_1_text = page_1_object.extractText()
    result = page_1_text.split()
    stringCleaned = " ".join(page_1_text.split())

    name.append(result[6] + " "+result[7])

    keywords = ["Agile Concepts",
                "Design Patterns",
                "Generics and Collections",
                "Spring Boot T esting",
                "Cloud Fundamentals",
                "Object Orientation in Java",
                "Concurrency",
                "Java Streams",
                "Understanding Microservices",
                "Reactive Programming",
                "Spring Boot Restful",
                "Exception Handling",
                "Lambda Expressions",
                "IOC Container",
                "Managing Entities in Java Persistence",
                "REST W eb Services"]

    for i in range(len(keywords)):
        order = stringCleaned.find(keywords[i])
        javaOrder.append({"index": order, "value": keywords[i]})

    javaOrder.sort(key=sortFn)
    javaOrder.reverse()
    dataSkills = []
    # endGet text funtion

    image = cv2.imread(getFinal)
    deep_copy = image.copy()

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(image_gray, 210, 255, cv2.THRESH_BINARY)
    thresh = 255 - thresh

    shapes, hierarchy = cv2.findContours(
        image=thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image=deep_copy, contours=shapes, contourIdx=-1,
                     color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    for contour in shapes:
        if cv2.contourArea(contour) > 1000:
            dataSkills.append(cv2.contourArea(contour))
            # print(cv2.contourArea(contour))
    return {"scoreBar": dataSkills, "name": name, "concepts": javaOrder}


def sortFn(dict):
    return dict['index']

def functio6():

    image = cv2.imread(js)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Remove horizontal
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 1))
    detected_lines = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(
        detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)

    # Remove vertical
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))
    detected_lines = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(
        detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)

    cv2.imwrite(getFinal, image)
    return functio7()


def function5():
    image = cv2.imread(Document011)
    msk = image.copy()
    msk = cv2.medianBlur(msk, 25)
    msk = cv2.erode(msk, np.ones((7, 7)))
    msk = cv2.threshold(msk, 200, 255, cv2.THRESH_BINARY)[1]
    msk = cv2.GaussianBlur(msk, (5, 0), 25)
    msk = cv2.threshold(msk, 120, 255, cv2.THRESH_BINARY)[1]
    msk = cv2.erode(msk, np.ones((31, 31)))
    image[np.where(msk != 0)] = 255
    cv2.imwrite(js, image)
    return functio6()


def function4():
    img = cv2.imread(CroppedImage)
    # Output img with window name as 'image'

    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 50, 255, 0)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (255, 255, 255), 2)

    cv2.imwrite(Document011, img)
    return function5()


def function3():
    img = cv2.imread(page0)
    # Cropping an image

    #cropped_image = img[2050:3300, 850:2900]
    cropped_image = img[2050:3300, 1540:2900]

    # Save the cropped image
    cv2.imwrite(CroppedImage, cropped_image)
    return function4()


def function2():
    if platform.system() == "Windows":     
        pages = convert_from_path(testpdf, 500,poppler_path= "../bin")
        for i in range(len(pages)):
            pages[i].save('../files/page' + str(i) + '.jpg', 'JPEG')
    elif platform.system() == "Linux":
        pages = convert_from_path(testpdf, 500)
        for i in range(len(pages)):
            pages[i].save('./files/page' + str(i) + '.jpg', 'JPEG')

    """  pages = convert_from_path(testpdf, 500, poppler_path="../bin")
    for i in range(len(pages)):
        pages[i].save('../files/page' + str(i) + '.jpg', 'JPEG') """
    return function3()


def function1(contents):
    rename(contents, testpdf)
    return function2()
#END-POINTS

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/submitFile")
async def upload(file: UploadFile = File(...)):
    try:
        listData = []
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
        return function1(file.filename)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()


@app.delete("/deleteFile")
def delete_File():
    try:
        remove(testpdf)
        remove(page0)
        remove(CroppedImage)
        remove(Document011)
        remove(js)
        remove(getFinal)
    except Exception:
        return {"done": "There was an error when is trying to delete a file"}
    finally:
        return {"done": "Memory restored ready to upload another file"}