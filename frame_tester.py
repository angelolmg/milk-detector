# Arbitrary frame tester
import cv2

colors = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

class_names = []
with open("obj.names") as f:
    class_names = [cname.strip() for cname in f.readlines()]

frame = cv2.imread('data/images/cond/cond_0fa04a70-9ffa-11ec-a81a-7085c2c6b3ed.jpg')
#frame = cv2.imread('fix/test1.png')
#frame = frame[20:20+400, 20:20+400]
frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) 
lt = 0.3
ut = 0.6

net = cv2.dnn.readNet("custom-yolov4-tiny-detector_best-v3.weights", "custom-yolov4-tiny-detector.cfg")

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416,416), scale=1/255)

classes, scores, boxes = model.detect(frame, lt, lt)
print(len(scores))
print(scores)
objects = zip(classes, scores, boxes)

for (classid, score, box) in objects:

    color = colors[int(classid) % len(colors)]
    label = f"{class_names[classid[0]]} : {score}"
    cv2.rectangle(frame, box, color, 2)
    cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

cv2.imshow("frame", frame)

cv2.waitKey(0)
cv2.destroyAllWindows()