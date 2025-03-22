import cv2
import numpy as np

# Create a blank image
canvas = np.zeros((500, 500, 3), dtype="uint8")

# Draw a rectangle
cv2.rectangle(canvas, (50, 50), (200, 200), (0, 255, 0), 3)

# Draw a circle
cv2.circle(canvas, (300, 300), 50, (255, 0, 0), -1)

# Draw a line
cv2.line(canvas, (100, 100), (400, 400), (0, 0, 255), 5)

cv2.imshow("Shapes", canvas)


# Wait for keypress and close
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()