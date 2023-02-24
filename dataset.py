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
import cv2 as cv
# required for marking attendance
import numpy as np
import face_recognition 
from numpy.lib.function_base import append
from bing_image_downloader import downloader

downloader.download("angry human face", limit = 20, output_dir='images/angry')