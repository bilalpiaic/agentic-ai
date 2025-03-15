# **OpenCV: Computer Vision with Python**

## **Introduction**
OpenCV (Open Source Computer Vision Library) is an open-source computer vision and machine learning software library. It has over **2500 optimized algorithms** for real-time image and video processing.

### **Installation**
Install OpenCV using:
```bash
pip install opencv-python
pip install opencv-python-headless  # For server environments without GUI
```

### **Basic Imports**
```python
import cv2
import numpy as np
```

---

## **1. Reading and Displaying Images**
```python
import cv2

# Load an image
image = cv2.imread("sample.jpg")

# Display the image
cv2.imshow("Image", image)

# Wait for keypress and close
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### **Basic Image Operations**
- Resize: `cv2.resize(img, (width, height))`
- Convert to grayscale: `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`
- Save an image: `cv2.imwrite("output.jpg", img)`

---

## **2. Drawing Shapes on Images**
```python
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
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

### **2. Image Processing**
Convert an image to grayscale and manipulate pixel values.
```python
import cv2

img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
print(img.shape)  # Image shape
img[50:100, 50:100] = 255  # Modify pixels to white
cv2.imshow('Modified Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## **3. Video Capture with OpenCV**
```python
import cv2

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Webcam Feed", frame)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## **4. Edge Detection using Canny**
```python
import cv2

image = cv2.imread("sample.jpg", 0)  # Convert to grayscale

edges = cv2.Canny(image, 100, 200)  # Canny edge detection

cv2.imshow("Edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## **5. Face Detection using Haar Cascades**
```python
import cv2

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Load an image
image = cv2.imread("face.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(gray, 1.1, 4)

# Draw rectangles around faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 3)

cv2.imshow("Face Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## **6. Object Tracking using Color Detection**
```python
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color range (blue in this case)
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    cv2.imshow("Original", frame)
    cv2.imshow("Masked", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

Here are **three very interesting OpenCV projects** with code that will engage students and help them apply Computer Vision concepts in a fun and practical way.

---

## **1. Virtual Painter (Draw with Your Fingers in the Air)**
In this project, students will use **color detection** to draw on the screen using their fingers or a colored object (like a red pen cap).

### **Concepts Covered**
✅ Color detection  
✅ Contours and shape tracking  
✅ Drawing on a blank canvas  

### **Code**
```python
import cv2
import numpy as np

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Define the color range for detection (e.g., Blue)
lower_color = np.array([100, 150, 0])
upper_color = np.array([140, 255, 255])

# Create a blank canvas to draw on
canvas = np.zeros((480, 640, 3), dtype=np.uint8)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # Find contours of the detected color
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 1000:
            x, y, w, h = cv2.boundingRect(largest_contour)
            center = (x + w//2, y + h//2)
            
            # Draw on canvas
            cv2.circle(canvas, center, 5, (255, 0, 0), -1)

    # Merge canvas with frame
    frame = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)

    cv2.imshow("Virtual Painter", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```
### **How it Works?**
- Detects a **colored object** using HSV color detection.
- Tracks the largest object and **draws** on the screen using contours.
- The drawing persists until the user exits.

---

## **2. Real-Time Motion Detection System**
A security-style project that detects **motion** and highlights moving objects. This is useful for surveillance and security applications.

### **Concepts Covered**
✅ Background subtraction  
✅ Contour detection  
✅ Motion detection  

### **Code**
```python
import cv2

# Initialize webcam
cap = cv2.VideoCapture(0)

# Background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply background subtraction
    fgmask = fgbg.apply(frame)

    # Find contours of moving objects
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 1000:  # Ignore small movements
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Motion Detection", frame)
    cv2.imshow("Mask", fgmask)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```
### **How it Works?**
- Uses **background subtraction** to detect motion.
- Highlights **moving objects** with a green rectangle.
- Ignores small noises using `cv2.contourArea(contour) > 1000`.

---

## **3. AI Face Mask Detection**
A **COVID-era** project where students can **detect whether a person is wearing a mask** or not.

### **Concepts Covered**
✅ Haar cascades for face detection  
✅ Machine learning for mask classification  
✅ Real-time video processing  

### **Code**
```python
import cv2
import numpy as np
import tensorflow as tf

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Load pre-trained mask detection model (TensorFlow/Keras)
model = tf.keras.models.load_model("mask_detector_model.h5")

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        face = frame[y:y + h, x:x + w]
        face_resized = cv2.resize(face, (100, 100)) / 255.0
        face_resized = np.expand_dims(face_resized, axis=0)

        # Predict mask/no mask
        prediction = model.predict(face_resized)[0][0]
        label = "Mask" if prediction > 0.5 else "No Mask"
        color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

        # Draw rectangle and label
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Face Mask Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```
### **How it Works?**
- Detects faces using **Haar cascades**.
- Loads a **trained deep learning model** (`mask_detector_model.h5`) to classify **Mask** vs. **No Mask**.
- Displays the **classification result** in real time.

---