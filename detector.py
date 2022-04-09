#TODO: ADD FUNCTIONS TO MAKE THINGS MORE SELF DESCRIPTIVE

import cv2, time
import pandas as pd
from tracker import *
from tkinter.messagebox import showinfo, showerror, showwarning

class Detector:
    def __init__(self, video_path, settings=None):
        
        if video_path == "":
            showerror(title='Detector initialization', message="Detector tried to initialize with no video available.")
            return None

        if settings is None:
            showerror(title='Detector initialization', message="Detector tried to initialize with no arguments.")
            return None

        '''
        self.cfg_path = 'defaults/default.cfg'
        self.weights_path = 'defaults/default.weights'
        self.names_path = 'defaults/default.names'
        self.products_path = 'defaults/default.csv'
        self.confidence_threshold = 0.3
        self.nms_threshold=0.5
        self.checking_proportion=0.6
        self.same_object_radius=40
        self.debug_detected_objects=0
        self.display_name_score=1
        self.display_bounding_boxes=1
        self.display_tracking_info=1
        self.display_fps=1
        '''
        self.video_over = False
        self.apply_settings(settings)

        # Get structure with all products available
        #products_file = "defaults/default.csv"
        self.products = []

        try:
            data = pd.read_csv(self.products_path)
            for index, row in data.iterrows():
                self.products.append([row["NAME"], float(row["PRICE"].replace(',','.')), 0])
        except:
            showerror(title='Products data loading error', message="Error loading products data (.csv). Could not find in " + str(self.products_path))
            return None
            #print(f"Products file {self.products_path} not found")

        self.screen_w = 0
        self.screen_h = 0

        #self.checking_proportion = 5/8
        self.checking_w = int(self.checking_proportion * self.screen_w)

        # (id, name)
        self.buffered_objs = []
        self.detected_objs = [] 

        # Basic colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (80, 80, 80)
        self.green = (0, 255, 0)
        self.yellow = (0,255,255)
        self.red = (0, 0, 255)
        self.box_color = [self.green, self.yellow]

        #self.same_object_radius = 40
        #self.print_objects = False
        #self.print_info = True

        self.n_products = 0
        self.total_price = 0

        self.class_names = []
        with open(self.names_path) as f:
            self.class_names = [cname.strip() for cname in f.readlines()]

        #cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # work with 3 & 5

        try:
            self.cap = cv2.VideoCapture(video_path)
        except:
            if video_path == "":
                showerror(title='Video Error', message="Bad video path. No video path provided, please load a video first.")
            else:
                showerror(title='Video Error', message="Bad video path. Could not find in " + str(video_path))
            return None

        #net = cv2.dnn.readNet("old/custom-yolov4-tiny-detector_best-v6.weights", "old/main-custom-yolov4-tiny-detector.cfg")
        net = cv2.dnn.readNet(self.weights_path, self.cfg_path)
        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(size=(416,416), scale=1/255)

        self.tracker = EuclideanDistTracker(self.same_object_radius, False)

    def getNextFrame(self):

        ret, frame = self.cap.read() 
        if not ret:
            self.video_over = True
            return None

        # Initialize screen proportion variables
        # Initialize checking threshold  
        if self.screen_w == 0: 
            (self.screen_w, self.screen_h, _) = frame.shape
            self.checking_w = int(self.checking_proportion * self.screen_w)
            
        # Detection
        start = time.time()
        classes, scores, boxes = self.model.detect(frame, self.confidence_threshold, self.nms_threshold)
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

            if self.display_name_score:
                label = f"{self.class_names[class_id]} : {scores[i]}"
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.red, 3)
            
            if self.display_tracking_info:
                cv2.circle(frame, (cx, cy), self.same_object_radius, self.green, -1)
                cv2.putText(frame, str(id), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.red, 3)
            
            if self.display_bounding_boxes:
                cv2.rectangle(frame, (x, y), (x + w, y + h), self.box_color[class_id], 3)
        
        if self.debug_detected_objects:
            print(f"Products detected: {self.n_products}")
            for product in self.products:
                print(f"{product[0]}: {product[2]}")
            print(f"Total price: {self.total_price}")
            print("=========================")

        cv2.line(frame, (0, self.checking_w), (self.screen_h, self.checking_w), self.white, 5)

        # Draw FPS
        if (self.display_fps):
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
            classes, scores, boxes = self.model.detect(frame, self.confidence_threshold, self.nms_threshold)
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

                if (self.display_name_score):
                    label = f"{self.class_names[class_id]} : {scores[i]}"
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.red, 3)
                
                if (self.display_tracking_info):
                    cv2.circle(frame, (cx, cy), self.same_object_radius, self.green, -1)
                    cv2.putText(frame, str(id), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.red, 3)
                
                if (self.display_bounding_boxes):
                    cv2.rectangle(frame, (x, y), (x + w, y + h), self.box_color[class_id], 3)
            
            if self.debug_detected_objects:
                print(f"Products detected: {self.n_products}")
                for product in self.products:
                    print(f"{product[0]}: {product[2]}")
                print(f"Total price: {self.total_price}")
                print("=========================")

            cv2.line(frame, (0, self.checking_w), (self.screen_h, self.checking_w), self.white, 5)

            # Draw FPS
            if (self.display_fps):
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

    def apply_settings(self, settings):

        print("detector.py - Applying settings: " + str(settings))

        self.cfg_path = settings[0]
        self.weights_path = settings[1]
        self.names_path = settings[2]
        self.products_path = settings[3]
        self.confidence_threshold = settings[4]
        self.nms_threshold = settings[5]
        self.checking_proportion = settings[6]
        self.same_object_radius = settings[7]
        self.debug_detected_objects = settings[8]
        self.display_name_score = settings[9]
        self.display_bounding_boxes = settings[10]
        self.display_tracking_info = settings[11]
        self.display_fps = settings[12]


    def get_products(self):
        return self.products


#det = Detector()
#det.getNextFrame()
#det.play()