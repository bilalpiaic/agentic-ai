import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

# Load the MNIST dataset (images and labels for training and testing)
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Check original shape of data (optional)
# print(x_train.shape, y_train.shape)  # (60000, 28, 28), (60000,)

# Normalize image pixel values to the range [0, 1]
x_train = x_train.astype('float32') / 255.0
x_test  = x_test.astype('float32')  / 255.0

# Convert labels to one-hot encoded vectors
y_train = to_categorical(y_train, num_classes=10)
y_test  = to_categorical(y_test, num_classes=10)

# Check new shape of labels (optional)
# print(y_train.shape)  # (60000, 10)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten

# Initialize a Sequential model
model = Sequential()

# Input layer: Flatten the 28x28 images into vectors of length 784
model.add(Flatten(input_shape=(28, 28)))

# Hidden layer 1: Dense layer with 128 neurons and ReLU activation
model.add(Dense(128, activation='relu'))

model.add(Dense(128, activation='relu'))

# Hidden layer 2: Dense layer with 64 neurons and ReLU activation
model.add(Dense(64, activation='relu'))

# Output layer: Dense layer with 10 neurons (for 10 classes) and softmax activation
model.add(Dense(10, activation='softmax'))

# Optional: print a summary of the model architecture
model.summary()

# Compile the model with an optimizer, loss function, and metrics
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(x_train, 
                    y_train,
                    epochs=2,            # train for 10 epochs
                    batch_size=10,        # 32 samples per gradient update
                    validation_split=0.1) # use 10% of training data for validation

# Evaluate the trained model on the test data
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f"Test loss: {test_loss:.4f}")
print(f"Test accuracy: {test_acc:.4f}")

model.save('mnist_model.h5')

# Load the model (if needed)
from tensorflow.keras.models import load_model
model = load_model('mnist_model.h5')
predictions = model.predict(x_test)


# Make predictions on the first 5 test images
predictions = model.predict(x_test[:5])

# # `predictions` is an array of shape (5, 10) with probabilities for each class.
# # We convert these probabilities to the most likely class index using argmax.
# predicted_labels = np.argmax(predictions, axis=1)

# # Get the true labels for those same 5 test images for comparison
# true_labels = np.argmax(y_test[:5], axis=1)

# print("Predicted labels:", predicted_labels)
# print("True labels:     ", true_labels)
