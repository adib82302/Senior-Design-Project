import cv2
import onnxruntime
import numpy as np

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
    print("Array shape:", ort_outs[0].shape)
    print("Array contents:")
    print(ort_outs[0])
    
    # Process the outputs and draw bounding boxes
    for output in ort_outs:
        for detection in output:
            # Reshape the detection array to (5, 2625)
            detection = detection.reshape(5, -1)

            # Process each detection
            for i in range(detection.shape[1]):
                # Extract values from the detection array
                x_min, y_min, x_max, y_max, confidence = detection[:, i]

                # Convert coordinates from normalized format to pixel coordinates
                x_min = int(x_min * resized_frame.shape[1])
                y_min = int(y_min * resized_frame.shape[0])
                x_max = int(x_max * resized_frame.shape[1])
                y_max = int(y_max * resized_frame.shape[0])

                # Print detection coordinates and confidence score for debugging
                #print("Detection: xmin={}, ymin={}, xmax={}, ymax={}, confidence={}".format(x_min, y_min, x_max, y_max, confidence))

                # Draw bounding box
                color = (0, 255, 0)  # Green color for the bounding box
                thickness = 2  # Thickness of the bounding box
                cv2.rectangle(resized_frame, (x_min, y_min), (x_max, y_max), color, thickness)

                # Display confidence score
                label = f"Confidence: {confidence:.2f}"
                cv2.putText(resized_frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)

    # Display the processed frame with bounding boxes
    cv2.imshow('Processed Frame', resized_frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
