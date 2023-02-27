import cv2
import torch
from PIL import Image
import numpy

# Model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

model = torch.hub.load('ultralytics/yolov5', 'custom', path='datasets/best.pt')

# Images

im1 = Image.open('yolov5/data/images/test_img1.png')  # PIL image
im2 = Image.open('yolov5/data/images/test_img2.png')  # PIL image # PIL image
im0 = Image.open('yolov5/data/images/test_img0.png')

# Inference
results = model([im0, im1, im2], size=640)  # batch of images

# Results
results.print()
results.show()  # or .show()

w = results.xyxy[0].cpu().numpy().tolist()
# print(results.pandas().xyxy[0].name)
print(w)
print(len(w))
