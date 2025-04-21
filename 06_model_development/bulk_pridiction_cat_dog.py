import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import shutil

# Load saved model
model = load_model("cat_dog_model.h5")

# Create output directories if they don't exist
os.makedirs("cats", exist_ok=True)
os.makedirs("dogs", exist_ok=True)

# Folder containing images
data_folder = "data"

# Iterate over images in data folder
for img_file in os.listdir(data_folder):
    img_path = os.path.join(data_folder, img_file)

    # Load and preprocess image
    img = image.load_img(img_path, target_size=(150, 150))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    # Predict
    prediction = model.predict(img_tensor)
    
    # Move file based on prediction
    if prediction[0][0] > 0.5:
        shutil.copy(img_path, os.path.join("dogs", img_file))
        print(f"{img_file}: Dog")
    else:
        shutil.copy(img_path, os.path.join("cats", img_file))
        print(f"{img_file}: Cat")