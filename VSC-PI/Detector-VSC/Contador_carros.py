import cv2
from ultralytics import YOLO
import serial
import time


PORTA_ARDUINO = 'COM10'
LIMIAR_TROCA_B = 3   
LIMIAR_VOLTA_A = 1   

arduino = serial.Serial(PORTA_ARDUINO, 9600)
time.sleep(2)

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(1)

semaforo_atual = 'A'
ultimo_comando_enviado = None
contador_frames = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if contador_frames % 5 == 0:
        frame_small = cv2.resize(frame, (320, 240))
        results = model(frame_small)
        
        carros = 0
        for r in results:
            for box in r.boxes:
                if model.names[int(box.cls[0])] == "car":
                    carros += 1
        
       
        if semaforo_atual == 'A':
            if carros >= LIMIAR_TROCA_B:
                semaforo_atual = 'B'
                print(f"Mudando pra B (carros: {carros})")
        else:  
            if carros <= LIMIAR_VOLTA_A:
                semaforo_atual = 'A'
                print(f"Voltando pra A (carros: {carros})")
    
        if semaforo_atual != ultimo_comando_enviado:
            arduino.write(semaforo_atual.encode())
            ultimo_comando_enviado = semaforo_atual
            print(f"📨 Comando enviado: {semaforo_atual}")
        
        cv2.putText(frame, f"Carros: {carros}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"Semaforo: {semaforo_atual}", (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"Troca B: {LIMIAR_TROCA_B}+ | Volta A: <={LIMIAR_VOLTA_A}", 
                    (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    cv2.imshow("Contador", frame)
    
    
    if cv2.waitKey(1) == 27:
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()