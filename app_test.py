from collections import defaultdict

import cv2
import numpy as np
import tkinter as tk
import time
import math 

from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')
model.to("cuda")

# Open the video file
video_path = "assets/20230822T151946.mkv"
cap = cv2.VideoCapture(video_path)

# Store the track history
track_history = defaultdict(lambda: [])

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


def calcuate_fps(time_now, start_time):
    fps = 1.0/(time_now - start_time)
    return fps

def estimatespeed(location1, location2):
    d_pixel = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
    # pixels per meter:
    ppm = 20
    d_meters = d_pixel/ppm
    time_constant = 15*3.6
    
    speed = d_meters*time_constant
    return int(speed)

x_coor = 20
offset = 1

old_boxes = []
counter_test = 1

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # For getting time right now
        start_time = time.time()
        
        # Run YOLOv8 inference on the frame
        results = model.track(frame, persist=True)
        
        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Get the boxes and track IDs
        new_boxes = results[0].boxes
        location2 = 0
        speed = 0
        for loc1 in new_boxes:
            for loc2 in old_boxes:
                if loc2.id == loc1.id:
                    location2 = loc2.xywh.numpy()[0]
                    location1 = loc1.xywh.numpy()[0]
                    speed = estimatespeed(location1, location2)
                    cv2.putText(annotated_frame,F"{speed}km/h",(int(loc1.xywh[0][0])+60,int(loc1.xywh[0][1])),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0, 255, 255),2)
                
            
        
        counter_test += 1
        
        if True:
            # calculate fps
            current_fps = calcuate_fps(time.time(), start_time)
            
            # Display the annotated frame
            frame_show_resize =  cv2.resize(annotated_frame, (screen_width, screen_height), interpolation = cv2.INTER_AREA)
            cv2.putText(frame_show_resize,F"FPS : {round(current_fps, 2)}",(x_coor+20,39*(offset+1)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0, 255, 255),2)
            # cv2.putText(frame_show_resize,F"" )
            cv2.imshow("YOLOv8 Tracking", frame_show_resize)
        
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        old_boxes = new_boxes
    else:
        # Break the loop if the end of the video is reached
        break



# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
