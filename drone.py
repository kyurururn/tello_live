import socket
import time
import cv2
import threading

def capture():
    while True:
        ret, frame = cap.read()
        cv2.imshow('Tello Camera View', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    # ビデオストリーミング停止
    sock.sendto('streamoff'.encode('utf-8'), TELLO_ADDRESS)
    
# ドローンの設定
TELLO_IP = "192.168.10.1"
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP,TELLO_PORT)

# ソケット通信の設定
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(('', TELLO_PORT))
sock.sendto("command".encode("utf-8"),TELLO_ADDRESS)

# カメラ受信用のアドレス
sock.sendto("streamon".encode(encoding="utf-8"), TELLO_ADDRESS)
TELLO_CAMERA_ADDRESS = 'udp://@0.0.0.0:11111'
time.sleep(1)
cap = cv2.VideoCapture(TELLO_CAMERA_ADDRESS)
time.sleep(1)
cap.open(TELLO_CAMERA_ADDRESS)
time.sleep(1)

thread = threading.Thread(target=capture)
thread.start()


while True: 
    msg = input()

    if msg == "q":
        print ('QUIT...')
        sock.sendto("land".encode(encoding="utf-8"),TELLO_ADDRESS)
        sock.close()  
        break

    msg = msg.encode(encoding="utf-8")
    sock.sendto(msg, TELLO_ADDRESS)