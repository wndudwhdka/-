import cv2
import mediapipe as mp
import numpy as np 

def draw_by_location(image, xlocations, ylocations): # 이미지 핸들러에 적혀 있는 구역을 바탕으로 선을 그림
  dimensions = image.shape
 
  image1 = np.zeros([dimensions[0],dimensions[1],3],dtype =np.uint8)
 
  for i in range(int((len(xlocations)))-1):

    cv2.line(image1,(int(xlocations[i]),int(ylocations[i])),(int(xlocations[i+1]),int(ylocations[i+1])),(255,255,255),3)

  
  image = cv2.addWeighted(image, 0.7, image1, 0.3, 0)

  return image, image1