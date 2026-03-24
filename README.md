# project-team

Antes de rodar, baixar o Opencv e o YOLO

pip install opencv-python ultralytics

entrar na pasta Detector-VSC

Antes de rodar vereficar se é webcam ou camera
Se for camera ir no codigo "cap = cv2.VideoCapture(1)" e vereficar se ta com 1
Se for webcam mudar para "cap = cv2.VideoCapture(0)" 

e rodar o arquivo com:

//Visao computacional filtrada para apenas carros e pessoas
python .\Contador_carros.py

//Visao computacional com o YOLO mais potente
python .\VSC-meio.py

//Visao computacional com identificaçao de todos os objetos
python .\Objetos.py

//Visao computacional com Reconhecimento facial 
python .\main.py
