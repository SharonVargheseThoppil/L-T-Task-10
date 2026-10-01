from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Load the trained CIFAR-10 CNN model
MODEL_PATH = "model/cifar10_cnn_model.keras"
model = tf.keras.models.load_model(MODEL_PATH)

# CIFAR-10 class names
CLASS_NAMES = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck"
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Flask Deep Learning API is running",
        "status": "success"
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": True
    })

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Check whether an image was uploaded
        if "image" not in request.files:
            return jsonify({
                "error": "No image uploaded. Please send an image using the 'image' field."
            }), 400

        file = request.files["image"]

        # Open and preprocess image
        image = Image.open(file).convert("RGB")
        image = image.resize((32, 32))

        # Convert image to NumPy array
        image_array = np.array(image, dtype=np.float32)

        # Normalize pixel values
        image_array = image_array / 255.0

        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)

        # Make prediction
        predictions = model.predict(image_array, verbose=0)

        # Get predicted class
        predicted_index = int(np.argmax(predictions[0]))
        predicted_class = CLASS_NAMES[predicted_index]

        # Get confidence
        confidence = float(np.max(predictions[0])) * 100

        return jsonify({
            "prediction": predicted_class,
            "confidence": round(confidence, 2),
            "class_index": predicted_index
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )