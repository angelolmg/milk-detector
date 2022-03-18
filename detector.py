#TODO: ADD FUNCTIONS TO MAKE THINGS MORE SELF DESCRIPTIVE

import cv2, time
from cv2 import CV_32F
import pandas as pd
from tracker import *

class Detector:
    def __init__(self):

        # Get structure with all products available
        products_file = "milk-products.csv"
        self.products = []

        try:
            data = pd.read_csv(products_file)
            for index, row in data.iterrows():
                self.products.append([row["NAME"], float(row["PRICE"].replace(',','.')), 0])
        except:
            print(f"Products file {products_file} not found")

        self.screen_w = 0
        self.screen_h = 0

        self.checking_proportion = 5/8
        checking_w = int(self.checking_proportion * self.screen_w)

        # (id, name)
        self.buffered_objs = []
        self.detected_objs = [] 

        # Basic colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        gray = (80, 80, 80)
        self.green = (0, 255, 0)
        yellow = (0,255,255)
        self.red = (0, 0, 255)
        self.box_color = [self.green, yellow]

        self.same_obj_radius = 40
        print_objects = False
        self.print_info = False

        self.n_products = 0
        self.total_price = 0

        self.class_names = []
        with open("obj.names") as f:
            self.class_names = [cname.strip() for cname in f.readlines()]

        #cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # work with 3 & 5
        self.cap = cv2.VideoCapture("data2/videos/milk_cond7.mp4")
        net = cv2.dnn.readNet("custom-yolov4-tiny-detector_best-v6.weights", "custom-yolov4-tiny-detector.cfg")

        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(size=(416,416), scale=1/255)

        self.tracker = EuclideanDistTracker(self.same_obj_radius, print_objects)

    def getNextFrame(self):

        ret, frame = self.cap.read() 
        if not ret:
            return None

        # Initialize screen proportion variables
        # Initialize checking threshold  
        if self.screen_w == 0: 
            (self.screen_w, self.screen_h, _) = frame.shape
            self.checking_w = int(self.checking_proportion * self.screen_w)
            
        # Detection
        start = time.time()
        classes, scores, boxes = self.model.detect(frame, 0.3, 0.5)
        end = time.time()

        # Update tracker
        # Draw boxes and labels
        boxes_ids = self.tracker.update(boxes)
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
            if cy > self.checking_w:
                if curr_obj in self.buffered_objs:

                    self.buffered_objs.remove(curr_obj)

                    # check if object with same id wasn't detected already
                    duplicate = False
                    for objs in self.detected_objs:
                        if objs[0] == curr_obj[0]: 
                            duplicate = True
                            break
                        
                    if not duplicate: 
                        self.detected_objs.append(curr_obj)
                        self.total_price = round(self.total_price + self.products[curr_obj[1]][1], 2)
                        self.products[curr_obj[1]][2] += 1 
                        self.n_products += 1
                    
            elif curr_obj not in self.buffered_objs:
                self.buffered_objs.append(curr_obj)


            label = f"{self.class_names[class_id]} : {scores[i]}"
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.red, 3)
            cv2.circle(frame, (cx, cy), self.same_obj_radius, self.green, -1)
            cv2.putText(frame, str(id), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.red, 3)
            cv2.rectangle(frame, (x, y), (x + w, y + h), self.box_color[class_id], 3)
        
        if self.print_info:
            print(f"Products detected: {self.n_products}")
            for product in self.products:
                print(f"{product[0]}: {product[2]}")
            print(f"Total price: {self.total_price}")
            print("=========================")

        cv2.line(frame, (0, self.checking_w), (self.screen_h, self.checking_w), self.white, 5)

        # Draw FPS
        fps_label = f"FPS: {round((1.0/(end - start)), 2)}"
        cv2.putText(frame, fps_label, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.black, 4)
        cv2.putText(frame, fps_label, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.green, 2)
        frame = cv2.resize(frame, (870,500)) 
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return frameRGB

    def play(self):

        while True:

            ret, frame = self.cap.read() 
            if not ret:
                break

            #frame = frame[50:50+500, 50:50+500]
            # Initialize screen proportion variables
            # Initialize checking threshold  
            if self.screen_w == 0: 
                (self.screen_w, self.screen_h, _) = frame.shape
                self.checking_w = int(self.checking_proportion * self.screen_w)
                
            # Detection
            start = time.time()
            classes, scores, boxes = self.model.detect(frame, 0.3, 0.5)
            end = time.time()

            # Update tracker
            # Draw boxes and labels
            boxes_ids = self.tracker.update(boxes)
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
                if cy > self.checking_w:
                    if curr_obj in self.buffered_objs:

                        self.buffered_objs.remove(curr_obj)

                        # check if object with same id wasn't detected already
                        duplicate = False
                        for objs in self.detected_objs:
                            if objs[0] == curr_obj[0]: 
                                duplicate = True
                                break
                            
                        if not duplicate: 
                            self.detected_objs.append(curr_obj)
                            self.total_price = round(self.total_price + self.products[curr_obj[1]][1], 2)
                            self.products[curr_obj[1]][2] += 1 
                            self.n_products += 1
                        
                elif curr_obj not in self.buffered_objs:
                    self.buffered_objs.append(curr_obj)


                label = f"{self.class_names[class_id]} : {scores[i]}"
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.red, 3)
                cv2.circle(frame, (cx, cy), self.same_obj_radius, self.green, -1)
                cv2.putText(frame, str(id), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.red, 3)
                cv2.rectangle(frame, (x, y), (x + w, y + h), self.box_color[class_id], 3)
            
            if self.print_info:
                print(f"Products detected: {self.n_products}")
                for product in self.products:
                    print(f"{product[0]}: {product[2]}")
                print(f"Total price: {self.total_price}")
                print("=========================")

            cv2.line(frame, (0, self.checking_w), (self.screen_h, self.checking_w), self.white, 5)

            # Draw FPS
            fps_label = f"FPS: {round((1.0/(end - start)), 2)}"
            cv2.putText(frame, fps_label, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.black, 4)
            cv2.putText(frame, fps_label, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.green, 2)


            # Draw frame
            small_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) 
            cv2.imshow("Cashier-less Checkout", small_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
            

#det = Detector()
#det.getNextFrame()
#det.play()