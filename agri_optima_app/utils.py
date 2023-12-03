from PIL import Image
import tensorflow as tf
import numpy as np

soil_classes = [
    'Black Soil',
    'Cinder Soil',
    'Laterite Soil',
    'Peat Soil',
    'Yellow Soil',
]

soil_model = tf.keras.models.load_model('agri_optima_app/templates/agri_optima_app/soil_analysis_V1.h5')

def classify_image_soil(image):
    img = Image.open(image)
    img = img.resize((220, 220))  # Adjust to your model's input size
    img = np.array(img)
    img = img / 255.0

    print(f"Input image shape: {img.shape}")
    predictions = soil_model.predict(np.array([img]))[0]

    predicted_class_index = np.argmax(predictions)
    predicted_class_label = soil_classes[int(predicted_class_index)]

    print(f"Predicted Class Index: {predicted_class_index}")
    print(f"Predicted Class Label: {predicted_class_label}")

    return predicted_class_label


# plant_classes = [
#     'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___healthy',
#     'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
#     'Potato_blight', 'Soybean___healthy', 'Squash___Powdery_mildew',
#     'Tomato___Bacterial_spot', 'Tomato___Late_blight',
#     'Tomato___Septoria_leaf_spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
#     'Tomato___healthy'
# ]

plant_classes = [
'Apple___Apple_scab', 'Apple___Black_rot',
 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
 'Potato_blight', 'Squash___Powdery_mildew',
 'Tomato_Yellow_Leaf_Curl_Virus'
]

plant_leaf_model = tf.keras.models.load_model('agri_optima_app/templates/agri_optima_app/smallPLD.h5')

def classify_image_plant(image):
    img = Image.open(image)
    img = img.resize((224, 224))  # Adjust to your model's input size
    img = np.array(img)
    img = img / 255.0

    print(f"Input image shape: {img.shape}")
    predictions = plant_leaf_model.predict(np.array([img]))[0]

    predicted_class_index_plant = np.argmax(predictions)
    predicted_class_label_plant = plant_classes[int(predicted_class_index_plant)]

    print(f"Predicted Class Index: {predicted_class_index_plant}")
    print(f"Predicted Class Label: {predicted_class_label_plant}")

    return predicted_class_label_plant
