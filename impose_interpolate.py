from ctypes import sizeof
import cv2
import os
import mediapipe as mp 
import shutil
import datetime
import time #to calculate frame per second 
import numpy as np

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

def draw_lms(img, results):
    mp_drawing.draw_landmarks(img, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(img, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

const_inf = 100000000000000

path = "F:/Online Class/4th year thesis/datasets/Sign language/point data"
out_path = "F:/Online Class/4th year thesis/datasets/Sign language/interpolated"

img_in = "F:/Online Class/4th year thesis/datasets/Sign language/Frames"

img_out = "F:/Online Class/4th year thesis/datasets/Sign language/imposed"

dir_list = os.listdir(path)

path_collect = "F:/Online Class/4th year thesis/datasets/Sign language/interpolated"

# print(dir_list)

# msd_lst = []

for fol in dir_list:
    # print(fol)
    child_folder = fol
    out_folder = os.path.join(out_path,child_folder)
    tem_path = path+"/"+fol
    tem_dir = os.listdir(tem_path)
    
    # print(tem_dir)
    id = 0
    lst=[]
    for pnt in tem_dir:
        # print(pnt)
        # if pnt == 'shundor_1_1664389748.840814_14.npy':
        tf=1
        pnt_str = str(tem_path)
        point_data_path = pnt_str+"/"+pnt
        # print(point_data_path)
        data=np.load(point_data_path)
        # print("Data start")
        # print(len(data))
        # print(data[0])
        # print(data)
        # print("Data end")
        for dt in data:
            # print("St")
            # print(dt)
            # print("End")
            if dt == const_inf:
                # print(dt)
                tf=0
        if tf==1:
            lst.append(id)
        id=id+1
    # print(fol)
    # print(lst)
    expected_sq=0
    msd_lst = []
    for pnt in tem_dir:
        # print(pnt)
        # if pnt == 'shundor_1_1664389748.840814_14.npy':
        tf=1
        pnt_str = str(tem_path)
        point_data_path = pnt_str+"/"+pnt
        # print(point_data_path)
        # data=np.load(point_data_path)
        # print("Data start")
        # print(len(data))
        # print(data[0])
        # print(data)
        # print("Data end"
        
        ext = 0
        
        for item in lst:
            if item==expected_sq:
                ext=1
            
        if ext == 0:
            msd_lst.append(expected_sq)
            
        expected_sq = expected_sq+1
    # print(msd_lst)
    
    if len(msd_lst) == 0:
        continue
    
    dir_list_img = os.listdir(img_in)
    
    # print(dir_list_img)
    
    sq_img = 0
    long_seq_img = 1000
    for fol_img in dir_list_img:
        child_folder_img = fol_img
        out_folder_img = os.path.join(img_out,child_folder_img)
        tem_path_img = img_in+"/"+fol_img
        tem_dir_img = os.listdir(tem_path_img)
        if os.path.exists(out_folder_img):
            shutil.rmtree(out_folder_img)
        os.mkdir(out_folder_img)
        
        # print(tem_path_img)
        for frame in tem_dir_img:
            # print(frame)
            img_data_path = tem_path_img+"/"+frame
            # print(img_data_path)
            img  = cv2.imread(img_data_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            ts = (datetime.datetime.now())
            
            x = len(msd_lst)
            
            missed = 0
            
            for i in range(0,x):
                if sq_img==msd_lst[i]:
                    missed  = 1
                    
            if missed:
                # print(sq_img)
                dir_list_colc = os.listdir(path_collect)
                
                for fol_colc in dir_list_colc:
                    # print(fol)
                    child_folder_colc = fol_colc
                    # out_folder = os.path.join(out_path,child_folder)
                    tem_path_colc = path_collect+"/"+fol_colc
                    tem_dir_colc = os.listdir(tem_path_colc)
                    
                    # print(tem_dir)
                    id = 0
                    lst=[]
                    for pnt_colc in tem_dir_colc:
                        # print(pnt)
                        # if pnt == 'shundor_1_1664389748.840814_14.npy':
                        tf=1
                        pnt_str_colc = str(tem_path_colc)
                        point_data_path_colc = pnt_str_colc+"/"+pnt_colc
                        # print(pnt_colc)
                        str1 = pnt_colc.split("_")
                        # print(str1)
                        str2 = str1[4].split(".")
                        # print(str2)
                        num_colc = int(str2[0])
                        if num_colc == sq_img:
                            data=np.load(point_data_path_colc)
                            
                            # print(data)
                            
                            # print(data[0])
                            
                            dt = data.tolist()
                            
                            # print(dt)
                            
                            x = dt[0]
                            y = dt[1]
                            
                            # img = draw_lms(img,data)
                            cv2.circle(img, (x,y), 2, (255,0,0), 2)
                
            
            ts = str(ts.timestamp())
            # cv2.imshow("frame", img)
            cv2. imwrite(os. path. join(out_folder_img
                                                , child_folder_img+'_'+str(long_seq_img)+"_"+ts+"_"+str(sq_img)+'.jpg'), img)
            
            long_seq_img = long_seq_img+1
            sq_img = sq_img+1
            
            
            
    
    
    
    
    
    
    