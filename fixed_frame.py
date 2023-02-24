from itertools import count
from math import ceil, floor
import cv2
import os
import mediapipe as mp 
import shutil
import datetime
import time #to calculate frame per second 
import numpy as np

const_inf = 100000000000000

path = "F:/captures/4th year thesis/datasets/Sign language/interpolated"
out_path = "F:/captures/4th year thesis/datasets/Sign language/fixed"

dir_list = os.listdir(path)

# print(dir_list)



for fol in dir_list:
    # print(fol)
    child_folder = fol
    out_folder = os.path.join(out_path,child_folder)
    tem_path = path+"/"+fol
    tem_dir = os.listdir(tem_path)
    if os.path.exists(out_folder):
        shutil.rmtree(out_folder)
    os.mkdir(out_folder)
    # print(tem_dir)
    
    count = 0
    for pnt in tem_dir:
        count = count+1
    count = count/30
    # print(count)
    
    id = count
    sequence = 0
    long_seq=1000
    for iii in range(0,28):
        # print(tem_dir[0])
        
        ts = (datetime.datetime.now())
                    
        ts = str(ts.timestamp())
        
        if id<=1:
            # print()
            point_data_path = tem_path+"/"+tem_dir[0]
            data=np.load(point_data_path)
            np.save(os.path.join(out_folder,child_folder+'_'+str(long_seq)+'_'+ts+'_'+str(sequence)),data)
            # print(data)
            
        else:
            flr = floor(id)
            cl = ceil(id)
            
            if flr==cl:
            
                # print("ST")
                
                # print(flr)
                
                # print(cl)
                
                # print("EN")
                
                point_data_path = tem_path+"/"+tem_dir[cl]
                data=np.load(point_data_path)
                np.save(os.path.join(out_folder,child_folder+'_'+str(long_seq)+'_'+ts+'_'+str(sequence)),data)
                # print(data)
            
            else:
                factor = (id-flr)/(cl-flr)
                
                point_data_path = tem_path+"/"+tem_dir[flr]
                data1=np.load(point_data_path)
                
                point_data_path = tem_path+"/"+tem_dir[cl]
                data2=np.load(point_data_path)
                
                data = data1
                
                for i in range(0,126):
                    data[i] = factor*(data2[i]-data1[i])
                np.save(os.path.join(out_folder,child_folder+'_'+str(long_seq)+'_'+ts+'_'+str(sequence)),data)
                
                # print(data)
            
        
        
        
        sequence = sequence+1
        long_seq = long_seq+1
        id=id+count
        
    
    