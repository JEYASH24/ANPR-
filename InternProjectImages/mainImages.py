from ultralytics import YOLO
import cv2
import easyocr
import util
from util import read_license_plate, write_csv

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

results = {}


# Load the YOLO models
coco_model = YOLO('yolov8n.pt')
license_plate_detector = YOLO('License_plate.pt')

# Load the image
image_path = r"C:\Users\Keerthana\Downloads\carImages\car11.jpg"  # Specify the path to your image
frame = cv2.imread(image_path)

vehicles = [2]

# detect vehicles
detections = coco_model(frame)[0]
detections_ = []
for detection in detections.boxes.data.tolist():
    x1, y1, x2, y2, score, class_id = detection
    if int(class_id) in vehicles:
        detections_.append([x1, y1, x2, y2, score])


# detect license plates
license_plates = license_plate_detector(frame)[0]
for license_plate in license_plates.boxes.data.tolist():
    x1, y1, x2, y2, score, class_id = license_plate

    # crop license plate
    license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

    # read license plate number

    license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop)
    print(license_plate_text)

    if license_plate_text is not None:

        results[license_plate_text] = {
            'image_path': image_path,
            'license_plate_bbox': [x1, y1, x2, y2],
            'license_plate_number': license_plate_text,
            'confidence_score': license_plate_text_score
        }

         # Draw bounding box around license plate
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (10, 10, 255), 2)

        # Draw text background
        text_size = cv2.getTextSize(license_plate_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        cv2.rectangle(frame, (int(x1), int(y1) - text_size[1] - 5),
                              (int(x1) + text_size[0] + 10, int(y1)), (10, 10, 255), -1)

                # Draw text
        cv2.putText(frame, license_plate_text, (int(x1) + 5, int(y1) - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show the image with detected text and bounding boxes

    cv2.imshow("Detected License Plate", frame)
    cv2.waitKey(0)

# write results
write_csv(results, 'test.csv')