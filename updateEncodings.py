import cv2
import face_recognition
import os
from datetime import datetime
import time
import pymongo


startTime = datetime.now()
path = "reference_img"
images = []
className = []
myList = os.listdir(path)

try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["faceEncodedData"]
    database = mydb['encodedData']
    print('Databse connected')
except:
    print('DB not Connected ..!')

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
    * Dependencies : face_recognidation          *
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

encodeListKnown = findEncodings(images)
print('Encoding Completed')

time = datetime.now()
time = time.strftime('%I:%M:%S')

date = datetime.now()
date = date.strftime('%d/%m/%y')

#print(encodeListKnown)

encodedData = {
    "$set":{
        "Time":time,
        "Date":date,
        "Data":str(encodeListKnown)
    }
}

old = []
for i in database.find():
    print(i)
    old.append(i)

print(old)
try:
    database.update_one(old[2],encodedData)
    print("Data addded to Database")
except:
    print('Something went wrong..!')