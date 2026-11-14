import os
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__, template_folder='templates', static_folder='static')

basedir = os.path.abspath(os.path.dirname(__file__))
modelPath = os.path.join(basedir, 'model', 'modelIris-knn.pkl')

try:
    knnModel = joblib.load(modelPath)
    print("Model KNN berhasil dimuat")
except Exception as e:
    print(f"Gagal memuat model: {e}")

labelSepalPatal = {
    'setosa': 'Iris Setosa',
    'versicolor': 'Iris Versi Color',
    'virginica': 'Iris Virginica'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        sl = float(data.get('sepal_length'))
        sw = float(data.get('sepal_weight'))
        pl = float(data.get('petal_length'))
        pw = float(data.get('petal_weight'))

        features = [[sl, sw, pl, pw]]

        prediction = knnModel.predict(features)
        hasilPrediksi = str(prediction[0])

        deskripsiHasil = labelSepalPatal.get(hasilPrediksi, str(hasilPrediksi))

        return jsonify({
            'status': 'success',
            'prediction': deskripsiHasil
        })
    except Exception as e:
        return jsonify({'status' : 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)