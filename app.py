from flask import Flask, request, jsonify, render_template
import os
import json

app = Flask(__name__)

# Data file
DATA_FILE = 'therapists.txt'

# Helper function to read data from file
def read_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Helper function to write data to file
def write_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/therapists', methods=['GET'])
def get_therapists():
    data = read_data()
    return jsonify(data)

@app.route('/api/therapists', methods=['POST'])
def add_therapist():
    name = request.json.get('name')
    data = read_data()
    data.append({'name': name, 'ratings': []})
    write_data(data)
    return jsonify({'name': name, 'ratings': []}), 201

@app.route('/api/therapists/<int:ther_id>/ratings', methods=['POST'])
def add_rating(ther_id):
    rating = request.json.get('rating')
    text = request.json.get('text')
    data = read_data()
    if 0 <= ther_id < len(data):
        data[ther_id]['ratings'].append({'rating': rating, 'text': text})
        write_data(data)
        return jsonify(data[ther_id]), 201
    return jsonify({'error': 'Therapist not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
