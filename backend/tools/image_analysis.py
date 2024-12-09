import os
import sys
import torch
import io #input/output module
from PIL import Image
from langchain_core.tools import tool

@tool
def image_detection(image_url: str) -> str:
    """identify the object in the image"""
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    img = Image.open(io.BytesIO(image_url)).convert("RGB")
    results = model(img)
    for obj in results.pred[0]:
        class_id = int(obj[5])  # Class ID of the detected object
        confidence = float(obj[4])  # Confidence score of the detection
        label = model.names[class_id]  # Get the object label from YOLO model's class names
        print("YOLO has detected a ", label, "with confidence of ", confidence)
        return label
        