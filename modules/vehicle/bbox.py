import time
import cv2
import datetime
import numpy as np
import math
import sympy as sym
import requests
class BBox:
    def __init__(self, xyxy, id=None):
        self.x1 = int(xyxy[0]) # x 
        self.y1 = int(xyxy[1]) # y
        self.x2 = int(xyxy[2]) # w 
        self.y2 = int(xyxy[3]) # h 
        
        self.cx = int((xyxy[0]+xyxy[2])/2) # central x
        self.cy = int((xyxy[1]+xyxy[3])/2) # central y
        
        self.id = id
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
        
    def time_now(self):
        now = datetime.datetime.now()
        date_time = now.strftime("%d-%m-%Y %H:%M:%S.%f")[:-4]
        self.date_time = date_time
        return date_time
    
    def path_vehicle(self):
        # print("at path_vhicle")
        return F"temps/staging/{self.label}_{self.speed}_{self.direction}_{self.line}.jpeg" #change for test
        # return F"temps\\staging\\{self.time_now()}_{self.label}_{self.speed}_{self.direction}_{self.line}.jpeg"

    def json_data(self, camera_name, vehicle_path):

        data = {
            "datatime" : self.date_time, 
            "speed" : self.speed, 
            "direction" : self.direction, 
            "camera_name" : camera_name, 
            "type_vehicle" : self.label, 
        }
        
        data_file = {
                    "image_vehicle" : open(vehicle_path, "rb"),
                    }
        
        return data, data_file
    

    def draw_box(self, frame):
        cv2.rectangle(frame, (self.x1, self.y1), (self.x2, self.y2), self.c, 2)
    
    def draw_id_speed(self, frame):
        id_speed = f"{str(int(self.id))} : {self.speed} Km/Jam"
        w, h = cv2.getTextSize(id_speed, 0, fontScale=0.8, thickness=1)[0]
        p1 = (self.x1, self.y1)
        p2 = p1[0] + w, p1[1] - h 
        cv2.rectangle(frame, p1, p2, self.c, -1, cv2.LINE_AA)
        cv2.putText(frame, id_speed, (self.x1, self.y1), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 1, cv2.LINE_AA, False)


    # calculate speed estimation
    def distance_line(self, start_line, finish_line):
        x1, y1, x2, y2 = start_line
        x3, y3, x4, y4 = finish_line    
        
        numerator = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
        denominator = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        distance = numerator / denominator
        return distance
    
    def estimate_speed(self, region, current_fps, vid_fps, real_dist):
        time_now = time.time()
        time_ = (current_fps / vid_fps) * (time_now - self.time_start)
        dist_line = self.distance_line(region.start_line, region.finish_line)
        dist_vehicle = self.distance_box()
        dist =real_dist * (dist_line / dist_vehicle) 
        speed = (dist/time_) * 3.6
        self.speed = round(speed,2)
    
    def estimatespeed(location1, location2):
        d_pixel = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
        # pixels per meter:
        ppm = 8
        d_meters = d_pixel/ppm
        time_constant = 15*3.6
        
        speed = d_meters*time_constant
        return int(speed)

    def distance_box(self):
        A = np.square(self.cx_start - self.cx)
        B = np.square(self.cy_start - self.cy)
        C = np.sqrt(A+B)
        return C

    # check position
    def check_potition(self, line ):
        x = sym.Symbol('x')
        y = sym.Symbol('y')
        
        x1 = line[0]
        y1 = line[1]
        
        x2 = line[2]
        y2 = line[3]
                
        a1 = (y - y1)
        a2 = (y2-y1)
        b1 = (x - x1)
        b2 = (x2- x1)

        temp1 = a1 * b2
        temp2 = a2 * b1

        c1 = 0
        c2 = 0

        try:
            c2, x2 = temp2.args
        except:
            x2 = temp2

        try:
            c1, y1 = temp1.args
        except:
            y1 = temp1

        a = y1 +(-x2)
        b = c2 - c1
        result = a.subs({x:self.cx, y: self.cy})

        if result < b :
            result = "out"
        else:
            result = "in"
        
        self.direction = result 

    def send_data(self, frame, url_api):
        try:
            # save the image result
            vehicle_image = frame[self.y1: self .y2, self .x1:self .x2]
            vehicle_path = self.path_vehicle(picture)
            picture += 1
            cv2.imwrite(vehicle_path, vehicle_image)
            

            data, data_file = self.json_data("camera_test")
                
            
            sendAlert = requests.post(url_api , data= data, files= data_files)
            status = sendAlert.json()['status']            
            print(status)
                
        except Exception as E:
            print(f"====Error==== :{E} ")

