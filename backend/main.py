

import os
import cv2
import numpy as np
import aspose.words as aw
from os import remove, rename, path
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader
from typing import Union
from fastapi import FastAPI, File, UploadFile
from PIL import Image

app = FastAPI()
function1_success = False


def function1(contents):
    rename(contents, "test.pdf")
    return function2()


def function2():
    pages = convert_from_path(
        "test.pdf", 500, poppler_path=r"C:\Users\antonio\Downloads\Apex Trainining\IKM-Project\backend\bin")
    for i in range(len(pages)):
        pages[i].save('page' + str(i) + '.jpg', 'JPEG')
    return function3()


def function3():
    img = cv2.imread('page0.jpg')

    # Cropping an image

    #cropped_image = img[2050:3300, 850:2900]
    cropped_image = img[2050:3300, 1540:2900]

    # Save the cropped image
    cv2.imwrite("Cropped Image.jpg", cropped_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return function4()


def function4():
    img = cv2.imread('Cropped Image.jpg')
    # Output img with window name as 'image'

    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 50, 255, 0)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #shapes, hierarchy = cv2.findContours(thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (255, 255, 255), 2)

    cv2.imwrite('Document.011.png', img)
    # print(cv2.contourArea(contour))
    # remove("Output011.png")

    return function5()


def function5():

    image = cv2.imread('Document.011.png')

    msk = image.copy()
    msk = cv2.medianBlur(msk, 25)
    msk = cv2.erode(msk, np.ones((7, 7)))
    msk = cv2.threshold(msk, 200, 255, cv2.THRESH_BINARY)[1]
    msk = cv2.GaussianBlur(msk, (5, 0), 25)
    msk = cv2.threshold(msk, 120, 255, cv2.THRESH_BINARY)[1]
    msk = cv2.erode(msk, np.ones((31, 31)))
    image[np.where(msk != 0)] = 255
    #cv2.imshow('Shapes', image)
    cv2.imwrite('js.png', image)
    return functio6()


def functio6():

    image = cv2.imread('js.png')
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

    #cv2.imshow('thresh', thresh)
    #cv2.imshow('image', image)
    cv2.imwrite('getFinal.png', image)
    cv2.waitKey()
    return functio7()


def sortFn(dict):
    return dict['index']


def functio7():
    javaOrder = []
    AgileConcepts = "Agile Concepts"
    DesignPatterns = "Design Patterns"
    GenericsandCollections = "Generics and Collections"

    SpringBootTesting = "Spring Boot T esting"

    CloudFundamentals = "Cloud Fundamentals"

    ObjectOrientationinJava = "Object Orientation in Java"

    Concurrency = "Concurrency"

    JavaStreams = "Java Streams"

    UnderstandingMicroservices = "Understanding Microservices"

    SpringReactiveProgramming = "Reactive Programming"

    SpringBootRestful = "Spring Boot Restful"

    ExceptionHandling = "Exception Handling"

    LambdaExpressions = "Lambda Expressions"

    IOCContainer = "IOC Container"

    ManagingEntitiesinJavaPersistence = "Managing Entities in Java Persistence"

    RESTWebServicesa = "REST W eb Services"

    javaDictionary = []
    # Get text
    name = []
    pdf = PdfFileReader('test.pdf')
    page_1_object = pdf.getPage(0)
    page_1_text = page_1_object.extractText()
    result = page_1_text.split()
    stringCleaned = " ".join(page_1_text.split())

    # for paragraph in page_1_text:
    #    textData.append(paragraph)

    name.append(result[6] + " "+result[7])

    str1 = stringCleaned.find(AgileConcepts)
    javaOrder.append({"index": str1, "value": AgileConcepts})

    str2 = stringCleaned.find(DesignPatterns)
    javaOrder.append({"index": str2, "value": DesignPatterns})

    str3 = stringCleaned.find(GenericsandCollections)
    javaOrder.append({"index": str3, "value": GenericsandCollections})

    str4 = stringCleaned.find(SpringBootTesting)
    javaOrder.append({"index": str4, "value": SpringBootTesting})

    str5 = stringCleaned.find(CloudFundamentals)
    javaOrder.append({"index": str5, "value": CloudFundamentals})

    str6 = stringCleaned.find(ObjectOrientationinJava)
    javaOrder.append({"index": str6, "value": ObjectOrientationinJava})

    str7 = stringCleaned.find(Concurrency)
    javaOrder.append({"index": str7, "value": Concurrency})

    str8 = stringCleaned.find(JavaStreams)
    javaOrder.append({"index": str8, "value": JavaStreams})

    str9 = stringCleaned.find(UnderstandingMicroservices)
    javaOrder.append({"index": str9, "value": UnderstandingMicroservices})

    str10 = stringCleaned.find(SpringReactiveProgramming)
    javaOrder.append({"index": str10, "value": SpringReactiveProgramming})

    str11 = stringCleaned.find(SpringBootRestful)
    javaOrder.append({"index": str11, "value": SpringBootRestful})

    str12 = stringCleaned.find(ExceptionHandling)
    javaOrder.append({"index": str12, "value": ExceptionHandling})

    str13 = stringCleaned.find(LambdaExpressions)
    javaOrder.append({"index": str13, "value": LambdaExpressions})

    str14 = stringCleaned.find(IOCContainer)
    javaOrder.append({"index": str14, "value": IOCContainer})

    str15 = stringCleaned.find(ManagingEntitiesinJavaPersistence)
    javaOrder.append(
        {"index": str15, "value": ManagingEntitiesinJavaPersistence})

    str16 = stringCleaned.find(RESTWebServicesa)
    javaOrder.append({"index": str16, "value": RESTWebServicesa})

    javaOrder.sort(key=sortFn)
    javaOrder.reverse()
    print(javaOrder)

    dataSkills = []

    # endGet text funtion
    image = cv2.imread("getFinal.png")
    deep_copy = image.copy()

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(image_gray, 210, 255, cv2.THRESH_BINARY)
    thresh = 255 - thresh

    shapes, hierarchy = cv2.findContours(
        image=thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image=deep_copy, contours=shapes, contourIdx=-1,
                     color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

    # for iteration, shape in enumerate(shapes):
    # if hierarchy[0, iteration, 3] == -1:
    #print(hierarchy[0, iteration, 3])

    for contour in shapes:
        if cv2.contourArea(contour) > 1000:
            dataSkills.append(cv2.contourArea(contour))
            print(cv2.contourArea(contour))
    # remove("Output011.png")
    #cv2.imshow('Shapes', deep_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return {"scoreBar": dataSkills, "name": name, "concepts": javaOrder}


@app.get("/")
def read_root():
    return {"Hello": "World"}


""" @app.post("/api/submitFile")
async def upload(file:UploadFile = File(...)):
        try:
            listData = []
            contents = file.file.read()
            with open(file.filename, 'wb') as f:
                f.write(contents)
            doc = aw.Document(file.filename)
            doc.save("Output.html")
            remove("Output.001.png")
            remove("Output.002.png")
            remove("Output.003.png")
            remove("Output.004.png")
            remove("Output.005.png")
            remove("Output.006.png")
            remove("Output.007.png")
            remove("Output.008.png")
            remove("Output.009.png")
            remove("Output.010.png")
            remove("Output.012.png")
            remove("Output.013.png")
            remove("Output.014.png")
            remove("Output.015.png")
            remove("OutputPDF.html")
            #here start the application to get areas of each bar
            img = cv2.imread('Output.011.png')
            # Output img with window name as 'image'

            imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(imgray, 50, 255, 0)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(img, contours, -1, (0,255,0), 2)
            cv2.imwrite('Document.011.png', img)
            cv2.imwrite('test_g.png', imgray)

            
            for contour in contours:
                listData.append(cv2.contourArea(contour))
                print(cv2.contourArea(contour))
                #remove("Output011.png")

    
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()

        return {"message":listData} """


@app.post("/api/submitFile")
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


@app.delete("/api/deleteFile")
def delete_File():
    try:
        remove("test.pdf")
        remove("page0.jpg")
        remove("Cropped Image.jpg")
        remove("Document.011.png")
        remove("js.png")
        remove("getFinal.png")
    except Exception:
        return {"done": "There was an error when is trying to delete a file"}
    finally:
        return {"done": "Memory restored ready to upload another file"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#    return {"item_id": item_id, "q": q}
