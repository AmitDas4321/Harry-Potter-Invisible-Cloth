import cv2
import numpy as np
import time

print("Starting blue invisibility cloak... Press 'q' to quit.")

cap = cv2.VideoCapture(0)

time.sleep(3)

background = 0

for i in range(30):
    ret, background = cap.read()

    if not ret:
        print("Couldn't capture the background.")
        cap.release()
        exit()

background = np.flip(background, axis=1)

while cap.isOpened():

    ret, img = cap.read()

    if not ret:
        break

    img = np.flip(img, axis=1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([90, 80, 80])
    upper_blue = np.array([130, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    kernel = np.ones((3, 3), np.uint8)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    mask_inv = cv2.bitwise_not(mask)

    background_part = cv2.bitwise_and(
        background,
        background,
        mask=mask
    )

    current_part = cv2.bitwise_and(
        img,
        img,
        mask=mask_inv
    )

    final_output = cv2.addWeighted(
        background_part,
        1,
        current_part,
        1,
        0
    )

    cv2.imshow("Blue Invisibility Cloak", final_output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()