# SmarTraffic

Projeto de visão computacional para detecção de objetos utilizando OpenCV e YOLO.  
Inclui módulos para detecção geral de objetos, contagem de veículos e reconhecimento facial.

## Requisitos

Instale as dependências necessárias:

```bash
pip install opencv-python ultralytics
```

## Configuração
1. Acesse a pasta do projeto:

```bash
cd Detector-VSC
```

2. Configure a fonte de captura de vídeo:
- No código, localize a linha:
```bash
cap = cv2.VideoCapture(0)
```
- Para webcam, mantenha o valor ```0```.
- Para câmera externa ou IP, altere para ```1``` ou conforme o índice do dispositivo.

## Execução
Os scripts disponíveis e suas respectivas funções:

| Arquivo | Descrição | 
|----------|----------|
| Contador_carros.py  | Detecção filtrada para veículos e pessoas | 
| VSC-meio.py  | Execução do YOLO em sua configuração padrão. |
| Objetos.py | Detecção de todos os objetos suportados pelo modelo. |
| main.py | Reconhecimento facial. |

Exemplo de execução:
```bash
python Contador_carros.py
```
