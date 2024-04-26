from ultralytics import YOLO



model = YOLO('/Users/adibk/Documents/Senior-Design-Project/Computer_Vision/best.pt')
model.export(format='onnx')