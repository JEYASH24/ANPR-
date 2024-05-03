from ultralytics import YOLO

model = YOLO('License_plate.pt')

results = model(source=r"C:\Users\Keerthana\Downloads\carImages\car11.jpg", show=True, conf=0.3, save=True)