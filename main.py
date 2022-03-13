#TODO: ADD FUNCTIONS TO MAKE THINGS MORE SELF DESCRIPTIVE

import cv2, time
import pandas as pd
from tracker import *

# Get structure with all products available
products_file = "milk-products.csv"
products = []

try:
    data = pd.read_csv(products_file)
    for index, row in data.iterrows():
        products.append([row["NAME"], float(row["PRICE"].replace(',','.')), 0])
except:
    print(f"Products file {products_file} not found")

screen_w = 0
screen_h = 0

checking_proportion = 5/8
checking_w = int(checking_proportion * screen_w)

# (id, name)
buffered_objs = []
detected_objs = [] 

# Basic colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (80, 80, 80)
green = (0, 255, 0)
yellow = (0,255,255)
red = (0, 0, 255)
box_color = [green, yellow]

same_obj_radius = 30
print_objects = False
print_info = True

n_products = 0
final_price = 0

class_names = []
with open("obj.names") as f:
    class_names = [cname.strip() for cname in f.readlines()]

#cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# work with 3 & 5
cap = cv2.VideoCapture("data/videos/milk_cond3.mp4")
net = cv2.dnn.readNet("custom-yolov4-tiny-detector_best-v3.weights", "custom-yolov4-tiny-detector.cfg")

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416,416), scale=1/255)

tracker = EuclideanDistTracker(same_obj_radius, print_objects)

while True:

    ret, frame = cap.read() 
    if not ret:
        break
    #frame = frame[50:50+500, 50:50+500]
    # Initialize screen proportion variables
    # Initialize checking threshold  
    if screen_w == 0: 
        (screen_w, screen_h, _) = frame.shape
        checking_w = int(checking_proportion * screen_w)
        
    # Detection
    start = time.time()
    classes, scores, boxes = model.detect(frame, 0.3, 0.6)
    end = time.time()

    # Update tracker
    # Draw boxes and labels
    boxes_ids = tracker.update(boxes)
    for i in range(len(boxes_ids)):
        x, y, w, h, id = boxes_ids[i]
        class_id = classes[i][0]
        curr_obj = (id, class_id)

        cx = int(x + w / 2)
        cy = int(y + h / 2)

        # check if object is below checking threshold
        #
        # if it's above checking threshold then: 
        # put it (objet identifier & class identifier tuple) in the buffer
        # if it's already in the buffer, do nothing
        #
        # if it's below checking threshold then:
        # check if it's buffered 
        # -> if it's not buffered that means its first appearance was below the threshold 
        # -> which is a miss detection, we buffer to handle this kind of behavior
        #
        # then check if it is not in the detected list already
        # if it isn't then add it to the detected objects list
        # if it is already, do nothing
        if cy > checking_w:
            if curr_obj in buffered_objs:

                buffered_objs.remove(curr_obj)

                # check if object with same id wasn't detected already
                duplicate = False
                for objs in detected_objs:
                    if objs[0] == curr_obj[0]: 
                        duplicate = True
                        break
                    
                if not duplicate: 
                    detected_objs.append(curr_obj)
                    final_price = round(final_price + products[curr_obj[1]][1], 2)
                    products[curr_obj[1]][2] += 1 
                    n_products += 1
                
        elif curr_obj not in buffered_objs:
            buffered_objs.append(curr_obj)


        label = f"{class_names[class_id]} : {scores[i]}"
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, red, 3)
        cv2.circle(frame, (cx, cy), same_obj_radius, green, -1)
        cv2.putText(frame, str(id), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.8, red, 3)
        cv2.rectangle(frame, (x, y), (x + w, y + h), box_color[class_id], 3)
    
    if print_info:
        print(f"Products detected: {n_products}")
        for product in products:
            print(f"{product[0]}: {product[2]}")
        print(f"Total price: {final_price}")
        print("=========================")

    cv2.line(frame, (0, checking_w), (screen_h, checking_w), white, 5)

    # Draw FPS
    fps_label = f"FPS: {round((1.0/(end - start)), 2)}"
    cv2.putText(frame, fps_label, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, black, 4)
    cv2.putText(frame, fps_label, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, green, 2)

    # Draw frame
    small_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) 
    cv2.imshow("Cashier-less Checkout", small_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()