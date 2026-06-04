from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
import numpy as np

app = Flask(__name__)
CORS(app)

# Load trained model
model = tf.keras.models.load_model("model.h5")

# CIFAR10 class labels
classes = ['airplane','automobile','bird','cat','deer',
           'dog','frog','horse','ship','truck']

@app.route('/predict', methods=['POST'])
def predict():

    file = request.files['image']

    image = Image.open(file).convert('RGB')
    image = image.resize((32,32))

    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)

    prediction = model.predict(image)

    predicted_class = classes[np.argmax(prediction)]

    return jsonify({
        "prediction": predicted_class
    })

if __name__ == '__main__':
    app.run(debug=True)