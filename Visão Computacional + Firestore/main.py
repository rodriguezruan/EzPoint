import serial
import tkinter
from tkinter import ttk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from ultralytics import YOLO
import cv2
import math 
import time

cmd = None
cargo = None

# Inicialize a conexão com o Firestore
cred = credentials.Certificate('ezpoint-cd326-firebase-adminsdk-6yfjv-7e14cc16f2.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

# Abra a porta serial. Certifique-se de que a porta e a velocidade (baudrate) estão corretas.
porta_serial = serial.Serial('COM5', 115200)  # Substitua 'COMx' pela porta serial do seu Arduino

# Variável para armazenar os dados decodificados
dados_decodificados = ""

# Crie um dicionário que mapeia os cargos para os índices de classe permitidos
cargos_permitidos = {
    "Supervisor": [0],  # Por exemplo, '0' representa a classe 'capacete'
    "Produção Química": [3, 4],  # '3' representa 'mascara' e '4' representa 'oculos'
    "Produção": [0, 2],  # '0' é 'capacete' e '2' é 'luvas'
    "Soldador": [0, 1],  # '0' é 'capacete' e '1' é 'colete'
}

# Loop para ler e processar dados da porta serial

# Os dados decodificados estão agora armazenados na variável 'dados_decodificados'
#print(f'Dados decodificados armazenados: {dados_decodificados}')

# restante do seu código, incluindo o loop de processamento de imagem da webcam
# ...

#start webcam--------------------------
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
#--------------------------------------

# model
#model = YOLO("epiconfig.pt")
model = YOLO("datsetpropriov2.pt")

# object classes
#classNames = ["Excavator", "Gloves", "Hardhat", "Ladder", "Mask", "NO-Hardhat", "NO-Mask", "NO-Safety Vest", "Person", "SUV", "Safety Cone", "Safety Vest", "bus", "dump truck", "fire hydrant", "machinery", "mini-van", "sedan", "semi", "trailer", "truck and trailer", "truck", "van", "vehicle", "wheel loader"]
classNames = ['capacete', 'colete', 'luvas', 'mascara', 'oculos']

#DEFINIÇÃO DE FUNÇÕES--------------------------------------

def enviar_comando_liberado():
    porta_serial.write('P'.encode())
    print("Mandando P para o Arduino")
    porta_serial.flush()
    time.sleep(5)
        
def enviar_comando_bloqueado():
    porta_serial.write('B'.encode())
    print("Mandando B para o Arduino")
    porta_serial.flush()
    time.sleep(5)

def enviar_comando_random():
    porta_serial.write('N'.encode())
    print("Mandando N para o Arduino")
    porta_serial.flush()
    time.sleep(5)

#DEFINIÇÃO DE FUNÇÕES--------------------------------------

#inicio do processamento de imagem
# Variável para armazenar os dados decodificados
dados_decodificados = ""

# Flag para controlar o processamento de imagem
processar_imagem = False

# Loop para ler e processar dados da porta serial
while True:
    try:
        # Leia os bytes da porta serial até receber um caractere de nova linha ('\n')
        linha = porta_serial.readline()
        
        # Decodifique os bytes para uma string UTF-8 (ignorando erros)
        try:
            linha_decodificada = linha.decode('utf-8', errors='ignore').strip()
            print(f'Dados decodificados: {linha_decodificada}')
            
            # Atualize a variável com os dados decodificados
            dados_decodificados = linha_decodificada
            
        except UnicodeDecodeError:
            print('Não foi possível decodificar todos os caracteres para UTF-8.')
        
        # Verifique se o valor do RFID lido existe no Firestore
        doc_ref = db.collection('Funcionarios').document(dados_decodificados).get()

        if doc_ref.exists:
            data = doc_ref.to_dict()
            cargo = data.get('cargo')
            print("Cargo:", cargo)
            
            # Ativar o processamento de imagem quando o cargo for encontrado
            processar_imagem = True
            break  # Saia do loop de verificação de cargo
            
        else:
            print("Documento não encontrado.")
            
    except KeyboardInterrupt:
        print("Programa encerrado pelo usuário.")
        break
    
    except Exception as e:
        print(f"Erro ao ler da porta serial: {str(e)}")

# Fechar a porta serial // Fechar a porta serial somente quando não for mais necessária
#porta_serial.close()


itens_detectados =[]

while processar_imagem:
    success, img = cap.read()
    results = model(img, stream=True)

    # Variável para verificar se uma pessoa foi detectada com confiança suficiente
    person_detected = False

    # coordinates
    #start webcam--------------------------
    #cap = cv2.VideoCapture(0)
    #cap.set(3, 640)
    #cap.set(4, 480)
    #--------------------------------------

    detected_helmet = False
    detected_vest = False
    detected_mask = False
    detected_googles = False
    detected_gloves = False

    for r in results:
        boxes = r.boxes

        itens_detectados = []

        if cargo in cargos_permitidos:
                indices_permitidos = cargos_permitidos[cargo]
                if indices_permitidos == sorted(itens_detectados): #sorted vai deixar a lista de classes encontradas em ordem
                    print("Usuario liberado!!!")
                    person_detected = True
                    cmd = "liberado"
                else:
                    print("Usuário Bloqueado")
                    cmd = "bloqueado"
        else: 
            print("Cargo não reconhecido.")
            cmd = "bloqueado"
            itens_detectados.append(cls)

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])
            itens_detectados.append(cls)

            current_class = classNames[cls]

            if current_class == 'capacete' and confidence >= 0.60:
                detected_helmet = True
            elif current_class == 'colete' and confidence >= 0.60:
                detected_vest = True
            elif current_class == 'oculos' and confidence >= 0.60:
                detected_googles = True
            elif current_class == 'luvas' and confidence >= 0.60:
                detected_gloves = True
            elif current_class == 'mascara' and confidence >= 0.60:
                detected_mask = True

            if cargo == "Soldador":
                if detected_googles and detected_gloves:
                    print("Usuário liberado!!!")
                    enviar_comando_liberado()
                    processar_imagem = False
                    break
            elif cargo == "Supervisor":
                if detected_helmet and detected_vest:
                    print("Usuário Liberado")
                    enviar_comando_liberado()
                    processar_imagem = False
                    break
            elif cargo == "Produção Química":
                if detected_mask and detected_gloves:
                    print("Usuário Liberado")
                    enviar_comando_liberado()
                    processar_imagem = False
                    break
            elif cargo == "Produção":
                if detected_helmet and detected_gloves and detected_vest:
                    print("Usuário Liberado")
                    enviar_comando_liberado()
                    processar_imagem = False
                    break


            # Se a classe for 'person' e a confiança for maior que 0.60, imprima "Usuario liberado!!!"

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
       processar_imagem = False

    # Verifique se uma pessoa foi detectada com confiança e tome alguma ação
    if person_detected:
        # Faça algo aqui, se necessário
        enviar_comando_liberado()
        pass

    #if cmd == "liberado":
        #enviar_comando_liberado()
    #elif cmd == "bloqueado":
        #enviar_comando_bloqueado()
    #else:
        #enviar_comando_random()

    # Aguarde a resposta do Arduino e imprima-a
    #response = porta_serial.readline().decode().strip()
    #print("Resposta do Arduino:", response, '\n')

cap.release()
cv2.destroyAllWindows()

#Fechar a porta serial quando nao for mais necessaria
if porta_serial.is_open:
    porta_serial.close()
