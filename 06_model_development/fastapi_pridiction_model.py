from fastapi import FastAPI, File, UploadFile
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO
from PIL import Image

app = FastAPI()

# Load saved model
model = load_model("cat_dog_model.h5")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read image file
    contents = await file.read()
    img = Image.open(BytesIO(contents)).resize((150, 150))

    # Convert to numpy array and preprocess
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    # Make prediction
    prediction = model.predict(img_tensor)
    print(prediction)

    result = "Dog" if prediction[0][0] > 0.5 else "Cat"

    return {"filename": file.filename, "prediction": result}
