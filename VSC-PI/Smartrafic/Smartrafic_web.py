from flask import Flask, render_template, Response
import cv2
import time

app = Flask(__name__)

# Inicializar câmera
cap = cv2.VideoCapture(0)  # Tente 0, 1 ou 2 se não funcionar

if not cap.isOpened():
    print("Erro: Não foi possível abrir a câmera")
    cap = cv2.VideoCapture(1)  # Tenta segunda câmera

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            success, frame = cap.read()
            if not success:
                break
            else:
                # Codifica o frame como JPEG
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            time.sleep(0.03)  # 30 fps
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("\n🌐 Servidor rodando em: http://localhost:5000")
    print("🛑 Pressione Ctrl+C para parar\n")
    app.run(host='0.0.0.0', port=5000, debug=True)