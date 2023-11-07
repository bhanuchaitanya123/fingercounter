import cv2
import os 
import time
import HandTracking as htm
wcam,hcam=640,480
cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
folderpath="C:\\Users\\munab\\OneDrive\\python\\fingers"
mylist=os.listdir("fingers")
overlaylist=[]
for impath in mylist:
    image=cv2.imread(f'{folderpath}\\{impath}')
    overlaylist.append(image)
detector=htm.handDetector()
tipids=[4,8,12,16,20]
while True:
    r,img=cap.read()
    #img = cv2.resize(img, (800, 600))
    img=cv2.resize(img,(1000,1000))
    img=detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    fingers=[]
    if len(lmlist) != 0:
      if lmlist[tipids[0]][1] > lmlist[tipids[0]-1][1]:
        fingers.append(1)
      else:
        fingers.append(0)
      for id in range(1,5):
        if lmlist[tipids[id]][2] < lmlist[tipids[id]-2][2]:
           fingers.append(1)
        else:
            fingers.append(0)
      totalfingers=fingers.count(1)
      print(totalfingers)
      #if totalfingers != 0:
      if detector.results.multi_hand_landmarks:
            myHand=detector.results.multi_hand_landmarks[0]
            for id,lm in enumerate(myHand.landmark):
                h,w,c=img.shape
                
                if lmlist[tipids[0]][1] > lmlist[tipids[0]-1][1]:
                   cx,cy=int(lm.x * w) , int(lm.y * h)
                   try:
                     h,w,c=overlaylist[totalfingers-1].shape
                     img[lmlist[tipids[0]][1]:h+ lmlist[tipids[0]][1],lmlist[tipids[0]][1]:w+ lmlist[tipids[0]][1]]=overlaylist[totalfingers-1]
                   except:
                       h,w,c=overlaylist[totalfingers-1].shape
                       img[0:h,0:w]=overlaylist[totalfingers-1]
      
    cv2.imshow("image",img)
    cv2.waitKey(1)
