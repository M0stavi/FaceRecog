import cv2
import os
import mediapipe as mp 
import shutil
import datetime
import time #to calculate frame per second 
import numpy as np

const_inf = -1

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

def extract_key_points(result):
    lh = np.array([[res.x,res.y,res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.full(126,const_inf)

    rh = np.array([[res.x,res.y,res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.full(126,const_inf)
    
    return np.concatenate([lh,rh])    


path = "F:/captures/4th year thesis/datasets/Sign language/imposed/Vid/shundor_1.mp4"

out_path = "F:/captures/4th year thesis/datasets/Sign language/imposed/Frames"

point_out = "F:/captures/4th year thesis/datasets/Sign language/imposed/Points"

# dir_list = os.listdir(path)

# print(dir_list)

cap = cv2.VideoCapture(path)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

prevTime = 0
currTime = 0

with mp_holistic.Holistic(min_detection_confidence=0.1, min_tracking_confidence=0.1) as holistic:
    sequence = 0
    long_seq = 1000
    while (cap.isOpened()):
        
        # if cap.isOpened() == False : 
        #     break
        
        ret,frame = cap.read()
        
        if ret:
        
            img, results = med_detect(frame,holistic)
            
            img = draw_lms(img,results)
            
            ts = (datetime.datetime.now())
            
            ts = str(ts.timestamp())
            
            keypoints = extract_key_points(results)
            
            # if sequence == 0:
            #     print(keypoints)
            
            # if keypoints.shape() =126:
            
            np.save('F:/captures/4th year thesis/datasets/Sign language/imposed/Points/'+str(long_seq),keypoints)
            
            # sequence = sequence+1
            # long_seq = long_seq+1
            
            sq = str(sequence)
            
            cv2. imwrite('F:/captures/4th year thesis/datasets/Sign language/imposed/Frames/'+str(long_seq)+'.jpg', img)
            
            # cv2.imshow('Hand Gestures',img)
            
            sequence = sequence+1
            long_seq = long_seq+1
            
            if cv2.waitKey(1)==13 : 
                break
        
        else:
            break
    cap.release()
    cv2.destroyAllWindows() 
            
            
                
                
        
        
        
        
        
        