import cv2
import time 



def write_FPS_onscreen(image,prevTime):
    image = cv2.flip(image, 1)
    curTime = time.time()
    sec = curTime - prevTime
    prevTime = curTime
    fps = 1/(sec)
    str = "FPS : %0.1f" % fps
    cv2.putText(image, str, (0,100), cv2.FONT_HERSHEY_SIMPLEX,3,(255,255,255))
    cv2.imshow('MediaPipe Hands',image)

    return image, prevTime 


