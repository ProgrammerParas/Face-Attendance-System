import time
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import random
import pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

unknown_face_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
unknown_face_letter = random.choice(unknown_face_string)


path = 'C:\\Users\\paras\\OneDrive\\Documents\\VS CODE\\Face Attendance\\images'
unknown_face_file_path = 'C:\\Users\\paras\\OneDrive\\Documents\\VS CODE\\Face Attendance'
images = []
personNames = []
myList = os.listdir(path)
print(myList)
for cu_img in myList:
    current_Img = cv2.imread(f'{path}/{cu_img}')
    images.append(current_Img)
    personNames.append(os.path.splitext(cu_img)[0])
print(personNames)


def faceEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


now = datetime.now() #getting current datetime
current_time = now.strftime("%Y-%m-%d")

unknown_face_timings = datetime.now()
unknown_face_file_time = unknown_face_timings.strftime('%H-%M-%S')


def attendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            time_now = datetime.now()
            tStr = time_now.strftime('%H:%M:%S')
            dStr = time_now.strftime('%D/%m/%Y')
            f.writelines(f'\n{name},{tStr},{dStr}')


encodeListKnown = faceEncodings(images)
print('All Encodings Complete!!!')

cap = cv2.VideoCapture(0) #WebCam

while True:
    ret, frame = cap.read()
    faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25) #Resizing The Img Frame
    faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB) #converting image into rgb

    facesCurrentFrame = face_recognition.face_locations(faces) #Locating Faces From WebCam
    encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame) #

    for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = personNames[matchIndex].upper()
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2) #Recognition rectangle
            attendance(name)
            speak_name = f'{name} Present'
            speak(speak_name)

        if matches[matchIndex]:
            name = personNames[matchIndex].upper()
            #print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            attendance(name)


        if faceDis[matchIndex]< 0.50:
            name = personNames[matchIndex].upper()
            attendance(name)
        else:
            name = 'Unknown'
            #unknown_face_file = f'Unknown{unknown_face_letter}.png'
            cv2.imwrite('Unknown.png', frame)
            speak('Unknown Face Detected')
            #print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0, 0, 255),2)
            cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0, 0, 255),cv2.FILLED)
            cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) == 13:
        break

cap.release()
cv2.destroyAllWindows()
