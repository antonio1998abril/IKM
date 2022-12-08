import numpy as np
import cv2
from os import remove, rename, path
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader
from typing import Union
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import platform
from rapidfuzz import fuzz
import math

if platform.system() == "Windows":     
    image_dir = path.join("../files/")   
elif platform.system() == "Linux":
    image_dir = path.join("./files/")

# Save pages in the same folder
testpdf = path.join(image_dir, "test.pdf")
page0 = path.join(image_dir,"page0.jpg" )
CroppedImage = path.join(image_dir,"CroppedImage.jpg")
Document011 = path.join(image_dir, "Document.011.png")
js = path.join(image_dir, "js.png")
getFinal = path.join(image_dir, "getFinal.png")

#🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧 Footer Graphs 🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧
CroppedImageFooterCircle = path.join(image_dir,"CroppedImageFooterCircle.jpg")
CroppedLevelUpRow1 = path.join(image_dir,"CroppedLevelUpRow1.jpg")
CroppedLevelUpRow2 = path.join(image_dir,"CroppedLevelUpRow2.jpg")
CroppedLevelUpRow1Blackest = path.join(image_dir,"CroppedLevelUpRow1Blackest.jpg")
#pytorch
AreaG = path.join(image_dir,"AreaG.jpg")

#end points initializer
app = FastAPI()

# Round values
def truncate(n, decimals = 0): 
    multiplier = 10 ** decimals 
    return int(n * multiplier) / multiplier #✅

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier
###################################################################################
#Circle get color
def colorArea(area,image,color):
    _, binary = cv2.threshold(area, 225, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # draw all contours
    image = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    
    for i in contours[1:]:
        if truncate(cv2.contourArea(i), -4) > 1:#✅
        #detect area ✅
            #return {"color":color,"value":truncate(cv2.contourArea(i), -4)}#
            return {"color":color,"value":cv2.contourArea(i)}#✅

###################################################################################
    #add tresHold to define image sections
def CircleCV():
    # Read the images
    img = cv2.imread(CroppedImageFooterCircle)
    
    # Resizing the image
    image = cv2.resize(img, (700, 600))
    
    # Convert Image to Image HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    #maskTofindColorsArea = ["green","red","yellow"]
    #green
    # Defining lower and upper bound HSV values
    lowerGreen = np.array([50, 100, 100])
    upperGreen = np.array([70, 255, 255])
    # Defining mask for detecting color
    maskGreen = cv2.inRange(hsv, lowerGreen, upperGreen)

    #Red
    lowerRed= np.array([170, 160, 70])
    upperRed = np.array([180, 250, 250])
    maskRed = cv2.inRange(hsv, lowerRed, upperRed)
    #cv2.imshow("Red", maskRed)

    #yellow
    lowerYellow= np.array([18, 40, 90])
    upperYellow = np.array([27, 255, 255])
    maskYellow = cv2.inRange(hsv, lowerYellow, upperYellow)
    #cv2.imshow("Yellow", maskYellow)

    listArea = []

    listArea.append(colorArea(maskRed,image,"Weak"))#✅
    listArea.append(colorArea(maskYellow,image,"Proficient"))#✅
    

    flag = not np.any(maskGreen)
    if flag:
        listArea.append({"color":"Strong","value":0})
    else:
        listArea.append(colorArea(maskGreen,image,"Strong"))
  
  
   
    #✅
    total = 0
    for i in range(len(listArea)):
        total = total +listArea[i]["value"]
       


    newListArea=[]
    for i in range(len(listArea)):
        

        if(listArea[i]["color"] =="Proficient"):
            result = {"color":"Proficient","value":truncate((listArea[i]["value"] / total) * 100) -1}
            newListArea.append(result)
          
        if(listArea[i]["color"] =="Weak"):
            result = {"color":"Weak","value":round_up((listArea[i]["value"] / total) * 100)}
            newListArea.append(result)
            
    
        if(listArea[i]["color"] =="Strong"):
            result = {"color":"Strong","value":round_up((listArea[i]["value"] / total) * 100)}
            newListArea.append(result)
    
 
    
    flag= 0
    for i in range(len(newListArea)):
        if(newListArea[i]["color"] =="Strong" and newListArea[i]["value"] == 0.0):
            flag = 1
    for i in range(len(newListArea)):
        if(newListArea[i]["color"] =="Proficient" and flag == 1):
            newListArea[i]["value"] = newListArea[i]["value"] +1
    
       
    print(newListArea)
    return newListArea   
    # Make python sleep for unlimited time
   
###################################################################################
def deleteBlur(imageBlur):
    #DELETE BLUR
    img = cv2.imread(imageBlur)
    Z = img.reshape((-1,3))

    # convert to np.float32
    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 8
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))    
    cv2.imwrite(imageBlur,res2)

###################################################################################
def FooterRowLevelUp(image,context):
    label =str("")
    
    img = cv2.imread(image)
    # convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # apply thresholding to convert the grayscale image to a binary image
    ret,thresh = cv2.threshold(gray,50,255,0)

    # find the contours
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if(context == "Work Speed/Accuracy"):
        if len(contours) == 99:
            label="Above Average"
        elif len(contours) == 90:
            label ="Average"
        elif len(contours) == 89:
            label = "Very Slow"
        elif len(contours) == 93:
            label = "Very Fast"
        elif len(contours) == 101:
            label = "Below Average"
    elif(context == "Application Ability"):
        cv2.imwrite(CroppedLevelUpRow1Blackest, thresh)
        if len(contours) == 97:
            label="Significant"
        elif len(contours) == 96:
            label ="Moderate"
        elif len(contours) == 89:
            label = "Negligible"
        elif len(contours) >= 98:
            label = "Extensive"
        elif len(contours) == 90:
            label = "Limited"
    #✅Function Done
    return {"label":label,"context":context}
###################################################################################

def nextword(target, source):
    for i, w in enumerate(source):
        if target == "ID:" or target == "Date:" or target == "Score:" or target == "Coverage:" or target == "subject.Percentile:":
            if w == target:
                return source[i+1]
        elif target == "Subject:":
            if w == target:
                return source[i+1]+source[i+2]+source[i+3]+source[i+4]+source[i+5]+source[i+6]+source[i+7]
        elif target == "for:":
            if w == target:
                return source[i+1]+" "+source[i+2]
        elif target == "Client:":
            if w == target:
                return source[i+1]+" "+source[i+2]+" "+source[i+3]
###################################################################################


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
    #print(page_1_text.split(), sep='\n')

    findInside =stringCleaned.split()
    dataFile = [
        "for:",
        "ID:",
        "Date:",
        "Subject:",
        "Client:",
        "Score:",
        "subject.Percentile:",
        "Coverage:"
    ]
    dataMiner=[]
    for i in range(len(dataFile)):
        dataMiner.append(nextword(dataFile[i],findInside))

    for i in range(len(dataMiner)):
        if i == 3:
            proximity= fuzz.ratio("MDC BASIC JAVA INTERVIEW 2",dataMiner[i])
            if(proximity >= 60):
                dataMiner[3]="MDC BASIC JAVA INTERVIEW 2" 

    for i in range(len(dataMiner)):
        if(i == 0):
            dataMiner[i]={"label":"Assessment Result for","value":dataMiner[i]}
        if(i == 1):
            dataMiner[i]={"label":"ID","value":dataMiner[i]}
        if(i == 2):
            dataMiner[i]={"label":"Date","value":dataMiner[i]}
        if(i == 3):
            dataMiner[i]={"label":"Subject","value":dataMiner[i]}
        if(i == 4):
            dataMiner[i]={"label":"Client","value":dataMiner[i]}
        if(i == 5):
            dataMiner[i]={"label":"Score","value":dataMiner[i]}
        if(i == 6):
            dataMiner[i]={"label":"Percentile","value":dataMiner[i]}
        if(i == 7):
            dataMiner[i]={"label":"Subject Coverage","value":dataMiner[i]}   

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

    # Bar Graph
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
   
    listDataLevelUp = []
    listDataLevelUp.append(FooterRowLevelUp(CroppedLevelUpRow1,"Work Speed/Accuracy"))
    listDataLevelUp.append(FooterRowLevelUp(CroppedLevelUpRow2,"Application Ability"))
    
    #✅Return to Client
    return {"scoreBar": dataSkills, "name": name, "concepts": javaOrder,"subjectCoverage":CircleCV(),"FooterLevel":listDataLevelUp,"dataMiner":dataMiner}

###################################################################################
def sortFn(dict):
    #✅Function Done
    return dict['index']
###################################################################################
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
    #✅Function Done
    return functio7()

###################################################################################
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
    #✅Function Done
    return functio6()
###################################################################################

def function4():
    img = cv2.imread(CroppedImage)
    # Output img with window name as 'image'

    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 50, 255, 0)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (255, 255, 255), 2)

    cv2.imwrite(Document011, img)   

    #DELETE BLUR ✅
    #deleteBlur(CroppedImageFooterCircle)
    deleteBlur(AreaG)
    #✅Function Done
    return function5()
###################################################################################

def function3():
    img = cv2.imread(page0)
    # Cropping an image
    #cropped_image = img[2050:3300, 850:2900]
    cropped_image = img[2050:3300, 1540:2900]
    # Save the cropped image
    cv2.imwrite(CroppedImage, cropped_image)


    # footer Graphs
    cropped_image_footer = img[3580:4400, 2600:3500]    
    cv2.imwrite(CroppedImageFooterCircle,cropped_image_footer)


    #(arriba:abajo,derecha:izquierda)
    #cropped_image_foteer = img[3500:4500, 1500:3000], bar cropped_image_foteerLevelUp1 = img[3500:4400, 1000:2500]
    cropped_image_foteerLevelUp1 = img[3510:3720, 250:2050]
    cv2.imwrite(CroppedLevelUpRow1, cropped_image_foteerLevelUp1)

    cropped_image_foteerLevelUp2 = img[4120:4400, 250:2050]
    cv2.imwrite(CroppedLevelUpRow2, cropped_image_foteerLevelUp2)
    #✅Function Done

    #py AreaG 
    cropped_image_footerArea = img[3500:3600, 2500:3650]    
    cv2.imwrite(AreaG,cropped_image_footerArea)


    return function4()
###################################################################################

def function2():
    if platform.system() == "Windows":     
        pages = convert_from_path(testpdf, 500,poppler_path= "../bin")
        for i in range(len(pages)):
            pages[i].save('../files/page' + str(i) + '.jpg', 'JPEG')
    elif platform.system() == "Linux":
        pages = convert_from_path(testpdf, 500)
        for i in range(len(pages)):
            pages[i].save('./files/page' + str(i) + '.jpg', 'JPEG')
    #✅Function Done
    return function3()

###################################################################################
#END POINTS 👷👷👷👷👷👷
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
        remove(CroppedImageFooterCircle)
        remove(AreaG)
    
    except Exception:
        return {"done": "There was an error when was trying to delete a file"}
    finally:
        return {"done": "Memory restored ready to upload another file"}