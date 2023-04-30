import cv2
import os
import numpy as np

def tomar_foto_video():
    
    '''Esta función se encarga de comenzar una grabación en vivo, buscar un objeto amarillo(En este caso la placa), y tomar una foto cuando tenga un aréa mayor a 20000 y menor a 21000. La foto la guarda en la carpeta "fotos" '''
    
    
    # Crea un objeto de captura de video
    cap = cv2.VideoCapture(0)


    while True:
        # Lee un fotograma de la cámara
        ret, frame = cap.read()

        # Convertir la imagen a espacio de color HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Definir el rango de colores que deseas detectar en formato HSV
        # Aquí se define el rango de amarillo
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        # Aplicar la máscara para detectar solo los píxeles amarillos
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Encontrar los contornos en la imagen de la máscara
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Si se encontraron contornos
        if len(contours) > 0:
            # Encontrar el contorno más grande (el contorno de la parte amarilla)
            max_contour = max(contours, key=cv2.contourArea)

            # Encontrar el rectángulo que rodea el contorno
            x, y, w, h = cv2.boundingRect(max_contour)
            
            #Calcular aréa
            area = w * h
            print(area)
            
            #
            if area >20000 and area<21000:
                # Guarda la foto en la carpeta "fotos"
                cv2.imwrite('fotos/imagen.png', frame)
            
            
            # Dibujar un rectángulo alrededor del contorno
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Muestra el fotograma en una ventana
        cv2.imshow('Camara', frame)

        # Espera a que se presione una tecla
        key = cv2.waitKey(1)

        # Si se presiona la tecla "q", toma una foto
        #if key == ord('q'):
            # Guarda la foto en la carpeta "fotos"
        #    cv2.imwrite('fotos/imagen.png', frame)

        # Si se presiona la tecla "ESC", sale del bucle
        if key == 27:
            break

    # Libera la cámara y cierra la ventana
    cap.release()
    cv2.destroyAllWindows()


tomar_foto_video()




