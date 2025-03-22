import cv2

image = cv2.imread("apple.jpg", 0)  # Convert to grayscale

edges = cv2.Canny(image, 100, 200)  # Canny edge detection

cv2.imshow("Edges", edges)
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()