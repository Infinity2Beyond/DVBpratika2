import cv2

cap = cv2.VideoCapture('cam_video.mp4')
# Define target area
center_x, center_y = cap.get(3) // 2, cap.get(4) // 2
target_width, target_height = 200, 200
target_left, target_top = center_x - target_width // 2, center_y - target_height // 2
target_right, target_bottom = target_left + target_width, target_top + target_height

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Draw target area
    cv2.rectangle(frame, (int(target_left), int(target_top)), (int(target_right), int(target_bottom)), (0, 0, 255), 2)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    ret, thresh = cv2.threshold(gray, 105, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y), (x+w, y+h),(0,255,0),2)
        # Calculate the center of the contour
        cx = x + w // 2
        cy = y + h // 2

        # Check if the center is within the target area
        if target_left <= cx <= target_right and target_top <= cy <= target_bottom:
            print("The mark hits the target area! Coordinate: ({}, {})".format(x, y))
        else:
            print("Not hit")

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
