from cv2 import VideoCapture, imwrite 
 
capture = VideoCapture('input/input.mp4')
 
frameNr = 0
 
while (True):
 
    success, frame = capture.read()
 
    if success:
        imwrite(f'framesin/frame_{frameNr}.jpg', frame)
        print(f'framesin/frame_{frameNr}.jpg')
    else:
        break
 
    frameNr = frameNr+1
 
capture.release()