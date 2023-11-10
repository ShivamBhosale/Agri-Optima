from PIL import Image
import tensorflow as tf
import numpy as np

# Define your class names
classes = [
    'Black Soil',
    'Cinder Soil',
    'Laterite Soil',
    'Peat Soil',
    'Yellow Soil',
    # Add more class names here
]

# Load your deep learning model
model = tf.keras.models.load_model('agri_optima_app/templates/agri_optima_app/soil_analysis_V1.h5')

def classify_image(image):
    # Open and resize the uploaded image using Pillow
    img = Image.open(image)
    img = img.resize((220, 220))  # Adjust to your model's input size
    img = np.array(img)
    img = img / 255.0

    print(f"Input image shape: {img.shape}")
    # Make a prediction using your model
    predictions = model.predict(np.array([img]))[0]  # Get the predictions as a 1D array

    # Get the predicted class index
    predicted_class_index = np.argmax(predictions)

    # Get the class label based on the index
    predicted_class_label = classes[int(predicted_class_index)]  # Convert index to int

    print(f"Predicted Class Index: {predicted_class_index}")
    print(f"Predicted Class Label: {predicted_class_label}")
    
    return predicted_class_label
