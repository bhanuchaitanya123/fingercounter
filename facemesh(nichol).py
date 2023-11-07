import cv2
import mediapipe as mp
import numpy as np
from cvzone.PlotModule import LivePlot
plotY=LivePlot(1000,1000,[80,180])
counter=0
stage=0
#text=input("enter arms or hip or pushups:")
text='hip'
mp_drawing=mp.solutions.drawing_utils
mp_pose=mp.solutions.pose
cap=cv2.VideoCapture("C:\\Users\\munab\\OneDrive\\python\\static\\Image\\VID_20231029_143712.mp4")
with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    _,frame=cap.read()
    image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    image.flags.writeable=False
    results=pose.process(image)
    image.flags.writeable=True
    image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    image=cv2.resize(image,(1000,1200))
    #[640,480]
    try:
        landmarks=results.pose_landmarks.landmark
        '''print(len(landmarks))
        for lan in mp_pose.PoseLandmark:
            print(lan)'''
        #print(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value])
        def calculate_angle(a,b,c):
            a=np.array(a)
            b=np.array(b)
            c=np.array(c)
            radians=np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
            angle=np.abs(radians*180.0/np.pi)
            if angle >180.0:
                angle=360-angle
            return angle
        shoulder=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow=[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist=[landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        angle=calculate_angle(shoulder,elbow,wrist)
        
        rshoulder=[landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        relbow=[landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        rwrist=[landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        rangle=calculate_angle(rshoulder,relbow,rwrist)

        hip=[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        ankle=[landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        dangle=calculate_angle(shoulder,hip,ankle)
        
        rhip=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        rankle=[landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        langle=calculate_angle(rshoulder,rhip,rankle)
        
        #print(angle)
        cv2.putText(image,str(angle),tuple(np.multiply(elbow ,[1000,1200]).astype(int)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(image,str(rangle),tuple(np.multiply(relbow ,[1000,1200]).astype(int)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(image,str(dangle),tuple(np.multiply(hip ,[1000,1200]).astype(int)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)        
        cv2.putText(image,str(langle),tuple(np.multiply(rhip ,[1000,1200]).astype(int)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)

        if text == 'arms':
          if angle > 150 and rangle > 150:
            stage="down"
          if angle < 40 and rangle < 40 and stage == 'down':
            stage='up'
            counter+=1
            print(counter)
        elif text == 'pushups':
          if angle > 160 and rangle > 160:
            stage="down"
          if angle < 85 and rangle < 85 and stage == 'down':
            stage='up'
            counter+=1
        elif text == 'hip':
          if dangle > 160 and langle > 160:
            stage="up"
          if dangle < 105 and langle < 105 and stage == 'up':
            stage='down'
            counter+=1    
    except:
        pass
    try:
     if text == 'hip':
       imgplot=plotY.update(dangle,rangle)
       cv2.imshow('l',imgplot)
     elif text == 'arms':
       imgplot=plotY.update(angle,langle)
       cv2.imshow('l',imgplot)
     elif text == 'pushups':
       imgplot=plotY.update(angle,rangle)
       cv2.imshow('l',imgplot)
     cv2.rectangle(image,(0,0),(225,73),(245,117,16),-1)
     cv2.putText(image,str(counter),(10,60),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)
     mp_drawing.draw_landmarks(image,results.pose_landmarks,mp_pose.POSE_CONNECTIONS)
     #print(mp_pose.POSE_CONNECTIONS)
     mp_drawing.draw_landmarks(image,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,mp_drawing.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),mp_drawing.DrawingSpec(color=(245,66,230),thickness=2,circle_radius=2))
     cv2.imshow('i',image)
     if cv2.waitKey(10) & 0xFF == ord('q'):
      break
    except:
      pass
cap.release()
cv2.destroyAllWindows()
