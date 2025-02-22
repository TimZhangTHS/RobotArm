from torch import sort
from ultralytics import YOLO
import cv2
import cvzone
import math
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)


def find_angle_to_object(x1,y1,x2,y2):
    # Replace this with your actual calculation based on object coordinates
    # For example, you might calculate the angle based on the center of the object
    # and the center of the frame.
    frame_center = (640, 360)
    object_center = ((x1 + x2) // 2), ((y1 + y2 )// 2)
                     
    
    # Calculate the angle
    angle = np.degrees(np.arctan2(object_center[1] - frame_center[1], 
                                  object_center[0] - frame_center[0]))
    
    return angle
model = YOLO("best (3).pt")
model.export(format='onnx')



classNames = ['Clothe', 'LaundryBasket']

#tracking

while True:
    success, img = cap.read()
    results = model(img, stream = True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2  = int(x1), int(y1), int(x2), int(y2)
            print(x1, y1, x2, y2)
            print(find_angle_to_object(x1,y1,x2,y2))
            #cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),3)

            conf = math.ceil((box.conf[0]*100))/100
            cls = int(box.cls[0])

            if classNames[cls] == "LaundryBasket"  and conf>.5:
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),3)
                cvzone.putTextRect(img, f'{classNames[cls]} {conf}',(max(0,x1),max(35,y1)), scale = 1, thickness=2)#defult is 3 for both
                print("Basket: ", find_angle_to_object(x1,y1,x2,y2))
                c_x = x1 + int((x2-x1)/2)
                c_y = y1 + int((y2-y1)/2)
                cv2.circle(img, (c_x,c_y), radius=10, color=(0, 255, 0), thickness=10)
            if classNames[cls] == "Clothe" and conf > .5:
                cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),3)
                cvzone.putTextRect(img, f'{classNames[cls]} {conf}',(max(0,x1),max(35,y1)), scale = 1, thickness=2)#defult is 3 for both
                print("Clothe: ", find_angle_to_object(x1,y1,x2,y2))  
                c_x = x1 + int((x2-x1)/2)
                c_y = y1 + int((y2-y1)/2)
                cv2.circle(img, (c_x,c_y), radius=10, color=(0, 255, 0), thickness=10)

    cv2.imshow("Image", img)
    cv2.waitKey(1)



