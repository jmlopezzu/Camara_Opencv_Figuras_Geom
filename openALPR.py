import openalpr
import cv2

# Configurar la ubicación de los archivos de reconocimiento


# Crear una instancia de OpenALPR
alpr = openalpr.Alpr("us", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data","co")

# Configurar la cámara
cap = cv2.VideoCapture(0)

# Procesar el video en vivo
while True:
    # Leer cada fotograma del video
    ret, frame = cap.read()

    # Utilizar OpenALPR para reconocer matrículas
    results = alpr.recognize_ndarray(frame)

    # Si se detecta una matrícula, guardar una foto
    if results['results']:
        plate = results['results'][0]['plate']
        print(plate)
        filename = plate + '.jpg'
        cv2.imwrite(filename, frame)

    # Mostrar el fotograma en una ventana
    cv2.imshow('frame', frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()