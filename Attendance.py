import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import time


startTime = datetime.now()
path = "scanning_img"
images = []
className = []
myList = os.listdir(path)
#print(myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    className.append(os.path.splitext(cl)[0])

print('''
     <|---Welcome To Auto Attendance system---|>
    **********************************************
''')
print('''\n
    **********************************************
    * Project Name : Automatic Attendance system *
    * Author       : Muhammad Ramzy              *
    * Dependencies : face_recognition            *
    *                numpy                       *
    *                cv2                         *
    *                datetime                    *
    * Date Created : 4/1/2020                    *
    * Date Modified: 4/3/2020                    *
    **********************************************
''')

print('Loding Reference Images ..')
time.sleep(1)
for name in className:
    print(name)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDatalist = f.readlines()
        nameList = []
        for line in myDatalist:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

encodeListKnown = findEncodings(images)
print('Encoding Completed')

cap = cv2.VideoCapture(0)

endTime = startTime - datetime.now()

print(f'encoding completed with {endTime}')

while True:
    succes, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGRA2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodeSCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceLoc in zip(encodeSCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = className[matchIndex].upper()
            print(name)
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
            markAttendance(name)

    cv2.imshow('Scanning your face .....',img)
    cv2.waitKey(100)