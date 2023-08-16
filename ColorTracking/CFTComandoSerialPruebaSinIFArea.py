"""Deteccion de Colores"""

import sys
import cv2   #libreria de Open Cv
import numpy as np
import serial

def dibujar (mask,color):

    global frame

    # Obtener dimensiones del fotograma
    height, width, _ = frame.shape

    # Calcular coordenadas para el punto en el central de referencia
    center_x = width // 2
    center_y = (height // 2 )-150 # se le resta 150 para poder poner el punto de referencia mas arriba del centro (borrar los 150 estaria en el centro el punto)

    # Dibujar un punto en el centro del fotograma
    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

    contornos=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] # identificar todos los contornos existentes en la mascara de color
    contornos= sorted(contornos, key=cv2.contourArea,reverse=True)[:1]

    for c in contornos:  # se itera cada uno de los contornos encontrados 
        area=cv2.contourArea(c)  # se obtiene el area de cada uno de los contornos
        
        xr,yr,w,h=cv2.boundingRect(c)
        cv2.rectangle(frame,(xr,yr),(xr+w,yr+h),color,2)

        #Se obtienen las coordenadas x,y del centro de la figura (contorno)
        M=cv2.moments(c)  
        if M["m00"] == 0 : M["m00"]=1
        x=int(M["m10"]/M["m00"])
        y=int(M["m01"]/M["m00"])

        #nuevoContorno=cv2.convexHull(c) # genero un nuevo contorno mas suavizado 

        #Se genera un circulo en el punto medio de la figura, y se incluye un texto con las coordenadas en el frame (imagen original)
        cv2.circle(frame, (x,y), 7, (0,0,0), -1)
        cv2.putText(frame, '{},{}'.format(x,y),(x+10,y), cv2.FONT_ITALIC, 0.75, (0,0,0), 1, cv2.LINE_AA)
        #cv2.drawContours(frame, [nuevoContorno], 0, color, 3) # coloco el nuevo contorno en el frame (imagen original)

        x_rel=x-center_x 
        y_rel=y-center_y
        
        #DatosMarca=[x,y,area] #lista de paramatros a enviar por serial (x relativo,y Relativo,area) de la marca
        DatosMarca=[x_rel,y_rel,area] #lista de paramatros a enviar por serial (x relativo,y Relativo,area) de la marca
        #print(DatosMarca) # se imprime el los parametros por consola

        return DatosMarca


def envioSerialDatos(listaDatosMarca: list):

    if listaDatosMarca==None:
        #print("No hay marcas")
        listaDatosMarca=['N','H','M']


    # Convertir la lista en una cadena separada por comas
    cadena_enviar = ','.join(map(str, listaDatosMarca))

    # Agregar un salto de línea al final de la cadena
    cadena_enviar += '\n'
            
    # Enviar la cadena a través de la comunicación serial
    puerto.write(cadena_enviar.encode('utf-8'))

    print(cadena_enviar)



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

            Mask=cv2.erode(Mask, None, iterations=2) # Elimina el ruido blanco de la mascara (para mayor erode aumentar 'iterations')
            Mask=cv2.dilate(Mask, None, iterations=1) # Se incrementa el area del objeto  (para mayor mask aumentar 'iterations')
            
            DatosMask=dibujar(Mask,ContornoColor) #Dibuja el contorno y centros en el frame (imagen original) a patir de los parametros "Mask" y "ContornoColor", y retorna una lista con datos (x,y,area)

            cv2.imshow('Marca', frame)  # Se genera una ventana de nombre 'Marca' y muestra la imagen guardada y modificada 'frame'

            envioSerialDatos(DatosMask)
                

            #Condicion que espera para presionar la tecla 'a' para detener todo el bucle y seleccionar otra opcion 
            if cv2.waitKey(1) & 0xFF == ord('a'):  
                break

    cv2.destroyAllWindows() # Se cierran todas las ventanas abiertas


#Variable que contendra un objeto direccionado a la camara
cap=cv2.VideoCapture(0) # El 0 representa la camara incluida con una laptop, es necesario ir aumentando secuancialmente el numero hasta encontrar la camara adjunta
#cap=cv2.VideoCapture('/dev/video0', cv2.CAP_V4L2)  # En linux se debe escribir "/dev/video0" incluyendo comillas

#Determinar los rangos de color en HSV (High Sature Value)
rojoBajo1=np.array([0,100,20],np.uint8) # rangos rojos
rojoAlto1=np.array([10,255,255],np.uint8)

rojoBajo2=np.array([175,100,20],np.uint8)
rojoAlto2=np.array([179,255,255],np.uint8)

azulBajo=np.array([90,100,20],np.uint8)  # rangos azul
azulAlto=np.array([125,255,255],np.uint8)

VerdeBajo=np.array([50,100,20],np.uint8)  # rangos verde
VerdeAlto=np.array([70,255,255],np.uint8)

frame=None # Variable global de la imagen obtenida por la camara que sera procesada 

# Inicializar la comunicación serial (ajusta el nombre del puerto y la velocidad)
puerto = serial.Serial('COM4', 9600)


while True:    # Hacemos un bucle acorde a cuando la camara este habilitada

 
    #Seleccionar la marca a buscar 
    mselect = int(input("Por favor, ingresa un número de marca: "))

    if mselect==1:
        Marca('r') # Se llama la funcion marca con el parametro 'r'
    elif mselect==2:
        Marca('b')  # Se llama la funcion marca con el parametro 'b'
    elif mselect==3:
        Marca('g')  # Se llama la funcion marca con el parametro 'g'
    else:
        break
cap.release()  #Se cierra la comunicacion con la camara
sys.exit() # Se cierra sesion de python

        