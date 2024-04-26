from ultralytics import YOLO
import cv2
import cvzone
import math

# Settings
video_path = '/Users/adibk/Downloads/20240209_132128A.mp4'
cap = cv2.VideoCapture(video_path)
model = YOLO('/Users/adibk/Documents/Senior-Design-Project/Computer_Vision/best.pt')

# Define text color
text_color = (0, 255, 0)  # Green color for confidence interval text

while cap.isOpened():
    video_feed, frame = cap.read()
    
    #Pre-processing
    if not video_feed:
        print("cannot open file to process video ...  exiting")
        break

    #Processing
    still_images = model(frame, stream=True)
    for image in still_images:
        boxes = image.boxes
        for box in boxes:
            # Bounding box
            x1, y1, x2, y2 = box.xyxy[0] 
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(frame, (x1, y1), (x2, y2),(0,0,255), 5)
            
            # Confidence
            conf = math.ceil((box.conf[0]*100))/100
            cv2.putText(frame, f'{conf}', (x1, y1-20), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    #Post-Processing
    cv2.imshow("Video Feed with Detection", frame)
    if cv2.waitKey(1) == ord('f'):
        break

#Shut-down Procedure
cap.release()
cv2.destroyAllWindows()
