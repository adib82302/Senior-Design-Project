import onnx

# Load the ONNX model
onnx_model_path = '/Users/adibk/Documents/Senior-Design-Project/Computer_Vision/best.onnx'
onnx_model = onnx.load(onnx_model_path)

# Print input names
print("Input names:")
for input in onnx_model.graph.input:
    print(input.name)
