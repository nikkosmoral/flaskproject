from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd

from flask import Flask, render_template

app = Flask(__name__)

# Load the trained model
model = joblib.load("model/corn_yield_model.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    
    # Extract input values
    features = pd.DataFrame({
        'Temparature': [float(data['temperature'])],
        'Humidity': [float(data['humidity'])],
        'Rainfall': [float(data['rainfall'])],
        'Area (ha)': [float(data['area'])],
        'Weather': [data['weather']],
         'CornType': [data['corn_type']]
    })
    
    # Predict using the model
    prediction = model.predict(features)[0]
    
    return jsonify({'predicted_yield_kgs': prediction})

if __name__ == '__main__':
    app.run(debug=True)

