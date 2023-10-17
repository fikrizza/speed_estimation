
import cv2
import numpy as np
import sys
import collections



class Region:
    def __init__(self, start_line, finish_line, id):
        self.pts = start_line + finish_line
        
        self.start_line = start_line
        self.finish_line = finish_line
        
        self.vertices = np.array([[self.pts[i], self.pts[i+1]] for i in range(0, len(self.pts), 2)])
        self.count = 0
        self.c = (165, 84, 45)
        self.id = id
        
        self.x1 = finish_line[2]
        self.y1 = finish_line[3]
        
        self.x2 = finish_line[0]
        self.y2 = finish_line[1]
        
        self.p1 = (self.x1, self.y1)
        self.p2 = (self.x2, self.y2)
        
        # count
        self.count_vehicle = []
        
        
    
    def draw_on_frame(self, frame):
        cv2.polylines(frame, [self.vertices], isClosed=True, color=self.c, thickness=2)

    def draw_legend(self, frame, vertice_num=1, legend='count'):
        text = None
        try:
            if legend=='id':
                text = str(int(self.id))
            elif legend=='count':
                text = str(self.count)
        except:
            pass
        w, h = cv2.getTextSize(text, 0, fontScale=0.6, thickness=2)[0]
        p1 = (self.vertices[vertice_num][0], self.vertices[vertice_num][1])
        p2 = p1[0] + w, p1[1] - h
        cv2.rectangle(frame, p1, p2, self.c, -1, cv2.LINE_AA)
        cv2.putText(frame, text, p1, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1, cv2.LINE_AA, False)


    def draw_count(self, frame, list_data, current_fps):
        x_coor = 20
        offset = 1
        result_count = collections.Counter(list_data)
        
        # draw 
        cv2.rectangle(frame,(x_coor,16),(x_coor+450,8+45*(len(result_count))),(245, 187, 64),-1)
        for results in result_count:
            text = str(results)+" : "+ str(result_count[results])
            cv2.putText(frame,text,(x_coor+20,39*offset),cv2.FONT_HERSHEY_COMPLEX_SMALL,1.5,(255, 255, 255),2)
            offset += 1        
        cv2.putText(frame,F"Total Vehicle: {result_count['in']-result_count['out']}",(x_coor+20,39*offset),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0, 255, 255),2)
        cv2.putText(frame,F"FPS : {round(current_fps, 2)}",(x_coor+20,39*(offset+1)),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0, 255, 255),2)
		
        
        return frame  

