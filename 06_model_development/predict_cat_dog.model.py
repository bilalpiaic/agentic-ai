import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load saved model
model = load_model("cat_dog_model.h5")

# Load image
img_path = "226.jpg"  # Your image path
img = image.load_img(img_path, target_size=(150, 150))
img_tensor = image.img_to_array(img)
img_tensor = np.expand_dims(img_tensor, axis=0)
img_tensor /= 255.

# Predict
prediction = model.predict(img_tensor)
print("Dog" if prediction[0][0] > 0.5 else "Cat")