from fastapi import FastAPI, HTTPException, Request
import cv2
import numpy as np
import base64
import aiohttp
import requests
app = FastAPI()

def imgSplit(img_str):
    data = str.split(str(img_str),",")[1]
    return data

def detect_to_hog(base64_image):
    image_data = base64.b64decode(base64_image)
    nparr = np.frombuffer(image_data, np.uint8)
    img_gray = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    
    img_new = cv2.resize(img_gray, (128, 128), cv2.INTER_AREA)
    win_size = img_new.shape
    cell_size = (8, 8)
    block_size = (16, 16)
    block_stride = (8, 8)
    num_bins = 9
    
    hog = cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, num_bins)
    hog_descriptor = hog.compute(img_new)
    
    return hog_descriptor.flatten().tolist()

#path_model = "http://localhost:8008/"
path_model = "http://172.17.0.3:80/api/predict"
#path_model = "http://localhost:8008/api/predict"
#path_model = "api/predict"
HEADERS = {"Content-Type": "application/json"}

@app.get("/")
def root():
    return {"message" : "This is my first Container api"}

@app.get("/api/animal")
async def upload_image(request : Request):
    try:
        item = await request.json()
        img_str = item['img']
        base64_image = imgSplit(img_str);
        hog = detect_to_hog(base64_image)
        jsons = {"Hog" : hog}
        response = requests.post(path_model , json=jsons)
        if response.status_code == 200:
            # แปลงข้อมูล JSON ที่ได้จากเซิร์ฟเวอร์
            print("status 200")
            data = response.json()
            return data
        else:
            print("เกิดข้อผิดพลาดในการรับส่งข้อมูล")

        
    except:
        raise HTTPException(status_code=500 , detail = "invalid value")
        
@app.get("/api/animal/vector")
async def upload_image_to_hog(request : Request):
    try:
        item = await request.json()
        img_str = item['img']
        base64_image = imgSplit(img_str);
        hog = detect_to_hog(base64_image)
        return {"Hog":hog}
    except:
        raise HTTPException(status_code=500 , detail = "invalid value")
    
