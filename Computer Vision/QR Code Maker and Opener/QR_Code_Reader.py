import numpy as np
import cv2
import webbrowser
from pyzbar.pyzbar import decode


def qr_code_reader():
    cap = cv2.VideoCapture(0)
    cap.set(3, 480)
    cap.set(4, 480)

    qr_code_found = False
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        for barcode in decode(frame):
            qr_data = barcode.data.decode('utf-8')
            print(qr_data)

            cv2.rectangle(frame, (barcode.rect.left, barcode.rect.top),
                          (barcode.rect.left + barcode.rect.width , barcode.rect.top + barcode.rect.height),
                          (0, 0, 255), 2)

            if qr_data.startswith('http'):
                webbrowser.open(qr_data)
                qr_code_found = True
                break

        cv2.imshow('QR Code Reader', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if qr_code_found:
            break

    cap.release()
    cv2.destroyAllWindows()
    
        
            

        
qr_code_reader()