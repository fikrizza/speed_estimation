import numpy as np
import math
import time

class Vehicle:
    def __init__(self, xyxy, id=None, id_class=None):
        self.x1 = int(xyxy[0]) # x 
        self.y1 = int(xyxy[1]) # y
        self.x2 = int(xyxy[2]) # w 
        self.y2 = int(xyxy[3]) # h 
        
        self.cx = int((xyxy[0]+xyxy[2])/2) # central x
        self.cy = int((xyxy[1]+xyxy[3])/2) # central y
        
        self.id = id
        self.id_class = id_class
        self.centroid = (self.cx, self.cy)
        self.draw = True
        self.c = (0,200,0)
        self.init_previous()
        self.speed = None
        self.direction = None
        self.label = None
        self.line = "A"
        self.date_time = None
        
        self.status_finish = None        
        self.status_start = None
        self.status_sending = None
        
        self.time_start = None
        self.x1_start = None  
        self.y1_start = None 
        self.x2_start = None  
        self.y2_start = None  
        self.cx_start = None
        self.cy_start = None
        
    def init_start(self):
        time.time()
        self.status_start = True
        self.time_start = time.time()
        self.x1_start = self.x1  
        self.y1_start = self.y1 
        self.x2_start = self.x2  
        self.y2_start = self.y2 
         
        self.cx_start = int((self.x1_start + self.x2_start)/2) # central x
        self.cy_start = int((self.y1_start + self.y2_start)/2) # central y
    
    def init_previous(self):
        self.x1_p = None
        self.y1_p = None
        self.x2_p = None
        self.y2_p = None
    
    def estimate_speed(self):
        speed = 0
        self.speed = speed
        
    def distance_line(self, start_line, finish_line):
        x1, y1, x2, y2 = start_line
        x3, y3, x4, y4 = finish_line    
    
        numerator = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
        denominator = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
        distance = numerator / denominator
        return distance

    def distance_box(self, start_box, finish_box):
        A = np.square(start_box[0] - finish_box[0])
        B = np.square(start_box[1] - finish_box[1])
        C = np.sqrt(A+B)
        return C

    def estimate_speed(self, box, line, now, current_fps, vid_fps, real_dist):
        time = (current_fps / vid_fps) * (now - box.time)
        if time != 0 :
            dist_line2 = self.distance_line(box.start_line, [line.x1, line.y1, line.x2, line.y2])
            dist_vehicle2 = self.distance_box(box.start_box, [box.x2, box.y2])
            dist = (dist_vehicle2 / dist_line2) * real_dist / 1000
            speed = (dist/time) * 3600

            speed_kms = speed
            print(dist_line2, dist_vehicle2)
            box.speed = round(speed,2)
        else:
            box.speed = 0.00
