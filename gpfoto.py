import cv2
import os
import numpy as np
import pytesseract
import openalpr

def detectPlate(img):
    '''Esta función se encarga de detectar una placa en una imagen y devolver la placa detectada'''
    
    # Convertir la imagen a espacio de color HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

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

        # Calcular área
        area = w * h

        #
        if area >20000 and area<25000:
            # Crop the image using the rectangle coordinates
            cropped_img = img[y:y+h, x:x+w]

            # Add a delay to give more time for the yellow rectangle to be recognized
            cv2.waitKey(1000)

            # Preprocess the image to enhance OCR results
            gray_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            dilate = cv2.dilate(thresh, kernel, iterations=1)

            # Apply OCR on the preprocessed image
            ocr_text = pytesseract.image_to_string(dilate, lang='eng', config='--psm 11').strip()

            # Initialize the OpenALPR recognizer
            openalpr_path = '/usr/share/openalpr/config/'
            recognizer = openalpr.Alpr('us', openalpr_path, 'runtime_data')

            # Get the license plate number from the image
            result = recognizer.recognize_ndarray(cropped_img)

            # Write the OCR text and license plate number on top of the green rectangle
            if len(ocr_text) > 0:
                cv2.putText(img, f"{ocr_text} | {result['results'][0]['plate']}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                cv2.putText(img, result['results'][0]['plate'], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Destroy the OpenALPR recognizer object
            recognizer.unload()

        # Draw a rectangle around the contour
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return img

def detectVideo():
    '''Esta función se encarga de comenzar una grabación en vivo y buscar un objeto amarillo (En este caso la placa)'''

    # Crea un objeto de captura de video
    cap = cv2.VideoCapture(0)

    while True:
        # Lee un fotograma de la cámara
        ret, frame = cap.read()

        # Detect plate in frame
        frame_with_plate = detectPlate(frame)

        # Muestra el fotograma en una ventana
        cv2.imshow('Camara', frame_with_plate)

        # Espera a que se presione una tecla
        key = cv2.waitKey(1)

        # Si se presiona la tecla "ESC", sale del bucle
        if key == 27:
            break

    # Libera la cámara y cierra la ventana
    cap.release()
    cv2.destroyAllWindows()

detectVideo()
