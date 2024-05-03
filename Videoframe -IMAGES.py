import cv2
import os
import time  # Import the time module

# Directory to save images
save_dir = 'images'  # Change this to your desired directory name
os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Initialize camera
cap = cv2.VideoCapture(0)  # Use default camera (index 0)
# cap = cv2.VideoCapture('video.mp4')  # Read from video file

frame_count = 0  # Counter to keep track of frames

while True:
    # Capture frame every 1 second (adjust as needed)
    time.sleep(1)  # Delay for 1 second
    
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break  # Break the loop if frame not captured
    
    # Display the frame (optional)
    cv2.imshow('Frame', frame)

    # Save the frame as an image
    frame_count += 1
    file_name = os.path.join(save_dir, f'frame_{frame_count}.jpg')
    cv2.imwrite(file_name, frame)
    print(f'Frame saved as {file_name}')

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera
cap.release()
# Close all OpenCV windows
cv2.destroyAllWindows()
