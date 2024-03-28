import cv2
import cvzone
import pickle
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time
import psutil

# Video stream
cap = cv2.VideoCapture('carPark.mp4')

# Load previously saved parking spots
with open('CarParkPosition', 'rb') as f:
    posList = pickle.load(f)
width, height = 107, 48

# Function to check parking spaces for a single spot
def check_parking_space_single(img_processed, pos):
    x, y = pos

    # Crop the parking spot
    img_crop = img_processed[y:y+height, x:x+width]

    # Count the white pixels in the cropped image
    count = cv2.countNonZero(img_crop)
    cvzone.putTextRect(img, str(count), (x, y + height -3), scale=1,
                       thickness=2, offset=0, colorR=(0, 0, 255))

    # Determine color and thickness based on pixel count
    if count < 950:
        color = (0, 255, 0)
        thickness =3
    else:
        color = (0, 0, 255)
        thickness = 2

    # Draw rectangle around the parking spot
    cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

    # Display the pixel count
    cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                       thickness=2, offset=0, colorR=color)

    return count  # Return the count value

# Function to check parking spaces in parallel
def check_parking_space_parallel(img_processed):
    space_counter = 0

    with ThreadPoolExecutor() as executor:
        # Check parking spaces in parallel
        futures = [executor.submit(check_parking_space_single, img_processed, pos) for pos in posList]

        # Count total empty parking spaces
        for future in futures:
            count = future.result()
            if count is not None and count < 950:
                space_counter += 1

    # Display the count of empty parking spaces on the screen
    cvzone.putTextRect(img, f'Free {space_counter}/ {len(posList)}', (100, 50), scale=3,
                       thickness=5, offset=20, colorR=(0, 200, 0))

# Start timer
start_timer = time.time()

# Main loop
while True:
    start_time = time.time()  # Start of the process

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Read a frame from the video stream
    success, img = cap.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 25, 16)
    img_median = cv2.medianBlur(img_threshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)

    # Check empty parking spaces
    start_processing_time = time.time()  # Start of the process
    check_parking_space_parallel(img_dilate)
    end_processing_time = time.time()  # End of the process

    # Check elapsed time for the timer
    elapsed_timer = time.time() - start_timer

    # Perform operations at specific intervals (e.g., every 5 seconds)
    if elapsed_timer >= 5:  # Check every 5 seconds
        # Calculate total processing time and time to check empty parking spaces
        total_processing_time = end_processing_time - start_processing_time
        total_time = time.time() - start_time

        # Measure CPU usage
        cpu_usage = psutil.cpu_percent()

        # Measure RAM usage
        ram_usage = psutil.virtual_memory().percent

        # Print out processing times and resource usage
        print(f"Average Processing Time: {total_time} seconds")
        print(f"Average Empty Parking Space Check Time: {total_processing_time} seconds")
        print(f"Average CPU Usage: {cpu_usage}%")
        print(f"Average RAM Usage: {ram_usage}%")

        # Reset timer
        start_timer = time.time()
        print("-------------------------------------------")

    cv2.imshow("Image", img)
    cv2.waitKey(1)
