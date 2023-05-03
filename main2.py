import os
import time
from cvzone.HandTrackingModule import HandDetector
import cv2
import db

cur,conn = db.init_db()
db.create_table(cur,conn)

cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("Resources/Background.png")

#importing all the images to a list 

folderPathModes = "Resources/Modes"         # its only for Modes like Type of Coffee Suger and Cup size 
listImgModesPath = os.listdir(folderPathModes)
listImgModes = []
for imgModePath in listImgModesPath :
    listImgModes.append(cv2.imread( os.path.join (folderPathModes , imgModePath)))   
print(listImgModes)


# Importing all the Icon to a list

folderPathIcons = "Resources/Icons"         # its only for Modes like Type of Coffee Suger and Cup size 
listImgIconsPath = os.listdir(folderPathIcons)
listImgIcons = []
for imgIconsPath in listImgIconsPath :
    listImgIcons.append(cv2.imread( os.path.join (folderPathIcons , imgIconsPath)))   



ModeType = 0 #for changing Selection mode

selection = -1  #0 is also is a selection 
counter = 0     # for wait and hold like an loading bar 
selectionSpeed = 5


detector = HandDetector(detectionCon=0.8 , maxHands=1) #if we want to change or increase number of hands then just increase maxHands number 
modePositions = [(1136,196) , (1000,384) , (1136,581) ]
counterPause = 0
selectionList = [-1 ,-1 , -1]

while True :
    success, img = cap.read()

    hands , img = detector.findHands(img)  #Find the hand and its Landmarks

    imgBackground[ 139 : 139 + 480  , 50 : 50+640 ] = img
    imgBackground[ 0 : 720 , 847 :1280 ] = listImgModes[ModeType]       #for change the mode just change listmode values 



    if hands and counterPause == 0  and ModeType < 3 :
      #hand 1
      hand1 = hands[0]
      fingers1 = detector.fingersUp(hand1)

      if fingers1 == [0,1,0,0,0] :            # [thumb , 1st finger , middle finger ,  , ]
        if selection != 1 :                    # we have to reset  again and again 

            counter = 1              
        selection = 1

      elif fingers1 == [0,1,1,0,0] :            # [thumb , 1st finger , middle finger ,  , ]
        if selection != 2 :                    # we have to reset  again and again 

            counter = 1              
        selection = 2

      elif fingers1 == [0,1,1,1,0] :            # [thumb , 1st finger , middle finger ,  , ]
        if selection != 3 :                    # we have to reset  again and again 

            counter = 1              
        selection = 3

      else :
        selection = -1 
        counter = 0 

      if counter > 0 :
        counter +=1 

        cv2.ellipse(imgBackground, modePositions[selection-1] , (103 , 103),0,0,counter*selectionSpeed,(0,255,0),20)      #ellipse(Background , (center point) , ( Radius ), angle of circle , starting angle , ending angle , color as BGR , thickness )

        if counter*selectionSpeed > 360 :       #for jump on next page 
          selectionList[ModeType]= selection    # its in Loop & we  have to perform  everthing outside  the loop 
          ModeType += 1
          counter = 0
          selection = -1
          counterPause = 1

          if selectionList[2] != -1 :
            imgBackground[636 : 636 + 65 , 542:542+65] = listImgIcons[5+ selectionList[2]]
          if ModeType == 3:
            time.sleep(2)
            ModeType = 0

            selection = -1  #0 is also is a selection 
            counter = 0     # for wait and hold like an loading bar
            coffeename = ''
            sugar = ''
            cup = ''
            if selectionList[0] == 1:
               coffeename = 'Latte'
            elif selectionList[0] == 2:
               coffeename = "Black"
            else:
               coffeename = "Lemon Tea"
            if selectionList[1] == 1:
               sugar = 'one'
            elif selectionList[1] == 2:
               sugar = 'two'
            else :
               sugar = 'three'
            if selectionList[2] == 1:
               cup = 'Small'
            elif selectionList[2] == 2:
               cup = 'Medium'
            else :
               cup = 'Large'
            
            db.insert_val(coffeename,sugar,cup,time.ctime(),cur,conn)



    #To Pause after each selection is made 
    if counterPause > 0 :           # for pause between 2 pages 
      counterPause+=1
      if counterPause > 60 :        #time of Pause 60 will be about 2's  according frame rate
        counterPause = 0

    # Add selection icon at the Bottom 
    if selectionList[0] != -1 :
      imgBackground[636 : 636 + 65 , 133:133+65] = listImgIcons[selectionList[0]-1]        #imgbackgroung[height , 636 is  height , 133 is width]

    if selectionList[1] != -1 :
      imgBackground[636 : 636 + 65 , 340:340+65] = listImgIcons[2+ selectionList[1]]

    if selectionList[2] != -1 :
      imgBackground[636 : 636 + 65 , 542:542+65] = listImgIcons[5+ selectionList[2]]
      
# Display Image
    #cv2.imshow("image", img)
    cv2.imshow("Background", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    # cv2.waitKey(1)