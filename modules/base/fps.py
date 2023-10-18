import cv2
def get_fps(source):
    try:
        cap = cv2.VideoCapture(int(source))
    except:
        cap = cv2.VideoCapture(source)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    cap.release()
    return fps

def calcuate_fps(time_now, start_time):
    fps = 1.0/(time_now - start_time)
    return fps