import cv2
import torch

# Load the model
model = torch.hub.load('ultralytics/yolov8', 'custom', path_or_model='/Users/adibk/Documents/Senior-Design-Project/Computer_Vision/best.pt')  # Update path

# Initialize video capture
cap = cv2.VideoCapture('/Users/adibk/Downloads/20240209_130940A.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for YOLO input
    resized_frame = cv2.resize(frame, (640, 640))  # Adjust size according to model requirement
    
    # Convert frame to RGB (YOLO model expects RGB)
    frame_rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    
    # Convert to torch tensor and add batch dimension
    frame_tensor = torch.from_numpy(frame_rgb).permute(2, 0, 1).float().div(255.0).unsqueeze(0)
    
    # Perform inference
    results = model(frame_tensor)
    
    # Draw results on frame
    for result in results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = map(int, result[:6])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, f'{model.names[int(cls)]}: {conf:.2f}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    
    # Display the processed frame
    cv2.imshow('Processed Frame', frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
