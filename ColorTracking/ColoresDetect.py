"""Deteccion de Colores y modificacion de valores HSV"""

import cv2   #libreria de Open Cv V4.8.0
import numpy as np

#Funcion para determinar los pixeles que se tienen 
def pixeles():

    # Obtener la resolución de la imagen capturada
    #width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Obtener dimensiones del fotograma
    height, width, _ = frame.shape

    # Mostrar la resolución
    print(f"La resolución de la cámara es {width} x {height}")

# Función para ajustar los valores HSV
def ajustar_valores_hsv(valor):
    return cv2.getTrackbarPos(valor, 'Ajustes')

# Variable que contendra un objeto direccionado a la camara
cap=cv2.VideoCapture(0)


# Crear una ventana con sliders para ajustar los valores HSV
cv2.namedWindow('Ajustes')
cv2.createTrackbar('Hue Min', 'Ajustes', 0, 255, lambda x: None)
cv2.createTrackbar('Hue Max', 'Ajustes', 255, 255, lambda x: None)
cv2.createTrackbar('Sat Min', 'Ajustes', 0, 255, lambda x: None)
cv2.createTrackbar('Sat Max', 'Ajustes', 255, 255, lambda x: None)
cv2.createTrackbar('Val Min', 'Ajustes', 0, 255, lambda x: None)
cv2.createTrackbar('Val Max', 'Ajustes', 255, 255, lambda x: None)

#Determinar los rangos de color en HSV (High Sature Value)
#rojoBajo1=np.array([0,100,100],np.uint8) # rangos rojos
#rojoAlto1=np.array([5,255,255],np.uint8)

#rojoBajo2=np.array([175,100,100],np.uint8)
#rojoAlto2=np.array([179,255,255],np.uint8)

#azulBajo=np.array([90,100,20],np.uint8)  # rangos azul
#azulAlto=np.array([125,255,255],np.uint8)

#VerdeBajo=np.array([50,100,20],np.uint8)  # rangos verde
#VerdeAlto=np.array([70,255,255],np.uint8)

while(cap.isOpened()):    # Hacemos un bucle acorde a cuando la camara este habilitada
    ret,frame=cap.read()  # Leemos la camara en donde: 'ret' es boolenado que indica la obtencion de imagen - 'frame' guarda la imagen obtenida

    if ret==True:   # Si una imagen (ret) es obtenida (true) 

        blur=cv2.GaussianBlur(frame,(5,5),0)

        frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #Transformar el espacio de color BGR a HSV

        # Obtener los valores HSV ajustados desde los sliders
        hue_min = ajustar_valores_hsv('Hue Min')
        hue_max = ajustar_valores_hsv('Hue Max')
        sat_min = ajustar_valores_hsv('Sat Min')
        sat_max = ajustar_valores_hsv('Sat Max')
        val_min = ajustar_valores_hsv('Val Min')
        val_max = ajustar_valores_hsv('Val Max')

        # Definir el rango de color a detectar en HSV
        lower_bound = np.array([hue_min, sat_min, val_min])
        upper_bound = np.array([hue_max, sat_max, val_max])

        # Crear una máscara utilizando el rango de color definido
        mask = cv2.inRange(frameHSV, lower_bound, upper_bound)
        maskE=cv2.erode(mask, None, iterations=1) # Elimina el ruido blanco de la mascara
        maskD=cv2.dilate(maskE, None, iterations=1)

        # Aplicar la máscara al frame original
        resultado = cv2.bitwise_and(frame, frame, mask=mask)

        # Indicar que se busquen en la imagen los rangos de color y crear una mascara
        #MaskRed1=cv2.inRange(frameHSV,rojoBajo1,rojoAlto1)
        #MaskRed2=cv2.inRange(frameHSV,rojoBajo2,rojoAlto2)
        #MaskRed=cv2.add(MaskRed1,MaskRed2)   

        #MaskRedE=cv2.erode(MaskRed, None, iterations=1) # Elimina el ruido blanco de la mascara
        
        #MaskRedD=cv2.dilate(MaskRedE, None, iterations=1) # Se incrementa el area del objeto 


        #MaskBlue=cv2.inRange(frameHSV,azulBajo,azulAlto)

        #MaskGreen=cv2.inRange(frameHSV,VerdeBajo,VerdeAlto)


        # Obtener dimensiones del fotograma
        height, width, _ = frame.shape

        # Calcular coordenadas para el punto en el centro
        center_x = width // 2
        center_y = height // 2

        # Dibujar un punto en el centro del fotograma
        cv2.circle(frame, (center_x, center_y-150), 5, (0, 0, 255), -1)

        # Mostrar las coordenadas en el fotograma
        coordenadas_texto = f"Coordenadas: ({center_x}, {center_y})"
        cv2.putText(frame, coordenadas_texto, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        


        cv2.imshow('Video', frame)   # Se genera una ventana de nombre 'Video' y muestra la imagen guardada 'frame'
        cv2.imshow('Mascara', mask)
        cv2.imshow('MascaraErode', maskE)
        cv2.imshow('MascaraDilate', maskD)
        cv2.imshow('Resultado', resultado)
        #cv2.imshow('Blur', blur)
        

        if cv2.waitKey(1) & 0xFF == ord('s'):  #Condicion que espera para presionar la tecla 's' para detener todo el programa
            break

cap.release()  #Se cierra la comunicacion con la camara
cv2.destroyAllWindows() # Se cierran todas las ventanas abiertas