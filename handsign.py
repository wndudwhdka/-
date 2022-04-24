import cv2
import mediapipe as mp
import time 
import numpy as np 

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(cv2.CAP_DSHOW+0) # 기본으로 설정되있으면 0, 그것이 아니면 cv2.CAP_DSHOW+0
prevTime = 0
coordflag = 0
prevcoordx = 0
prevcoordy = 0


def draw_by_location(image, xlocations, ylocations): # 이미지 핸들러에 적혀 있는 구역을 바탕으로 선을 그림
  dimensions = image.shape
 
  image1 = np.zeros([dimensions[0],dimensions[1],3],dtype =np.uint8)
 
  for i in range(int((len(xlocations)))-1):

    cv2.line(image1,(int(xlocations[i]),int(ylocations[i])),(int(xlocations[i+1]),int(ylocations[i+1])),(255,255,255),3)

  
  image = cv2.addWeighted(image, 0.7, image1, 0.3, 0)

  return image, image1

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue
    
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
   
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        # mp_drawing.draw_landmarks(
        #     image,
        #     hand_landmarks,
        #     mp_hands.HAND_CONNECTIONS,
        #     mp_drawing_styles.get_default_hand_landmarks_style(),
        #     mp_drawing_styles.get_default_hand_connections_style())

        coordx = hand_landmarks.landmark[8].x*width
        coordy = hand_landmarks.landmark[8].y*height
          # draw_by_location(image,list_hand_locations)
          # print(current_coord)
          # print(list_hand_locations)
          # print('\n')

          # for hand_location in list_hand_locations:
          #   image=draw_by_location(image, hand_location)

       
        if (coordflag==0): # 초기에 플래그를 초기화 홤
          xcoord_array = np.array([int(coordx)])
          ycoord_array = np.array([int(coordy)])
          coordflag = 1

        else:          
          xcoord_array=np.append(xcoord_array,[int(coordx)])
          ycoord_array=np.append(ycoord_array,[int(coordy)])
        
          image, image1 = draw_by_location(image, xcoord_array, ycoord_array)
          print(len(xcoord_array)-len(ycoord_array))
       
        
    image = cv2.flip(image, 1)
    curTime = time.time()
    sec = curTime - prevTime
    prevTime = curTime
    fps = 1/(sec)
    str = "FPS : %0.1f" % fps
    cv2.putText(image, str, (0,100), cv2.FONT_HERSHEY_SIMPLEX,3,(255,255,255))

    cv2.imshow('MediaPipe Hands',image)
    
   
    
    if cv2.waitKey(5) & 0xFF == 27:
      coordflag = 0
      cv2.imwrite('sign.png',image1)
      break

cap.release()