from flask import Flask, render_template, request, jsonify, send_file
import csv
import os

app = Flask(__name__)
image_folder = r"C:\Users\Keerthana\Downloads\carImages"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_license_plate', methods=['POST'])
def process_license_plate():
    data = request.get_json()
    license_plate = data.get('licensePlate')

    # Read the CSV file
    with open('./resultsFolder.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reversed(list(reader)):
            if row['detected_plate_number'] == license_plate:  # Corrected column name
                # License plate found in the CSV file
                image_path = os.path.join(image_folder, os.path.basename(row['image_name']))
                return jsonify({'message': 'License plate found in CSV file', 'image_path': image_path})
    
    # License plate not found in the CSV file
    return jsonify({'message': 'License plate not found in CSV file'})

@app.route('/get_image')
def get_image():
    image_path = request.args.get('image_path')
    return send_file(image_path, mimetype='image/png')  # Adjust the mimetype as per your image format

if __name__ == '__main__':
    app.run(debug=True)