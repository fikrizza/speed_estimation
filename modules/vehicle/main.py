
import math
import sympy as sym
import numpy as np

def distance_line(start_line, finish_line):
    x1, y1, x2, y2 = start_line
    x3, y3, x4, y4 = finish_line    
    
    numerator = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
    denominator = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    distance = numerator / denominator
    return distance

def distance_box(start_box, finish_box):
    A = np.square(start_box[0] - finish_box[0])
    B = np.square(start_box[1] - finish_box[1])
    C = np.sqrt(A+B)
    return C

def estimate_speed(box, line, now, current_fps, vid_fps, real_dist):
    time = (current_fps / vid_fps) * (now - box.time)
    if time != 0 :
        dist_line2 = distance_line(box.start_line, [line.x1, line.y1, line.x2, line.y2])
        dist_vehicle2 = distance_box(box.start_box, [box.x2, box.y2])
        dist = (dist_vehicle2 / dist_line2) * real_dist / 1000
        speed = (dist/time) * 3600

        speed_kms = speed
        print(dist_line2, dist_vehicle2)
        box.speed = round(speed,2)
    else:
        box.speed = 0.00


def check_potition( line, titik, box ):
    x = sym.Symbol('x')
    y = sym.Symbol('y')

    a1 = (y - line[0][1])
    a2 = (line[1][1]-line[0][1])
    b1 = (x - line[0][0])
    b2 = (line[1][0]-line[0][0])

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
    result = a.subs({x:titik[0], y: titik[1]})

    if result < b :
        result = "out"
    else:
        result = "in"
    
    box.direction = result 
    # return result


def intersect_more_than(box, line):
    
     if line.y2 == line.y1: 
        # for straight line in coordinat y
        return box.y2 >= line.y2 and (box.x2 <= line.x2 and box.x2 >= line.x1)
     else:
        # 
        return box.x2 >= line.x2 and (box.y2 <= line.y2 and box.y2 >= line.y1)

def intersect( A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def center_point_front(x1, x2,  y2):
    point = (int(x1 + (x2-x1)/2), int(y2))
    return point
