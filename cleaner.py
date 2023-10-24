#!/usr/bin/env python

import cv2
import numpy as np
from PIL import Image
from PyQt5.QtGui import QImage

def PIL_to_qimage(pil_img):
    temp = pil_img.convert('RGBA')
    data = np.array(temp) 
    red, green, blue, alpha = data.T 
    data = np.array([blue, green, red, alpha])
    data = data.transpose()
    temp = Image.fromarray(data)
    
    return QImage(
        temp.tobytes('raw', "BGRA"),
        temp.size[0],
        temp.size[1],
        QImage.Format.Format_RGBA8888
    )

def PIL_to_NumpyArray(pil_img):
    temp = pil_img.convert('RGBA')
    data = np.array(temp) 
    red, green, blue, alpha = data.T 
    data = np.array([blue, green, red, alpha])
    data = data.transpose()
    temp = Image.fromarray(data)
    img = np.array(temp)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img

def processImage(imagePath, valid=True, feather=0, img=None):
    if img is None:
        if not valid:
            pil_img = Image.open(imagePath)
            img = PIL_to_NumpyArray(pil_img)
        else:
            img = cv2.imread(filename=imagePath)
            
    height, width = img.shape[0], img.shape[1]
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    edges = cv2.inRange(hsv, (75, 0, 0), (120, 255,255))

    mask = np.zeros((height, width, 1), np.uint8)

    print (height, width)
    
    if height > width:
        minLen = width
        maxLen = height
    else:
        minLen = height
        maxLen = width
        
    print (minLen)

    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/500, threshold=10, minLineLength=minLen-10, maxLineGap=50)

    lineWidthH = 20
    lineWidthV = 20
    
    v = []
    h = []
    if lines is not None:
        for line in lines:
            if (line[0][0] == line[0][2]):
                v.append(line[0][0])
            if (line[0][1] == line[0][3]):
                h.append(line[0][1])
        if len(h) > 1:
            lineWidthH = max(h)-min(h) + feather
        else:
            lineWidthH = 0
        if len(v) > 1:
            lineWidthV = max(v)-min(v) + feather
        else:
            lineWidthV = 0

        for line in lines:
            if (line[0][0] == line[0][2]):
                cv2.line(mask, (line[0][0], maxLen), (line[0][2], 0), 255, lineWidthV, cv2.FILLED)
            if (line[0][1] == line[0][3]):
                cv2.line(mask, (maxLen, line[0][1]), (0, line[0][3]), 255, lineWidthH, cv2.FILLED)
    else:
        return img
                
    #mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    #return mask

    print (h)
    print (v)

    print (lineWidthH, lineWidthV)
    
    try:
        output = cv2.inpaint(img, mask, max(lineWidthV, lineWidthH), flags=cv2.INPAINT_TELEA)
    except:
        output = None

    return img, output

