import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime


path = 'C:\\Users\\paras\\OneDrive\\Documents\\VS CODE\\Face Attendance2\\images'
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

#cap = cv2.VideoCapture(0) #WebCam
img = cv2.imread('C:\\Users\\paras\\OneDrive\\Documents\\VS CODE\\Face Attendance2\\images\\BillGates.jpg')

while True:
    # ret, frame = img.read()
    faces = cv2.resize(img, (0, 0), None, 0.25, 0.25) #Resizing The Img Frame
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
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2) #Recognition rectangle
            attendance(name)

    cv2.imshow('Result', img)
    if cv2.waitKey(1) == 13:
        break