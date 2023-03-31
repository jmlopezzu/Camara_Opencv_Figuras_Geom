import cv2, time
#1. Crear objeto
video=cv2.VideoCapture(0)
a=0
while True:
    a=a+1
#3. Crear un objeto frame
    check, frame =video.read()
    print(check)
    print(frame) #representar la imagen

#6. para convertir a gris
    gray =cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#4. mostrar el frame
    cv2.imshow('GAIA', gray)

#5. par precionar cualquier tecla
#cv2.waitKey (0)

#7. 
    key =cv2.waitKey(0)

    #if key ==ord('q'):
    #   break

    print(a)

#2. Apagar la camara
    video.release()
#8. Destruir todas las ventanas
    
    cv2.destroyAllWindows

