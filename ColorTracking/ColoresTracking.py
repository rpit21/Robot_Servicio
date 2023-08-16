"""Deteccion de Colores y Tracking"""

import cv2   #libreria de Open Cv
import numpy as np

def dibujar (mask,color):
    contornos,h=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # identificar todos los contornos existentes en la mascara de color

    for c in contornos:  # se itera cada uno de los contornos encontrados 
        area=cv2.contourArea(c)  # se obtiene el area de cada uno de los contornos
        if area>=1500:    # se filtran los contornos para quedarnos con aquellos que tienen un area mayor de 1500 reduciendo el ruido

            #Se obtienen las coordenadas x,y del centro de la figura (contorno)
            M=cv2.moments(c)  
            if M["m00"] == 0 : M["m00"]=1
            x=int(M["m10"]/M["m00"])
            y=int(M["m01"]/M["m00"])

            nuevoContorno=cv2.convexHull(c) # genero un nuevo contorno mas suavizado 

            #Se genera un circulo en el punto medio de la figura, y se incluye un texto con las coordenadas en el frame (imagen original)
            cv2.circle(frame, (x,y), 7, (0,0,0), -1)
            cv2.putText(frame, '{},{}'.format(x,y),(x+10,y), cv2.FONT_ITALIC, 0.75, (0,0,0), 1, cv2.LINE_AA)
            cv2.drawContours(frame, [nuevoContorno], 0, color, 3) # coloco el nuevo contorno en el frame (imagen original)
            print(area) # se imprime el area por consola


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

while(cap.isOpened()):    # Hacemos un bucle acorde a cuando la camara este habilitada
    ret,frame=cap.read()  # Leemos la camara en donde: 'ret' es boolenado que indica la obtencion de imagen - 'frame' guarda la imagen obtenida

    if ret==True:   # Si una imagen (ret) es obtenida (true) 

        frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #Transformar el espacio de color BGR a HSV

        # Indicar que se busquen en la imagen los rangos de color
        MaskRed1=cv2.inRange(frameHSV,rojoBajo1,rojoAlto1)
        MaskRed2=cv2.inRange(frameHSV,rojoBajo2,rojoAlto2)
        MaskRed=cv2.add(MaskRed1,MaskRed2)   

        MaskBlue=cv2.inRange(frameHSV,azulBajo,azulAlto)

        MaskGreen=cv2.inRange(frameHSV,VerdeBajo,VerdeAlto)

        #Dibujar el contorno e identificar coordenadas por medio de la funcion dibujar

        dibujar(MaskRed, (0,0,255))
        dibujar(MaskBlue,(255,0,0))
        dibujar(MaskGreen,(0,255,0))

        cv2.imshow('Video', frame)   # Se genera una ventana de nombre 'Video' y muestra la imagen guardada 'frame'

        if cv2.waitKey(1) & 0xFF == ord('s'):  #Condicion que espera para presionar la tecla 's' para detener todo el programa
            break

cap.release()  #Se cierra la comunicacion con la camara
cv2.destroyAllWindows() # Se cierran todas las ventanas abiertas