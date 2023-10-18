from collections import defaultdict

import cv2
import numpy as np
import tkinter as tk
import time
import math
from torch import cuda

from modules.vehicle import Vehicle
from modules.base.fps import get_fps, calcuate_fps
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')
model.to('cuda' if cuda.is_available() else 'cpu')

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        coordinate = [x, y]
        print(coordinate)

cv2.namedWindow("RGB")
cv2.setMouseCallback('RGB', RGB)

# Open the video file
video_path = "assets/20230822T151946.mkv"
cap = cv2.VideoCapture(video_path)

root = tk.Tk()
screen_width = root.winfo_screenwidth()//2
screen_height = root.winfo_screenheight()//2

x_coor = 20
offset = 1

old_boxes = []
new_boxes = []

area = [(249, 157), (382, 157), (500, 363), (135, 363)]

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # For getting time right now
        start_time = time.time()
        frame =  cv2.resize(frame, (screen_width, screen_height), interpolation = cv2.INTER_AREA)
        # Run YOLOv8 inference on the frame
        results = model.track(frame, persist=True)
        
        # # Visualize the results on the frame
        annotated_frame = frame
        
        # Get the boxes and track IDs
        boxes = results[0].boxes
        # location2 = 0
        speed = 0
        
        # calculate fps
        current_fps = calcuate_fps(time.time(), start_time)
        
        # Get xywh from new box and old box
        for box in boxes:            
            vehicle = Vehicle(box.xyxy[0], box.id, box.cls)
            new_boxes.append(vehicle)
            res = cv2.pointPolygonTest(np.array(area, np.int32), ((vehicle.cx, vehicle.cy)), False)
            if res>=0:
                annotated_frame = results[0].plot()
                for old_box in old_boxes:
                    if old_box.id == box.id:
                            location2 = old_box.xywh.numpy()[0]
                            # location1 = box.xywh.numpy()[0]
                            # speed = estimate_speed(location1, location2) #Get the estimate speed use xywh coordinate
                            # cv2.putText(annotated_frame,F"{speed}km/h",(int(box.xywh[0][0])+60,int(box.xywh[0][1])),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0, 255, 255),2)
        
        # For display the annotated frame
        if True:
            # Display the annotated frame
            cv2.putText(annotated_frame,F"FPS : {round(current_fps, 2)}",(x_coor+20,39*(offset+1)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0, 255, 255),2)
            cv2.polylines(annotated_frame, [np.array(area, np.int32)], True, (255, 255, 0), 3)
            cv2.imshow("RGB", annotated_frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(0) & 0xFF == ord("q"):
            break
        old_boxes = new_boxes
    else:
        # Break the loop if the end of the video is reached
        break



# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
