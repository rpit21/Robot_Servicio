"""Deteccion de Colores, tracking y comunicacion serial"""

import sys
import cv2   #libreria de Open CV V4.8.0
import numpy as np
import serial

#Funcion para dibujar los contornos, punto central y coordenadas de la deteccion, retornando una lista con los datos de la marca(x,y,area)
def dibujar (mask,color):

    global frame

    # Obtener dimensiones del fotograma
    height, width, _ = frame.shape

    # Calcular coordenadas para el punto en el central de referencia
    center_x = width // 2
    center_y = (height // 2 )-150 # se le resta 150 para poder poner el punto de referencia mas arriba del centro (borrar los 150 estaria en el centro el punto)
    
    # Dibujar un punto en el centro de referencia del fotograma
    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

    contornos=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] # identificar todos los contornos existentes en la mascara de color

    contornos= sorted(contornos, key=cv2.contourArea,reverse=True)[:1] #Ordenamos los contornos de mayor a menor a menor, y escogemos el mayor de ellos

    for c in contornos:  # se itera cada uno de los elementos del contorno encontrado 
        area=cv2.contourArea(c)  # se obtiene el area de cada uno de los contornos
        if area>=50:    # se filtran los contornos para quedarnos con aquellos que tienen un area mayor de 50 reduciendo el ruido

            #Se obtienen las coordenadas x,y del centro de la figura (contorno) reconocido
            M=cv2.moments(c)  
            if M["m00"] == 0 : M["m00"]=1
            x=int(M["m10"]/M["m00"])
            y=int(M["m01"]/M["m00"])

            nuevoContorno=cv2.convexHull(c) # genero un nuevo contorno mas suavizado 

            #Se genera un circulo en el punto medio de la figura (marca), y se incluye un texto con las coordenadas en el frame (imagen original)
            cv2.circle(frame, (x,y), 7, (0,0,0), -1)
            cv2.putText(frame, '{},{}'.format(x,y),(x+10,y), cv2.FONT_ITALIC, 0.75, (0,0,0), 1, cv2.LINE_AA)
            cv2.drawContours(frame, [nuevoContorno], 0, color, 3) # coloco el nuevo contorno en el frame (imagen original)

            #Encuentro la posicion relativa de la marca con respecto al punto de referencia 
            x_rel=x-center_x 
            y_rel=y-center_y

            DatosMarca=[x_rel,y_rel,area] #lista con datos (x relativo,y relativo ,area) de la marca
            #DatosMarca=[x,y,area] #lista con datos (x,y,area) de la marca
            #print(DatosMarca) # se imprime el area por consola

            return DatosMarca #Retorno de una lista con los datos cada vez que se ejecute la funcion
        
#Funcion para transforma una lista a un string incluyendo /n y enviarlo por comunicacion serial
def envioSerialDatos(listaDatosMarca: list):

    #Evaluamos la obtencion de datos de 'DatosMask' en caso que este vacio (NONE) se llena la lista con Valores que corresponderan que no hay marcas 
    if listaDatosMarca==None:
        #print("No hay marcas")
        listaDatosMarca=['N','H','M'] #Lista llenada con valores que representaran que no hay marcas

    # Convertir la lista en una cadena separada por comas
    cadena_enviar = ','.join(map(str, listaDatosMarca))

    # Agregar un salto de línea al final de la cadena
    cadena_enviar += '\n'
            
    # Enviar la cadena a través de la comunicación serial al arduino
    ArduinoPort.write(cadena_enviar.encode('utf-8'))

    print(cadena_enviar) # imprimir la cadena enviada por serial

#Funcion para lectura de datos serial pasando como parametro el puerto a leer
def lecturaSerial(puerto: serial):
    # Leer la línea recibida a través de la comunicación serial
    linea_recibida = puerto.readline().decode('utf-8').strip()

    # Imprimir la línea recibida
    print("Dato recibido:", linea_recibida)

    return linea_recibida

#Funcion para capturar el video de la camara, transformar HSV, y buscar cada una de las mascaras de acuerdo al color pasado en parametro
def Marca (colormarca):

    global frame

    while(cap.isOpened()):    # Hacemos un bucle acorde a cuando la camara este habilitada
        ret,frame=cap.read()  # Leemos la camara en donde: 'ret' es boolenado que indica la obtencion de imagen - 'frame' guarda la imagen obtenida
        
        if ret==True:   # Si una imagen (ret) es obtenida (true) 
             
            frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #Transformar el espacio de color BGR a HSV

            # Sentencia IF para la generacion de mascaras acorde al color, dado el parametro de la funcion "colormarca"
            if colormarca=='r':

                # Indicar que se busquen en la imagen HSV los rangos de color rojo y guardarlo en una mascara "Mask"
                MaskRed1=cv2.inRange(frameHSV,rojoBajo1,rojoAlto1)
                MaskRed2=cv2.inRange(frameHSV,rojoBajo2,rojoAlto2)
                Mask= cv2.add(MaskRed1,MaskRed2)

                ContornoColor=(0,0,255) # Asignar el color del contorno que se ira a mostrar en pantalla
                
            elif colormarca=='b':
                # Indicar que se busquen en la imagen HSV los rangos de color azul y guardarlo en una mascara "Mask"
                Mask=cv2.inRange(frameHSV,azulBajo,azulAlto)

                ContornoColor=(255,0,0) # Asignar el color del contorno que se ira a mostrar en pantalla

            elif colormarca=='g':
                # Indicar que se busquen en la imagen HSV los rangos de color verde y guardarlo en una mascara "Mask"
                Mask=cv2.inRange(frameHSV,VerdeBajo,VerdeAlto)

                ContornoColor=(0,255,0) # Asignar el color del contorno que se ira a mo1strar en pantalla

            Mask=cv2.erode(Mask, None, iterations=1) # Elimina el ruido blanco de la mascara
            Mask=cv2.dilate(Mask, None, iterations=1) # Se incrementa el area del objeto 
            
            DatosMask=dibujar(Mask,ContornoColor) #Dibuja el contorno y centros en el frame (imagen original) a patir de los parametros "Mask" y "ContornoColor", y retorna una lista con datos (x,y,area)

            cv2.imshow('Marca', frame)  # Se genera una ventana de nombre 'Marca' y muestra la imagen guardada y modificada 'frame'

            envioSerialDatos(DatosMask) # Llama funcion para enviar la lista 'DatosMask'  por serial al arduino
            
            #Condicion que espera para presionar la tecla 'a' para detener todo el bucle y seleccionar otra opcion 
            if cv2.waitKey(1) & 0xFF == ord('a'):  
                break

            #Condicion que espera para que el area de la marca sea mayor a 70000 para detener todo el bucle y determinar que se llego, para volver a seleccionar la marca a seguir
            if not DatosMask==None:
                if DatosMask[2]>=70000.0:
                    print("Fin del tracking")
                    envioSerialDatos([0,0,0]) # envio de lista de finalizacion 0,0,0
                    break

    cv2.destroyAllWindows() # Se cierran todas las ventanas abiertas al acabar el bucle


#Variable que contendra un objeto direccionado a la camara
cap=cv2.VideoCapture(0) # El 0 representa la camara incluida con una laptop, es necesario ir aumentando secuancialmente el numero hasta encontrar la camara adjunta
#cap=cv2.VideoCapture('/dev/video0', cv2.CAP_V4L2)  # En linux se debe escribir "/dev/video0" incluyendo comillas

# Inicializar la comunicación serial (ajusta el nombre del puerto y la velocidad)
ArduinoPort = serial.Serial('COM4', 9600)
#ArduinoPort = serial.Serial('/dev/ttyACM0', 9600) # En linux se debe escribir '/dev/ttyACM0' designando el puerto USB Arduino
#ArduinoPort = serial.Serial('/dev/ttyTHS1', 9600) # En linux se debe escribir '/dev/ttyTHS1' puerto UART1 o /dev/ttyS0' UART2 de la Jetson

# Variable global de la imagen obtenida por la camara que sera procesada en todo el codigo 
frame=None  

#Determinar los rangos de color en HSV (High Sature Value)
rojoBajo1=np.array([0,100,20],np.uint8) # rangos rojos  
rojoAlto1=np.array([10,255,255],np.uint8)

rojoBajo2=np.array([175,100,20],np.uint8)
rojoAlto2=np.array([179,255,255],np.uint8)

azulBajo=np.array([90,100,20],np.uint8)  # rangos azul
azulAlto=np.array([125,255,255],np.uint8)

VerdeBajo=np.array([50,100,20],np.uint8)  # rangos verde
VerdeAlto=np.array([70,255,255],np.uint8)




while True:    # Hacemos un bucle general (main loop)

 
    #Ingreso de consola para seleccionar la marca a buscar 
    mselect = int(input("Por favor, ingresa un número de marca: "))
    #mselect= lecturaSerial(puertoTablet) # lectura serial

    #Condicion IF para llamar a la funcion 'Marca' con parametro distinto e iniciar el reconocimiento de una marca en especifico
    if mselect==1:
        Marca('r') # Se llama la funcion marca con el parametro 'r'
    elif mselect==2:
        Marca('b')  # Se llama la funcion marca con el parametro 'b'
    elif mselect==3:
        Marca('g')  # Se llama la funcion marca con el parametro 'g'
    else:
        break

cap.release()  #Se cierra la comunicacion con la camara
ArduinoPort.close() # Se cierra el puerto de comunicacion serial
sys.exit() # Se cierra sesion de python

        