import os
from ultralytics import YOLO
import cv2
from util import read_license_plate, write_csv

# Load the YOLO models
license_plate_detector = YOLO('License_plate.pt')

# Path to the folder containing images
image_folder = r"C:\Users\Keerthana\Downloads\carImages"

# Initialize results dictionary
results = {}

# Loop through each image in the folder
for filename in os.listdir(image_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
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
                results[license_plate_text] = {
                    'image_name': filename,
                    'detected_plate_bbox': [x1, y1, x2, y2],
                    'detected_plate_number': license_plate_text,
                    'confidence_score': license_plate_text_score,
                    'image_path' : image_path
                }

# write results to CSV
write_csv(results, 'resultsFolder.csv')
