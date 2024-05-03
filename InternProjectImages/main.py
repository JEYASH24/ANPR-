import os
import csv
import cv2
from util import read_license_plate, write_csv
from time import sleep
from ultralytics import YOLO

# Load the YOLO models
license_plate_detector = YOLO('License_plate.pt')

# Path to the folder containing images
image_folder = r"C:\Users\Keerthana\Downloads\carImages"

while True:
    # Check for unprocessed images
    unprocessed_images = [filename for filename in os.listdir(image_folder)
                          if filename.endswith(('.jpg', '.jpeg', '.png'))]

    # Load existing results from CSV to track processed images
    processed_images = set()
    if os.path.exists('resultsFolder.csv'):
        with open('resultsFolder.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip the header
            for row in reader:
                image_name = row[0].strip()  # Assuming the first column is the image name
                processed_images.add(image_name)

    # Process unprocessed images
    for filename in unprocessed_images:
        if filename not in processed_images:
            # Load the image
            image_path = os.path.join(image_folder, filename)
            frame = cv2.imread(image_path)

            # detect license plates
            license_plates = license_plate_detector(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate

                # crop license plate
                license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]

                # read license plate number
                license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop)

                if license_plate_text is not None:
                    # Write results to CSV
                    write_csv({license_plate_text: {
                        'image_name': filename,
                        'detected_plate_bbox': [x1, y1, x2, y2],
                        'detected_plate_number': license_plate_text,
                        'confidence_score': license_plate_text_score,
                        'image_path': image_path
                    }}, 'resultsFolder.csv')

    # Sleep for some time before checking for new images
    sleep(10)  # Adjust sleep time as needed
