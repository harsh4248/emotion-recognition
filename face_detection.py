import cv2
from emotion_recogintion import preprocess_image

    




# Create a video capture object
cap = cv2.VideoCapture(0)

# Loop until the user presses the Esc key
while True:

    # Capture a frame from the webcam
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    frame, emotion = preprocess_image(frame)

    # Display the frame
    cv2.imshow('frame', frame)

    # Wait for a key press
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the video capture object
cap.release()

# Close all windows
cv2.destroyAllWindows()