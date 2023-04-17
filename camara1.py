import cv2

# Define the key event listener
def key_event_listener(event):
    # Check if the pressed key is the 's' key (for save)
    if event == ord('s'):
        # Take a picture with the camera
        frame = cap.read()
        # Save the picture to disk
        cv2.imwrite('picture.png', frame)

# Initialize the camera capture object
cap = cv2.VideoCapture(0)

# Setup the window and key event listener
cv2.namedWindow("Camera Feed")
cv2.setMouseCallback("Camera Feed", key_event_listener)

# Start the main loop
while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    # Show the frame in the window
    cv2.imshow("Camera Feed", frame)
    # Wait for a key event
    key = cv2.waitKey(1) & 0xFF
    # If the 'q' key is pressed, quit the loop
    if key == ord('q'):
        break

# Release the resources
cap.release()
cv2.destroyAllWindows()
