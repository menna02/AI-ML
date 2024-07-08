import time
import mediapipe as mp
import cv2
import numpy as np

my_hand = mp.solutions.hands
my_hand_draw = mp.solutions.drawing_utils

tipsId = [4,8,12,16,20]

cap = cv2.VideoCapture(0)
cap.set(3, 512)
cap.set(4, 512)
with my_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            print('Failed to open Camera')
            break
        
        # frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame.flags.writeable = False
        results = hands.process(frame)
        frame.flags.writeable = True

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        lmdraw = []
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                my_hand_draw.draw_landmarks(frame, handLms, my_hand.HAND_CONNECTIONS)
            
            for id, lm in enumerate(handLms.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmdraw.append([id, cx, cy])
                cv2.circle(frame, (cx, cy), 5, (255, 0,
                                                255), cv2.FILLED)
        
        if len(lmdraw) != 0:
            fingers = []
            if lmdraw[tipsId[0]][1] > lmdraw[tipsId
                                            [0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            
            for id in range(1,5):
                if lmdraw[tipsId[id]][2] < lmdraw[tipsId[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            totalFingers = fingers.count(1)
            

            cv2.rectangle(frame, (20,20),(170,220), (0,255,0), cv2.FILLED)
            cv2.putText(frame, str(totalFingers), (45, 150), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2,
                        cv2.LINE_AA)
        
        current_time = str(time.ctime())
        cv2.putText(frame, current_time, (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        cv2.imshow('Live', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
    
            




