from flask import Flask, render_template, Response, jsonify
from ultralytics import YOLO
import cv2
import serial
import time
import threading
from collections import deque

app = Flask(__name__)

# Configurações
PORTA_ARDUINO = 'COM10'
LIMIAR_TROCA_B = 3   
LIMIAR_VOLTA_A = 1   

# Variáveis globais
class SemaforoController:
    def __init__(self):
        self.semaforo_atual = 'A'
        self.ultimo_comando_enviado = None
        self.carros_detectados = 0
        self.frame_atual = None
        self.running = True
        self.arduino = None
        self.model = None
        self.cap = None
        
    def init_arduino(self):
        try:
            self.arduino = serial.Serial(PORTA_ARDUINO, 9600)
            time.sleep(2)
            return True
        except:
            print("Arduino não conectado - modo simulação")
            self.arduino = None
            return False
    
    def init_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.model = YOLO("yolov8n.pt")
        
    def process_frame(self):
        contador_frames = 0
        
        while self.running:
            if self.cap is None:
                break
                
            ret, frame = self.cap.read()
            if not ret:
                break
            
            if contador_frames % 5 == 0:
                frame_small = cv2.resize(frame, (320, 240))
                results = self.model(frame_small)
                
                carros = 0
                for r in results:
                    for box in r.boxes:
                        if self.model.names[int(box.cls[0])] == "car":
                            carros += 1
                
                self.carros_detectados = carros
                
                # Lógica do semáforo
                if self.semaforo_atual == 'A':
                    if carros >= LIMIAR_TROCA_B:
                        self.semaforo_atual = 'B'
                        print(f"Mudando pra B (carros: {carros})")
                else:
                    if carros <= LIMIAR_VOLTA_A:
                        self.semaforo_atual = 'A'
                        print(f"Voltando pra A (carros: {carros})")
                
                # Enviar comando para Arduino
                if self.semaforo_atual != self.ultimo_comando_enviado:
                    if self.arduino:
                        self.arduino.write(self.semaforo_atual.encode())
                    self.ultimo_comando_enviado = self.semaforo_atual
                    print(f"📨 Comando enviado: {self.semaforo_atual}")
                
                # Adicionar informações no frame
                cv2.putText(frame, f"Carros: {carros}", (20, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, f"Semaforo: {self.semaforo_atual}", (20, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, f"Troca B: {LIMIAR_TROCA_B}+ | Volta A: <={LIMIAR_VOLTA_A}", 
                           (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            # Codificar frame para JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            self.frame_atual = buffer.tobytes()
            contador_frames += 1
            
            time.sleep(0.03)  # Limitar taxa de frames
    
    def get_frame(self):
        if self.frame_atual is None:
            # Frame vazio se ainda não houver frame
            blank = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(blank, "Aguardando camera...", (50, 240),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            ret, buffer = cv2.imencode('.jpg', blank)
            return buffer.tobytes()
        return self.frame_atual
    
    def cleanup(self):
        self.running = False
        if self.cap:
            self.cap.release()
        if self.arduino:
            self.arduino.close()

# Inicializar controlador
controller = SemaforoController()
controller.init_arduino()
controller.init_camera()

# Iniciar thread de processamento
processing_thread = threading.Thread(target=controller.process_frame)
processing_thread.daemon = True
processing_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            frame = controller.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            time.sleep(0.03)
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    return jsonify({
        'semaforo': controller.semaforo_atual,
        'carros': controller.carros_detectados,
        'limiar_troca_b': LIMIAR_TROCA_B,
        'limiar_volta_a': LIMIAR_VOLTA_A,
        'arduino_conectado': controller.arduino is not None
    })

@app.route('/set_limiar/<string:tipo>/<int:valor>')
def set_limiar(tipo, valor):
    global LIMIAR_TROCA_B, LIMIAR_VOLTA_A
    if tipo == 'troca_b':
        LIMIAR_TROCA_B = valor
    elif tipo == 'volta_a':
        LIMIAR_VOLTA_A = valor
    return jsonify({'success': True})

@app.route('/set_semaforo/<string:sinal>')
def set_semaforo(sinal):
    if sinal in ['A', 'B']:
        controller.semaforo_atual = sinal
        if controller.arduino:
            controller.arduino.write(sinal.encode())
        controller.ultimo_comando_enviado = sinal
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/shutdown')
def shutdown():
    controller.cleanup()
    return "Sistema encerrado"

if __name__ == '__main__':
    import numpy as np
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)