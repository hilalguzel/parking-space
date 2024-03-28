import cv2
import pickle

# List to hold the coordinates of car parking spots
width, height = 107, 48

try:
    # Load previously saved parking spots
    with open('CarParkPosition', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

# Function to determine if the mouse is clicked
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        # Add a new parking spot
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            # If the mouse is released and it's on top of a parking spot line, remove that parking spot
            if x1< x< x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    # Save the updated parking spots to a file
    with open('CarParkPosition', 'wb') as f:
        pickle.dump(posList, f)

# Main loop
while True:
    # Read the image
    img = cv2.imread('carParkImg.png')

    # Draw the saved parking spots
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    #cv2.rectangle(img, (50, 192), (157, 240), (255, 0, 255), 2)
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)
