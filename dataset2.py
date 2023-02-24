# required for authentication
# import firebaseAuth as fba

# required for GUI
# from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QFileDialog, QComboBox, QTableWidget
# from PyQt5.QtCore import QTimer, QTime , Qt, QDate, QDateTime, QRect
# from PyQt5.QtGui import QImage, QPixmap, QImage, QPixmap
# from PyQt5 import QtWidgets, QtGui, QtCore
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
from PyQt5.uic import loadUi
# import requests
# import datetime
# import sqlite3
import imutils
import time
import csv
import sys
import os 

# required for face recognition
from numpy.lib.function_base import append
import face_recognition 
import numpy as np
import cv2 as cv
import dlib
from bing_image_downloader import downloader

# downloader.download("angry human face", limit=10, output_dir="images/")

img = cv.imread('images/angry human face/Image_3.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img = gray


face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

faces = face_cascade.detectMultiScale(img, 1.1, 4)

preferred_width = 300
preferred_height = 300

x0 , y0 , x_width, y_height = 0,0,0,0

for (x,y,w,h) in faces :
    x0 , y0 , x_width, y_height = x, y, w, h
    #cv.rectangle( img, (x,y), (x+w, y+h), (255,0,0), 2)
    # cv.rectangle( img, (146,585),( 333, 772), (0,255,0), 2)
    # cv.rectangle( img, (x,y), (x+w-100, y+h-300), (0,255,0), 2)

    # print( x, y, x+w, y+h )
#

# cv.imshow("out",img)
print('old original', img.shape)

print( 'x0, x0+x_width, y0 , y0+y_height' )
print( x0, x0+x_width, y0 , y0+y_height )

cropped_img = img[y0: y0+y_height, x0 : x0+x_width ]

#cv.imshow("out", cropped_img)
print('cropped', cropped_img.shape)

resized_img = cv.resize(cropped_img, (preferred_width, preferred_height))
#cv.imshow("out",resized_img)
#print('resized + cropped', resized_img.shape)

#cv.waitKey(0)

#cv.imwrite("test.jpg", resized_img)
cv.imwrite(os.path.join('images' , 'path.jpg'), resized_img)
# images_path = os.listdir('images/angry human face/')
# print(images_path)