#!/usr/bin/env python3

import os
import cv2
import logging as log
import datetime as dt
from playsound import playsound

casc_path = "bin/data/haarcascade_frontalface_default.xml"
lock_command = "gnome-screensaver-command -l"
sound_path = "bin/data/lock_sound.mp3"


class FaceRecognition:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(casc_path)
        self.video_capture = cv2.VideoCapture(0)
        log.basicConfig(filename='bin/data/webcam.log', level=log.INFO)

    def get_frame(self):
        last_face_detected_time = dt.datetime.now()
        anterior = 0

        # Capture frame-by-frame
        ret, frame = self.video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if anterior != len(faces):
            anterior = len(faces)
            log.info("faces: " + str(len(faces)) + " at " + str(dt.datetime.now()))
            last_face_detected_time = dt.datetime.now()

        if len(faces) == 0:
            no_face_detected_in_seconds = int((dt.datetime.now() - last_face_detected_time).total_seconds())
            log.info(f"No face detected screen while be locked after {str(no_face_detected_in_seconds)} secondes")
            if no_face_detected_in_seconds == 5:
                log.info("Lock screen...")
                if sound_path:
                    playsound(sound_path)

                os.system(lock_command)
                return None

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("KO 2")
            return None

        return ret, frame
