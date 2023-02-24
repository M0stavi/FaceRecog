import cv2
import os
import mediapipe as mp 
import datetime
import time #to calculate frame per second 

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

def med_detect(img,model):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img.flags.writeable = False
    results = model.process(img)
    img.flags.writeable = True
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    return img,results

def draw_lms(img, results):
    mp_drawing.draw_landmarks(img, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(img, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    
    return img

    
    
    

#to open web camera
cap = cv2.VideoCapture("F:/Online Class/4th year thesis/datasets/Sign language/Videos/paani/paani_2.mp4")           #we pass 0 as port number is 0 
# cap = cv2.VideoCapture(1)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
   
size = (frame_width, frame_height)


result = cv2.VideoWriter('F:/Online Class/4th year thesis/datasets/Sign language/Videos/paani/filename.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)

#calculating frame per second
prevTime = 0
currTime = 0


with mp_holistic.Holistic(min_detection_confidence=0.1, min_tracking_confidence=0.1) as holistic:
    sequence = 1
    while True:
        ret,frame = cap.read()
        #to convert images from bgr to rgb
        #  imgBGR = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        #  results = hands.process(imgBGR)
        #checking whether multiple hands were extracted or not
        #  print(results.multi_hand_landmarks) 
        
        img, results = med_detect(frame,holistic)
        
        # print(results)
        
        # print(len(results.left_hand_landmarks.landmark))
        
        # print(len(results.right_hand_landmarks.landmark))
        
        img = draw_lms(img,results)
        cnv = str(sequence)
        sequence = sequence+1      
        path = 'F:/Online Class/4th year thesis/datasets/Sign language/Frames/paani_2'
        ts = (datetime.datetime.now())
        ts = str(ts.timestamp())
        result.write(img)
        # print(type(ts))
        # print(type(cnv))
        # cnv = cnv+ts
        cv2. imwrite(os. path. join(path , 'paani_2'+ts+'.jpg'), img)    
        
        #  print(len(results.multi_hand_landmarks))

        #drawing hand landmarks on our hand
        # if results.multi_hand_landmarks :
        #     #  print(results.pose_landmarks)
        #     for handLandmarks in results.multi_hand_landmarks:   #calculating id's (there are 21 id's in total)
        #             for id,lm in enumerate(handLandmarks.landmark):
        #                 #print(id,lm)

        #                 h,w,c = img.shape
        #                 cx,cy = int(lm.x*w),int(lm.y*h) 
        #                 # print(id,cx,cy)

        #                 if id==4:
        #                     #drawing the circle on the landmarks
        #                     cv2.circle(img,(cx,cy),20,(255,0,255),cv2.FILLED)

        #             mpDraw.draw_landmarks(img,handLandmarks,mpHands.HAND_CONNECTIONS)      #connecting the landmarks on our hands
        #             # cv2.imwrite("saved.png",img)
        #             cnv = str(sequence)
        #             sequence = sequence+1      
        #             path = 'F:/Online Class/4th year thesis/datasets/Sign language/Frames'
        #             cv2. imwrite(os. path. join(path , 'saved'+cnv+'.jpg'), img)    

        # #calculating fps - fps defines how fast our object detection model processes our video and generates the desired output.
        # currTime = time.time()
        # fps = 1/(currTime - prevTime) #1 for per second  
        # prevTime = currTime
        # cv2.putText(img , str(int(fps)) ,(10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)


        cv2.imshow('Hand Gestures',img)
        if cv2.waitKey(1)==13 :          #if we press enter the web camera stops
            break
        
    result.release()
    cv2.destroyAllWindows()