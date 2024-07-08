import cv2
import mediapipe as mp

chest_ids = [11, 12, 13, 14]
counter =0
down= False
up = False


def drawLandMarks(frame, lmdraw, chest_ids):
    for id in chest_ids:
        cx = lmdraw[id][1]
        cy = lmdraw[id][2]
        cv2.circle(frame, (cx, cy), 5, (255, 255, 255), 2)
        cv2.circle(frame, (cx, cy), 15, (50, 0,255), 3)
    
    cv2.line(frame, (lmdraw[chest_ids[0]][1], lmdraw[chest_ids[0]][2]), 
             (lmdraw[chest_ids[2]][1], lmdraw[chest_ids[2]][2]), (255, 255, 255), 2, 1)
    
    cv2.line(frame, (lmdraw[chest_ids[1]][1], lmdraw[chest_ids[1]][2]), 
             (lmdraw[chest_ids[3]][1], lmdraw[chest_ids[3]][2]), (255, 255, 255), 2, 1)

    return frame



# cap = cv2.VideoCapture('vid1.mp4')
cap = cv2.VideoCapture(0)


mp_pose = mp.solutions.pose
mp_pose_drawing = mp.solutions.drawing_utils


with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as poses:
    while True:
        ret, frame = cap.read()
        if not ret:
            # cap = cv2.VideoCapture('vid1.mp4')
            # continue
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame.flags.writeable= False
        results = poses.process(frame)
        frame.flags.writeable = True

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        lmdraw = []
        # mp_pose_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if not results.pose_landmarks:
            continue

        for index, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = frame.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmdraw.append([index, cx, cy])
        
        if lmdraw:
            frame = drawLandMarks(frame, lmdraw, chest_ids)
            chest_down = (lmdraw[chest_ids[1]][2] > lmdraw[chest_ids[3]][2]) and (lmdraw[chest_ids[0]][2] > lmdraw[chest_ids[2]][2])
                
            if chest_down and not down:
                down = True
                up = False
            
            if not chest_down and down:
                down = False
                up = True
                counter += 1

        cv2.rectangle(frame, (20,50), (500, 150), (36, 80, 60), cv2.FILLED)
        cv2.putText(frame, f'Counter: {counter}', (40, 120), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255),2)
        
        cv2.imshow('Push Up Counter', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
