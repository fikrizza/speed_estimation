import numpy as np
from scipy.spatial import distance as dist

new_id = 1
disappeared_threshold = 10
# semakin besar 
dist_threshold = 450 
id_tracker = {}
MAX_VAL = 999999

class CentroidTracker:
    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.n_appeared = 1
        self.n_disappeared = 0
    def disappeared(self):
        self.n_disappeared += 1
        self.n_appeared = max(0, min(self.n_appeared-3, 60))
    def appeared(self, position):
        self.position = position
        self.n_appeared += 1
        self.n_disappeared = 0

def track_bboxes(new, old):
    global new_id
    # global id_tracker
    n_old = len(old)
    n_new = len(new)
    if n_old == 0:
        # all new id # ini bikin yang baru
        for box in new:
            box.id = new_id
            id_tracker[new_id] = CentroidTracker(new_id, box.centroid)
            
            new_id += 1
    if n_new == 0:
        # all disappeared # jika yang lama nggk ada 
        for box in old:
            process_disappeared(box, new)


    if n_old*n_new > 0:
        # Set up arrays to help matching ids
        D = dist_centroid_L1(old, new)
        unmatched_old = [True for _ in range(n_old)]
        unmatched_new = [True for _ in range(n_new)]
        for _ in range(min(n_old,n_new)):
            d_min = D.min() # ini apa daah mas 
            if(d_min > dist_threshold):
                break
            D_min_id = np.where(D == D.min())
            row, col = D_min_id[0][0], D_min_id[1][0]
            matched_id = old[row].id
            new[col].id = matched_id
            copy_properties(old, row, new, col)       
            save_previous(old, row, new, col)
            id_tracker[matched_id].appeared(new[col].centroid)
            for i in range(n_old):
                D[i][col] = MAX_VAL
            for j in range(n_new):
                D[row][j] = MAX_VAL
            unmatched_old[row] = False
            unmatched_new[col] = False
            
        # Assign new ids to new boxes
        for i in range(n_new):
            if unmatched_new[i]:
                new[i].id = new_id
                id_tracker[new_id] = CentroidTracker(new_id, new[i].centroid)
                new_id += 1
                
        # Process disappeared boxes
        for i in range(n_old):
            if unmatched_old[i]:
                process_disappeared(old[i], new)
                
    # Reset new_id back to 1
    if new_id > MAX_VAL:
        new_id = 1
    
        
    return id_tracker


def process_disappeared(box, new):
    id_tracker[box.id].disappeared()
    if id_tracker[box.id].n_disappeared < disappeared_threshold:
        box.draw = False # don't draw disappeared box
        new.append(box)
    else:
        id_tracker.pop(box.id)

def dist_centroid_L1(old, new):
    c_old = [i.centroid for i in old]
    c_new = [i.centroid for i in new]
    return dist.cdist(np.array(c_old), np.array(c_new), 'cityblock')

def dist_centroid_L2(old, new):
    c_old = [i.centroid for i in old]
    c_new = [i.centroid for i in new]
    return dist.cdist(np.array(c_old), np.array(c_new), 'euclidean')

def copy_properties(old, row, new, col):

    new[col].speed = old[row].speed
    new[col].direction = old[row].direction
    new[col].status_start = old[row].status_start
    new[col].time_start = old[row].time_start
    new[col].x1_start = old[row].x1_start
    new[col].y1_start = old[row].y1_start
    new[col].x2_start = old[row].x2_start
    new[col].y2_start = old[row].y2_start
    new[col].status_finish = old[row].status_finish
    
    new[col].cy_start = old[row].cy_start
    new[col].cx_start = old[row].cx_start
    
    
    

        
def save_previous(old, row, new, col):
    new[col].x1_p = old[row].x1
    new[col].y1_p = old[row].y1
    new[col].x2_p = old[row].x2
    new[col].y2_p = old[row].y2