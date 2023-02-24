import cv2
import os
import mediapipe as mp 
import shutil
import datetime
import time #to calculate frame per second 
import numpy as np

pose = []

lh = np.array([[res.x,res.y,res.z] for res in results.left_hand_landmarks.landmark]).flatten()

rh = np.array([[res.x,res.y,res.z] for res in results.right_hand_landmarks.landmark]).flatten()

