from flask import Flask, render_template, Response
import cv2
import time
import numpy as np

app = Flask(__name__)

def iniciar_camera():
    """Tenta diferentes métodos para Windows"""
    
    # Método 1: DirectShow (recomendado para Windows)
    print("Tentando DirectShow...")
    for i in range(3):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            # Testa se realmente consegue ler um frame
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"✅ Câmera {i} funcionando com DirectShow!")
                return cap
            else:
                cap.release()
    
    # Método 2: Método padrão
    print("Tentando método padrão...")
    for i in range(3):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"✅ Câmera {i} funcionando com método padrão!")
                return cap
            else:
                cap.release()
    
    return None

# Inicializa a câmera
cap = iniciar_camera()

# Configurações da câmera se foi encontrada
if cap is not None:
    # Ajusta resolução para melhor performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    print("✅ Sistema pronto! Acesse http://localhost:5000")
else:
    print("❌ Nenhuma câmera encontrada!")
    print("\nSoluções:")
    print("1. Verifique se a câmera está conectada")
    print("2. Feche programas que usam a câmera (Zoom, Teams, Chrome)")
    print("3. Execute como administrador")
    print("4. Verifique as permissões de privacidade da câmera no Windows")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def generate():
        global cap
        
        # Se não tem câmera, mostra mensagem de erro
        if cap is None:
            while True:
                # Cria frame preto com mensagem
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(frame, "Camera nao encontrada", (150, 200), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.putText(frame, "Verifique a conexao da camera", (120, 250), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.putText(frame, "Feche outros programas que usam a camera", (80, 300), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                ret, buffer = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n\r\n')
                time.sleep(0.1)
        
        # Se tem câmera, faz streaming
        while True:
            if cap is None or not cap.isOpened():
                break
                
            success, frame = cap.read()
            if not success or frame is None:
                print("Erro ao ler frame, tentando reiniciar...")
                time.sleep(0.1)
                continue
            
            # Redimensiona para tamanho menor (opcional)
            # frame = cv2.resize(frame, (640, 480))
            
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
            time.sleep(0.03)  # ~30 fps
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚦 SEMÁFORO INTELIGENTE")
    print("="*50)
    print("\n🌐 Acesse no navegador: http://localhost:5000")
    print("🛑 Pressione Ctrl+C para parar\n")
    
    # Executa com debug=True para ver erros
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)