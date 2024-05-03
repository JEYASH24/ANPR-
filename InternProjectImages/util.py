import easyocr
import cv2
import os
import csv

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# def write_csv(results, output_path):
#     with open(output_path, 'w') as f:
#         f.write('image_name,detected_plate_bbox,detected_plate_number,confidence_score, image_path\n')

#         for plate_info in results.values():
#             image_name = plate_info['image_name']
#             bbox = plate_info['detected_plate_bbox']
#             plate_number = plate_info['detected_plate_number']
#             confidence_score = plate_info['confidence_score']
#             image_path = plate_info['image_path']
#             f.write('{},"{}","{}",{}, {}\n'.format(image_name, bbox, plate_number, confidence_score, image_path))
#         f.close()


def write_csv(results, filename):
    mode = 'a' if os.path.exists(filename) else 'w'
    with open(filename, mode, newline='') as csvfile:
        fieldnames = ['image_name', 'detected_plate_bbox', 'detected_plate_number', 'confidence_score', 'image_path']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if mode == 'w':
            writer.writeheader()

        for result in results.values():
            writer.writerow({
                'image_name': result['image_name'],
                'detected_plate_bbox': result['detected_plate_bbox'],
                'detected_plate_number': result['detected_plate_number'],
                'confidence_score': result['confidence_score'],
                'image_path': result['image_path']
            })

        csvfile.flush()  # Ensure the data is written immediately without buffering


def license_complies_format(text):
    # Remove spaces and dashes from the text
    text = text.replace(' ', '').replace('-', '')

    # Check if the text is empty or too short
    if len(text) < 7:
        return False
    
    if not text[-5].isalpha():
        return False
    
    if not text[-4:].isdigit():
        return False

    # Check if the text matches any of the four specified formats
    format_1 = text[0].isalpha() and text[1].isalpha() and text[2].isdigit() and text[3].isdigit() \
               and text[4].isalpha() and text[5].isalpha() and text[6:].isdigit()

    format_2 = text[0].isalpha() and text[1].isalpha() and text[2].isdigit() and text[3].isalpha() \
               and text[4].isalpha() and text[5:].isdigit()

    format_3 = text[0].isalpha() and text[1].isalpha() and text[2].isdigit() and text[3].isdigit() \
               and text[4].isalpha() and text[5:].isdigit()

    format_4 = text[0].isalpha() and text[1].isalpha() and text[2].isdigit() and text[3].isalpha() and text[4:].isdigit()

    return format_1 or format_2 or format_3 or format_4


def read_license_plate(license_plate_crop):
    max_confidence = 0
    best_license_plate = None

    # Convert license plate crop to grayscale
    license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)

    for threshold_value in range(1, 230):
        
        # Apply thresholding
        _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, threshold_value, 255, cv2.THRESH_BINARY_INV)

        # Read text from the thresholded image
        detected_text = reader.readtext(license_plate_crop_thresh)

        # Extract valid characters from detected text
        text = ""
        for detection in detected_text:
            bbox, detected_text, score = detection
            detected_text = detected_text.upper().replace(' ', '')
            for char in detected_text:
                if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                    text += char

        # Check if the extracted text complies with license plate format
        if license_complies_format(text):
            # Check if the confidence score is the highest so far
            if score > max_confidence:
                max_confidence = score
                best_license_plate = text

    return best_license_plate, max_confidence



