from PIL import Image, ImageDraw
import onnxruntime
import numpy as np
import cv2

# Load the ONNX model
onnx_model_path = '/Users/adibk/Documents/Senior-Design-Project/Computer_Vision/best.onnx'
ort_session = onnxruntime.InferenceSession(onnx_model_path)

# Initialize video capture
cap = cv2.VideoCapture('/Users/adibk/Downloads/20240209_130940A.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame (e.g., resize, normalize)
    resized_frame = cv2.resize(frame, (800, 800))  # Resize to match the expected input dimensions of the model
    preprocessed_frame = resized_frame.astype(np.float32) / 255.0  # Normalize pixel values
    preprocessed_frame = np.transpose(preprocessed_frame, (2, 0, 1))  # Change to NCHW format

    # Add batch dimension
    input_tensor = np.expand_dims(preprocessed_frame, axis=0)

    # Perform inference
    ort_inputs = {'images': input_tensor}
    ort_outs = ort_session.run(None, ort_inputs)

    # Process the outputs (e.g., draw bounding boxes)
    for r in ort_outs:
        for box in r:
            # Bounding box
            x1, y1, x2, y2 = box[:4].astype(int)  # Extract bounding box coordinates and convert them to integers
            conf = box[4]  # Extract confidence score
            
            # Convert frame to PIL Image
            pil_img = Image.fromarray(frame)
            draw = ImageDraw.Draw(pil_img)
            
            # Draw bounding box
            draw.rectangle([(x1, y1), (x2, y2)], outline=(0, 255, 0), width=3)
            
            # Display confidence score
            draw.text((x1, y1 - 20), f'{conf:.2f}', fill=(255, 255, 255))
            
            # Convert back to OpenCV format
            frame = np.array(pil_img)

    # Display the processed frame
    cv2.imshow('Processed Frame', frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
