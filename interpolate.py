from ctypes import sizeof
import cv2
import os
import mediapipe as mp 
import shutil
import datetime
import time #to calculate frame per second 
import numpy as np

const_inf = 100000000000000

path = "F:/Online Class/4th year thesis/datasets/Sign language/point data"
out_path = "F:/Online Class/4th year thesis/datasets/Sign language/interpolated"

dir_list = os.listdir(path)

print(dir_list)

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
    sequence = 0
    long_seq=1000
    expected_sq = 0
    msd_lst = []
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
        # print("Data end"
        
        ext = 0
        
        for item in lst:
            if item==expected_sq:
                ext=1
        
        ts = (datetime.datetime.now())
                    
        ts = str(ts.timestamp())
        
        if ext==1:
        
            np.save(os.path.join(out_folder,child_folder+'_'+str(long_seq)+'_'+ts+'_'+str(sequence)),data)
            
        if ext == 0:
            msd_lst.append(expected_sq)
            prev = -1
            nxt = -1
            x = len(lst)
            for i in range(0,x-1):
                if expected_sq > lst[i] and expected_sq < lst[i+1]:
                    prev = lst[i]
                    nxt = lst[i+1]
            # if nxt!=prev:
            
            if nxt==prev:
                factor=1
            else:
                factor = (expected_sq-prev) / (nxt-prev)
            
            pr_ar = np.full(126,const_inf)
            
            nx_ar = np.full(126,const_inf)
            
            for ld in tem_dir:
                # print(ld)
                
                splt_txt = ld.split("_")
                
                # print(splt_txt)
                
                
                # if pnt == 'shundor_1_1664389748.840814_14.npy':
                ld_str = str(tem_path)
                # print("EIJE")
                point_data_path_2 = ld_str+"/"+ld
                # print(point_data_path_2)
            
                data=np.load(point_data_path_2)
                
                # print("Start")
                # print(data[0])
                # print("End")
                
                # print(data)
                
                final_split = splt_txt[4].split(".")
                
                # print(type(final_split[0]))
                
                num = int(final_split[0])
                
                if num == prev:
                    # print(prev)
                    pr_ar = data
                if num == nxt:
                    nx_ar = data
                    # print(nxt)
                    
            cur_ar = data
            
            
            
            for i in range(0,126):
                
                if nx_ar[i] != pr_ar[i]:
                    cur_ar[i] = factor*(nx_ar[i]-pr_ar[i])
                else:
                    cur_ar[i] = nx_ar[i]
                # print(factor*(nx_ar[i]-pr_ar[i]))
            data = cur_ar
            
            # print("Start")
            # print(cur_ar[0])
            # print("End")
            # print(cur_ar)
            np.save(os.path.join(out_folder,child_folder+'_'+str(long_seq)+'_'+ts+'_'+str(sequence)),cur_ar)
            
            
            # print("Expexted: ", expected_sq)
            # print("Pre ",prev,' ','next ', nxt)
            
            
        
        # print(msd_lst)
        
        long_seq = long_seq+1
        
        sequence = sequence+1
        
        expected_sq = expected_sq+1
    