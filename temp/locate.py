import cv2 as cv
import sys
import numpy as np
import os.path
import pytesseract
import datetime


net = ''

def load_model():
    global net
    modelConfiguration = "Z:\djangotemp\\temp\\model\\darknet-yolov3.cfg";
    modelWeights = "Z:\djangotemp\\temp\\model\\lapi.weights";
    net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)

def getOutputsNames(net):
    layersNames = net.getLayerNames()
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def run_locate(frame):
    # Number Plate Detection
    # using Yolov3
    global net
    print(type(frame))
    inpWidth = 416
    inpHeight = 416
    confThreshold = 0.5
    blob = cv.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)
    net.setInput(blob)
    outs = net.forward(getOutputsNames(net))
    chosen_detections = []
    chosen_detections_length = 0
    max_conf_index = 0
    max_conf = 0
    for out in outs:
        for detection in out:
            if(detection[5] > confThreshold):
                if(detection[5] > max_conf):
                    max_conf = detection[5]
                    max_conf_index = chosen_detections_length
                chosen_detections.append(detection)
                chosen_detections_length += 1
    if not chosen_detections_length:
        return
    box = chosen_detections[max_conf_index]
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    center_x = int(box[0] * frameWidth)
    center_y = int(box[1] * frameHeight)
    width = int(box[2] * frameWidth)
    height = int(box[3] * frameHeight)
    left = int(center_x - width / 2)
    top = int(center_y - height / 2)
    # the framme consisting of the cropped image
    new_frame = frame[top:top+height+1 , left-5:left+width+5]

    # OCR
    # using tesseract

    text = pytesseract.image_to_string(new_frame, lang='eng', config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    folder_path = 'Z:\\djangotemp\\temp\\media\\'
    file = open(folder_path + "data.txt","a")
    #text = text[:11]
    file.write(text + ' --------  ' + str(datetime.datetime.now()) + '\n')
    file.close()
    print(text)
    cv.imwrite(folder_path + text + '.jpg',frame)
    cv.imwrite(folder_path + 'numberplate_' + text + '.jpg',new_frame)
    return
