# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)

# brew install tesseract

# pip install pytesseract

import cv2
import os
import numpy as np
import pytesseract

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
            
            #
            if area >20000 and area<21000:
                # Crop the image using the rectangle coordinates
                cropped_img = frame[y:y+h, x:x+w]
                
                # Preprocess the image to enhance OCR results
                gray_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
                thresh = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                dilate = cv2.dilate(thresh, kernel, iterations=1)

                # Apply OCR on the preprocessed image
                ocr_text = pytesseract.image_to_string(dilate, lang='eng', config='--psm 11')

                # Display the OCR text on the original frame
                cv2.putText(frame, ocr_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Guarda la foto en la carpeta "fotos"
                cv2.imwrite('fotos/imagen.png', cropped_img) 
                                                    
            # Dibujar un rectángulo alrededor del contorno
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Muestra el fotograma en una ventana
        cv2.imshow('Camara', frame)

        # Espera a que se presione una tecla
        key = cv2.waitKey(1)

        # Si se presiona la tecla "ESC", sale del bucle
        if key == 27:
            break

    # Libera la cámara y cierra la ventana
    cap.release()
    cv2.destroyAllWindows()

tomar_foto_video()
