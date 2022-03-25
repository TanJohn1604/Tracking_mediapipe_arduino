import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import  serial
import time
def nothing(x):
    pass
def CreateTrackBar_Init():
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("Lower - H", "Trackbars", 90, 179, nothing)
    cv2.createTrackbar("Lower - S", "Trackbars", 90, 179, nothing)

CreateTrackBar_Init()

def initConnection(port,baud):
    try:
        ser=serial.Serial(port,baud)
        print("Device connected")
        return ser
    except:
        print("Errorrrrrrr")
def sendData(se,data,digits):
    myString="$"
    for d in data:
        myString+= str(d).zfill(digits)
    try:
        se.write(myString.encode())
        print(myString)
    except:
        print("send fail")


pTime = 0
cTime = 0
cap = cv2.VideoCapture(1)
detector = htm.handDetector()
ser=initConnection("COM4",9600)
pan=90.00
tilt=90.00
x=0
y=0
w=0
h=0
width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
flag=1
flag2=0
c_fps=0
p_fps=0
f_fps=0
while True:
    Lower_H_Value = cv2.getTrackbarPos("Lower - H", "Trackbars")
    Lower_S_Value = cv2.getTrackbarPos("Lower - S", "Trackbars")
    success, img = cap.read()
    img = detector.findHands(img, draw=True )
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[8])
        if flag>5:
            flag=0
            objX = lmList[4][1]
            objY = lmList[4][2]
            errorPan = objY- height / 2
            errorTilt = objX  - width / 2
            print("------------------")
            print(lmList[4])
            print(errorPan)
            if abs(errorPan) > 10:
                pan=pan-errorPan/40
                # if errorPan > 0:
                #     pan = pan - 1
                # if errorPan < 0:
                #     pan = pan + 1

            if abs(errorTilt) > 10:
                tilt = tilt - errorTilt / 40

            if pan > 150:
                pan = 150
                print("pan out of range !!!")
            if tilt > 150:
                tilt = 150
                print("tilt out of range !!!")
            if pan < 20:
                pan = 20
                print("pan out of range !!!")
            if tilt < 20:
                tilt = 20
                print("tilt out of range !!!")


            sendData(ser, [int(pan),int(tilt) ], 3)
        flag=flag+1
    cTime = time.time()
    c_fps = 1 / (cTime - pTime)
    f_fps=c_fps*0.1+p_fps*0.9
    p_fps=f_fps
    pTime = cTime
    # cv2.line(img,(0,0),(200,int(height)),(255,0,0),1,1)
    cv2.line(img, (0,int(height / 2)), (int(width),int(height/2)), (255, 0, 0), 1, 1)
    cv2.line(img, (int(width/2), 0), (int(width/2), int(height)), (255, 0, 0), 2, 1)

    cv2.circle(img,(int(width/2),int(height/2)),15,(0,255,0),1,1)
    cv2.putText(img, str(int(f_fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)
    cv2.imshow("Image", img)
    key=cv2.waitKey(10)
    if key == 27:
        break
