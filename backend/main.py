from typing import Union
from fastapi import FastAPI, File, UploadFile
import aspose.words as aw
from os import remove
import cv2

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/submitFile")
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
            remove("Output.html")
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

        return {"message":listData}

@app.delete("/api/deleteFile")
def delete_File():
        try:
            remove("Output.011.png")
            remove("Document.011.png")
            remove("test_g.png")
        except Exception:
            return {"done": "There was an error when is trying to delete a file"}
        finally:
            return {"done": "Memory restored ready to upload another file"}

#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: Union[str, None] = None):
#    return {"item_id": item_id, "q": q}