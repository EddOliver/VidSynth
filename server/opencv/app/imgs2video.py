import cv2
import os
import numpy as np

myDir = sorted(os.listdir("output"),key=lambda f: int(''.join(filter(str.isdigit, f))))

video = cv2.VideoCapture("sample.mp4")
fps = video.get(cv2.CAP_PROP_FPS)

size = (0,0)

img_array = []
for filename in myDir:
    img = cv2.imread(f'framesout/{filename}')
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)

vidwriter = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'avc1'), fps, size)
 
for i in range(len(img_array)):
    vidwriter.write(img_array[i])
vidwriter.release()