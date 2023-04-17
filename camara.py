import cv2

# Create an object to capture video from camera
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video capture!")

# Capture frame-by-frame
ret, frame = cap.read()

# If frame is read correctly, save it
if ret:
    cv2.imwrite('picture.png', frame)

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
