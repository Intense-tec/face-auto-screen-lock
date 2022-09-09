#!/usr/bin/env python3

import os
import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
from playsound import playsound

casc_path = "haarcascade_frontalface_default.xml"
lock_command = "gnome-screensaver-command -l"
sound_path = "./lock_sound.mp3"

video_capture = cv2.VideoCapture(0)
last_face_detected_time = dt.datetime.now()
anterior = 0

face_cascade = cv2.CascadeClassifier(casc_path)
log.basicConfig(filename='webcam.log',level=log.INFO)

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    if anterior != len(faces):
        anterior = len(faces)
        print("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))
        last_face_detected_time = dt.datetime.now()

    if len(faces) == 0:
        no_face_detected_in_seconds = int((dt.datetime.now() - last_face_detected_time).total_seconds())
        print(f"No face detected screen while be locked after {str(no_face_detected_in_seconds)} secondes" )
        if no_face_detected_in_seconds == 5:
            print("Lock screen...")
            if sound_path:
                playsound(sound_path)

            os.system(lock_command)
            break

    # Display the resulting frame
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
