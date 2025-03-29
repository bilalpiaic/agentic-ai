## 1. Introduction to Keras
**
Neural Network
9https://docs.google.com/document/d/1BN4-8vTZ94PAot-5ZSufZ_yXAIe2epuxY_d3iu7lzlE/edit?usp=sharing **
**Keras** is a high-level neural networks API written in Python. It runs on top of backends like TensorFlow, making it simple to prototype, build, and deploy deep learning models. Its ease of use and intuitive design makes it a popular choice for both beginners and experienced practitioners.

**Key Points:**
- **User-friendly:** Minimalistic API designed for quick experimentation.
- **Modularity:** Models are made by connecting configurable building blocks (layers, optimizers, etc.).
- **Backend Agnostic:** While TensorFlow is the most common backend, Keras can also run on Theano, CNTK, etc.

---

## 2. Environment Setup

Before starting with Keras, ensure you have TensorFlow installed (which includes Keras as `tf.keras`). You can install TensorFlow via pip:

```bash
pip install tensorflow
```

This command installs TensorFlow 2.x, which integrates Keras directly into its API.

---

## 3. Building a Model with the Sequential API

The **Sequential API** is one of the simplest ways to build a model in Keras. It lets you stack layers linearly.

### Example: A Simple Feedforward Neural Network

```python
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# Create a Sequential model
model = Sequential([
    # Input layer (specify input shape for the first layer)
    Dense(64, activation='relu', input_shape=(100,)),  
    # Hidden layer with dropout for regularization
    Dropout(0.5),
    Dense(64, activation='relu'),
    # Output layer (for binary classification, using sigmoid activation)
    Dense(1, activation='sigmoid')
])

# Display the model summary
model.summary()
```

**Explanation:**
- **Input Layer:** The first `Dense` layer has an `input_shape` parameter. In this example, we assume each input sample is a vector of length 100.
- **Hidden Layers:** Two hidden layers with 64 neurons each using the ReLU activation function. Dropout is added to help prevent overfitting.
- **Output Layer:** A single neuron with a sigmoid activation is typical for binary classification.

---

## 4. Compiling the Model

After defining the model architecture, compile the model. This step configures the learning process by setting the optimizer, loss function, and evaluation metrics.

### Example:

```python
model.compile(
    optimizer='adam',                # Optimizer to update weights
    loss='binary_crossentropy',      # Loss function for binary classification
    metrics=['accuracy']             # Evaluation metric
)
```

**Explanation:**
- **Optimizer:** 'adam' is widely used due to its adaptive learning rate.
- **Loss Function:** 'binary_crossentropy' is suitable for binary classification problems.
- **Metrics:** Accuracy is a common metric for classification tasks.

---

## 5. Training the Model

Training involves feeding the model with data and letting it learn patterns. This is done using the `model.fit()` method.

### Example: Training with Dummy Data

```python
import numpy as np

# Generate dummy training data
X_train = np.random.rand(1000, 100)  # 1000 samples, each with 100 features
y_train = np.random.randint(2, size=(1000, 1))  # 1000 binary labels

# Train the model
history = model.fit(
    X_train, y_train,
    epochs=10,             # Number of times to iterate over the dataset
    batch_size=32,         # Number of samples per gradient update
    validation_split=0.2   # Reserve 20% of data for validation
)
```

**Explanation:**
- **Epochs:** Number of complete passes through the training dataset.
- **Batch Size:** Number of samples processed before the model's weights are updated.
- **Validation Split:** A fraction of the training data set aside for validation during training.

---

## 6. Evaluating and Making Predictions

Once trained, you can evaluate your model on unseen test data or use it to make predictions.

### Example: Evaluating the Model

```python
# Generate dummy test data
X_test = np.random.rand(200, 100)
y_test = np.random.randint(2, size=(200, 1))

# Evaluate the model on the test data
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test loss: {test_loss}, Test accuracy: {test_accuracy}")
```

### Example: Making Predictions

```python
# Predict probabilities on new data
predictions = model.predict(X_test)
# For binary classification, convert probabilities to class labels
predicted_classes = (predictions > 0.5).astype("int32")
print(predicted_classes[:5])
```

**Explanation:**
- **model.evaluate:** Computes the loss and metric values for the model on test data.
- **model.predict:** Outputs the predicted values. For classification, these probabilities are often converted to class labels based on a threshold (0.5 for binary classification).

---

## 7. Advanced Topic: The Functional API

The **Functional API** allows you to build more complex models, including those with multiple inputs, outputs, or non-linear topology (e.g., models with shared layers or residual connections).

### Example: Building a Model Using the Functional API

```python
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model

# Define the input
inputs = Input(shape=(100,))

# Define the layers and connect them
x = Dense(64, activation='relu')(inputs)
x = Dense(64, activation='relu')(x)
outputs = Dense(1, activation='sigmoid')(x)

# Create the model
functional_model = Model(inputs=inputs, outputs=outputs)
functional_model.summary()

# Compile the model
functional_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
```

**Explanation:**
- **Inputs:** The `Input` layer defines the shape of the input data.
- **Layer Connections:** Layers are called as functions on tensors to build the computation graph.
- **Model Creation:** The `Model` function links the inputs and outputs.

---

## 8. Callbacks and Model Checkpoints

Callbacks provide a way to customize the behavior of the training process. Common examples include early stopping and saving the best model.

### Example: Using EarlyStopping and ModelCheckpoint

```python
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Early stopping to halt training when a monitored metric has stopped improving.
early_stopping = EarlyStopping(monitor='val_loss', patience=3, verbose=1)

# Save the model after every epoch if the validation loss improves.
model_checkpoint = ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True, verbose=1)

# Train the model with callbacks
history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stopping, model_checkpoint]
)
```

**Explanation:**
- **EarlyStopping:** Monitors a metric (e.g., validation loss) and stops training if no improvement is seen for a number of epochs (patience).
- **ModelCheckpoint:** Saves the model to disk when a new best performance is observed.

---

## 9. Saving and Loading Models

After training, you might want to save your model for later use.

### Example: Saving and Loading a Model

```python
# Save the entire model to a HDF5 file
model.save('my_model.h5')

# Later, load the model (for inference or further training)
from tensorflow.keras.models import load_model
loaded_model = load_model('my_model.h5')

# Verify that the loaded model works as expected
loaded_model.evaluate(X_test, y_test)
```

**Explanation:**
- **model.save:** Saves the architecture, weights, and training configuration.
- **load_model:** Loads the saved model for further use.
