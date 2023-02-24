from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import imutils
import time
import dlib
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDialog, QMessageBox, QFileDialog, QComboBox, QTableWidget
from PyQt5.QtCore import QSequentialAnimationGroup, QTimer, QTime , Qt, QDate, QDateTime, QRect
from PyQt5.QtGui import QIcon, QImage, QPixmap, QImage, QPixmap
from PyQt5.uic import loadUi
import sys
import os 
import requests
import sqlite3
import firebaseAuth as fba
import datetime
import shutil
import os.path

import cv2 as cv
import numpy as np
import os 
import face_recognition 
from datetime import datetime
import csv


# path = 'root/images'
# images = []
# classNames = []
# myList = os.listdir(path)

# print(myList) # names of image files

# for cl in myList:
#   currentImg = cv.imread(f'{path}/{cl}')
#   images.append(currentImg)
#   classNames.append(os.path.splitext(cl)[0] )
# print(classNames) # names of image files without extension

# def create_new_csv(csv_filename):

#     ############################################################################################################
#                 #  CREATE A NEW CSV AND CLOSE IT WE WILL READ THAT LATER
#     ############################################################################################################

#     # now = datetime.now()
#     # dtString = now.strftime('%d-%m-%Y')
#     # courseCode = "CSE-3207"
      
#     # csv_filename = '{}-{}'.format(courseCode,dtString)

#     attendance_path = 'root/Attendance'
  
#     with open(f'{attendance_path}/{csv_filename}.csv','w+') as f:
#       f.close()

#     #############################################################################################################


# def findEncodings(images):
#   encodeList = []
#   for img in images:
#     img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
#     encode = face_recognition.face_encodings(img)[0]
#     encodeList.append(encode)

#   return encodeList

# def markAttendance(name):

#   now = datetime.now()
#   dtString = now.strftime('%d-%m-%Y')
#   courseCode = "CSE-3207"
      
#   csv_filename = '{}-{}'.format(courseCode,dtString)

#   attendance_path = 'root/Attendance'
  
#   with open(f'{attendance_path}/{csv_filename}.csv','r+') as f:

#     myDataList = f.readlines()
#     namelist = []
#     for line in myDataList:
#       entry = line.split(',')
#       namelist.append(entry[0])
#     if name not in namelist:
#       now = datetime.now()
#       TIMEString = now.strftime('%I:%M:%S')
#       f.writelines(f'\n{name},{TIMEString}')  

# encodeListKnown = findEncodings(images)
# # print(len(encodeListKnown))
# print('Encoding complete')

# # cap = cv.VideoCapture("v4.mp4")
# cap = cv.VideoCapture(0)

# csv_created = False

# while True:
#   success, img = cap.read()
#   imgSmall = cv.resize(img,(0,0),None, 0.25,0.25) 
#   imgSmall = cv.cvtColor(imgSmall, cv.COLOR_BGR2RGB)

#   if (csv_created == False ):
  
#     now = datetime.now()
#     dtString = now.strftime('%d-%m-%Y')
#     courseCode = "CSE-3207"
#     csv_filename = '{}-{}'.format(courseCode,dtString)

#     create_new_csv(csv_filename)

#     csv_created = True


#   facesCurrentFrame = face_recognition.face_locations(imgSmall)
#   encodesCurrentFrame = face_recognition.face_encodings(imgSmall, facesCurrentFrame)

#   for encodeFace, faceLoc in zip(encodesCurrentFrame,facesCurrentFrame):
#     matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
#     faceDistance = face_recognition.face_distance(encodeListKnown,encodeFace)
#     #print(faceDistance) # the lesser the distance the best match it is 
#     matchIndex = np.argmin(faceDistance)

#     if matches[matchIndex]:
#       s_name = classNames[matchIndex]
#       name = ''
#       print(s_name)
#       # for xx in s_name:
#       #   if xx == '_':
#       #     break
#       #   name = name+xx
#       name = s_name.split('_')[0]
        
#       print(name)
#       y1, x2, y2, x1 = faceLoc
#       y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
#       cv.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
#       # cv.rectangle(img,(x1,y1-35),(x2,y2),(0,255,0),cv.FILLED)
#       cv.putText(img,name,(x1+6,y2-6),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
      
#       markAttendance(name)

#     else:
#       y1, x2, y2, x1 = faceLoc
#       y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
#       cv.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
#       # cv.rectangle(img,(x1,y1-35),(x2,y2),(0,255,0),cv.FILLED)
#       cv.putText(img,'Unknown',(x1+6,y2-6),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
#       print("notFound")

#   cv.imshow("Output",img) 
#   if cv.waitKey(1) & 0xFF == ord('p'):
#         break

# cap.release()
# cv.destroyAllWindows()



###########################################

class Face_Detection_Window(QMainWindow):
  def __init__(self):
    super(Face_Detection_Window,self).__init__()
    loadUi('UI/detect_ui.ui',self)
 
    user = {}
    user['email'] = 'user'
    self.user = user
    self.logic = 0
    self.cam_is_on = False

    
    self.path = "root/images"
    self.images = []
    self.classNames = []
    self.myList = os.listdir(self.path)
    self.cache_data = []
    self.csv_filename = ""

    for cl in self.myList:
      currentImg = cv.imread(f'{self.path}/{cl}')
      self.images.append(currentImg)
      self.classNames.append(os.path.splitext(cl)[0] )
      # print(self.classNames) # names of image files without extension
    
    self.img_label.setText("")

    self.logout_btn.clicked.connect( self.logout )
    self.start_attendance_btn.clicked.connect( self.showwebcam_btn_function )
    self.stop_attendance_btn.clicked.connect( self.stop_webcam_btn_function )
    self.select_img_btn.clicked.connect( self.select_img_from_pc )
    self.clear_btn.clicked.connect( self.clear_input )


  def clear_input(self):
      self.name_input.setText('')
 
  def select_img_from_pc(self):
      new_name = self.name_input.text().strip()
      
      if( new_name != '') :
            fname_tuple = QFileDialog.getOpenFileName(self, 'Open file', 'D:\ms-excel', ' ( *.png *.jpg)') # this is the default directory 
            filename = fname_tuple[0] # WITHOUT EXTENSION 

            # print(filename, 'file selected')

            ext = filename.split('.')[-1]

            file_source = filename
            file_destination = 'root/images'

            renamed_file = f'{file_destination}/{new_name}.{ext}'
            # print( os.listdir('root/images/') )
            # if file exist in os.listdir then do not copy 

            if not os.path.exists(renamed_file) :

                shutil.move( file_source, renamed_file)
                #moved successfully
                self.clear_input()
            else :
                print('this filename already exists in the dir')
                
      else :
          print('enter a name first')
      
  def stop_webcam_btn_function(self):
    if (self.cam_is_on ) :
      self.logic = 3
      self.markattendance_err_label.setText("Stopped Webcam...")

  def showwebcam_btn_function(self):
    
      
      print('Encoding START')

      # now = datetime.datetime.now()
      # dtString = now.strftime('%d-%m-%Y')
      
      # csv_filename = '{}-{}'.format(self.course_code,dtString)
      #     # MAIN TOKEN

      # fields = ["Serial No.", "Roll No.", "Time"]

      # with open("{}.csv".format( csv_filename ), 'w', newline='') as file:
      #       writer = csv.writer(file)
      #       writer.writerow(fields)

      # from datetime import datetime
      self.markattendance_err_label.setText("Loading ...")
  
      # cap = cv.VideoCapture(0)

      encodeListKnown = self.findEncodings( self.images)
      print('Encoding DONE')

      cap = cv.VideoCapture(0)

      self.cam_is_on = True
      # check further same csv exist kore ki na
      csv_created = False
      arr = []
      for i in range(125):
                  arr.append(0)

      # while ( cap.isOpened() ):
      while ( self.logic == 0 ):
        ret, frame = cap.read()

        if ret == True:
          self.markattendance_err_label.setText("Detecting...")

          self.display_the_img(frame,1)

          imgSmall = cv.resize(frame,(0,0),None, 0.25,0.25)
          imgSmall = cv.cvtColor(imgSmall, cv.COLOR_BGR2RGB)

          facesCurrentFrame = face_recognition.face_locations(imgSmall)
          encodesCurrentFrame = face_recognition.face_encodings(imgSmall, facesCurrentFrame)
          for encodeFace, faceLoc in zip(encodesCurrentFrame,facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDistance = face_recognition.face_distance(encodeListKnown,encodeFace)
            #print(faceDistance) # the lesser the distance the best match it is 
            matchIndex = np.argmin(faceDistance)
          
            if matches[matchIndex]:
                classNames = self.classNames
                s_name = classNames[ matchIndex ]
                name = ''
                
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                # cv.rectangle(img,(x1,y1-35),(x2,y2),(0,255,0),cv.FILLED)
                cv.putText(frame,s_name,(x1+6,y2-6),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

                self.display_the_img(frame,1)
    
                # self.markAttendance(name, csv_filename)

                print( s_name + " attended")
            else:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
                # cv.rectangle(img,(x1,y1-35),(x2,y2),(0,255,0),cv.FILLED)
                cv.putText(frame,'Unknown',(x1+6,y2-6),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                print("Unknown Face Detected")
                self.display_the_img(frame,1)

        k = cv.waitKey(1)

        if  self.logic == 3 :
              break 

      self.logic = 0
      
      self.markattendance_err_label.setText("Detected Successfully ")
      self.img_label.setText("")

    
  def display_the_img(self,img,w):

    # image = cv.resize(img, (640, 480)) eta k half kore disi
    image = cv.resize(img, (320, 240))

    qformat = QImage.Format_Indexed8
    if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
    outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
    outImage = outImage.rgbSwapped()
    self.img_label.setPixmap(QPixmap.fromImage(outImage))
    self.img_label.setScaledContents(True)

  def findEncodings(self, images ):
    encodeList = []
    for img in self.images :
      img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
      encode = face_recognition.face_encodings(img)[0]
      encodeList.append(encode)

    print('Encoding ... ')
    return encodeList
 
  def logout(self):
    
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)

    msg.setText('Are you sure to Logout?')
          # msg.setInformativeText("This is additional information")
    msg.setWindowTitle("Logout Confirmation")
          # msg.setDetailedText("The details are as follows:")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.setDefaultButton(QMessageBox.Cancel)
    msg.buttonClicked.connect(self.logout_confirmation)
	
    retval = msg.exec_()
   
  def logout_confirmation(self, i):

    # if OK button is clicked then logout
    if ( i.text() == "OK" ):
      login = Login()
      widget.addWidget(login)
      widget.setWindowTitle('Login') 
      widget.setFixedSize(470,570)
      widget.setCurrentIndex(widget.currentIndex()+1)


class Login(QMainWindow):
  def __init__(self):
    super(Login,self).__init__()
    loadUi('UI/login_ui.ui',self)
 
    self.submit_btn.clicked.connect(self.loginFunction)

  def loginFunction(self):
        # email = self.email_input.text()
        # password = self.password_input.text()
         
        self.mainappwindow = Face_Detection_Window()
        # self.mainappwindow.welcome_label.setText(user['email'])
        widget.addWidget(self.mainappwindow)
        widget.setWindowTitle('Face Detection Application') 
        widget.setFixedSize(770,570)
        widget.setCurrentIndex(widget.currentIndex()+1)
    

# main
app = QApplication(sys.argv)
mainWindow = Login()

widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setWindowTitle('Login') 
widget.setFixedSize(470,570)
widget.show()

try:
  sys.exit(app.exec_())
except :
  print("EXIT")
