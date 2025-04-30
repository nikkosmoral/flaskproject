from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd
from db import insert_prediction, fetch_predictions  # Import database functions

app = Flask(__name__)

# Load the trained model and encoders
model = joblib.load("model/corn_yield_model.pkl")
weather_encoder = joblib.load("weather_encoder.pkl")
corn_type_encoder = joblib.load("corn_type_encoder.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form

    # Extract input values
    features = pd.DataFrame({
        'Temperature': [float(data['Temperature'])],
        'Humidity': [float(data['Humidity'])],
        'Rainfall': [float(data['Rainfall'])],
        'Area (ha)': [float(data['Area (ha)'])],
        'Weather': [data['Weather']],
        'CornType': [data['CornType']]
    })

    # Encode categorical variables
    features['Weather'] = weather_encoder.transform(features['Weather'])
    features['CornType'] = corn_type_encoder.transform(features['CornType'])

    # Ensure feature order matches training data
    features = features[model.feature_names_in_]

    # Predict using the model
    prediction = model.predict(features)[0]

    # Store prediction in the database
    insert_prediction(
        temperature=features['Temperature'][0],
        humidity=features['Humidity'][0],   
        rainfall=features['Rainfall'][0],
        area=features['Area (ha)'][0],
        weather=data['Weather'],
        corn_type=data['CornType'],
        predicted_yield=prediction
    )

    return jsonify({'predicted_yield_kgs': prediction})

@app.route('/predictions', methods=['GET'])
def get_predictions():
    """Fetch stored predictions from the database."""
    return jsonify(fetch_predictions())

if __name__ == '__main__':
    app.run(debug=True)
