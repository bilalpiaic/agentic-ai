import cv2
import numpy as np

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Define the color range for detection (e.g., Blue)
lower_color = np.array([100, 150, 0])  # Lower HSV boundary
upper_color = np.array([140, 255, 255])  # Upper HSV boundary

# Initialize canvas (it will be resized to match the frame size)
canvas = None  

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create mask to detect the specified color
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Find contours of the detected color
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize canvas after getting frame size
    if canvas is None:
        canvas = np.zeros_like(frame)  # Ensure same size & channels as frame

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 1000:  # Minimum area threshold
            x, y, w, h = cv2.boundingRect(largest_contour)
            center = (x + w // 2, y + h // 2)

            # Draw on canvas
            cv2.circle(canvas, center, 5, (255, 0, 0), -1)  # Blue dot

    # Merge canvas with frame
    blended = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)

    # Display the result
    cv2.imshow("Virtual Painter", blended)
    cv2.imshow("Mask", mask)  # Show the color mask

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
