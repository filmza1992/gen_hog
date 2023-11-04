from fastapi import FastAPI, HTTPException, Request
import cv2
import numpy as np
import base64
import imutils
import pytesseract

def imgSplit(img_str):
    data = str.split(str(img_str),",")[1]
    return data
    

def img2vec(img):
    v, buffer = cv2.imencode(".jpg", img)
    img_str = base64.b64encode(buffer)
    data = "image data,"+str.split(str(img_str),"'")[1]
    print(data)
    

    return data
img_json = img2vec(cv2.imread('image\MP11.jpg'))
img_base64 = imgSplit(img_json)


