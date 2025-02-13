import cv2
import numpy as np


def nothing(x): pass


img = cv2.imread('sectors/sector_37_27.jpg')
img = cv2.resize(img, (img.shape[1] * 5, img.shape[0] * 5))
kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
img = cv2.filter2D(img, -1, kernel)

hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.namedWindow("Trackbars")

cv2.createTrackbar("Lower Hue", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Upper Hue", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Lower Saturation", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Upper Saturation", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Lower Value", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Upper Value", "Trackbars", 255, 255, nothing)

while True:
    l_h = cv2.getTrackbarPos("Lower Hue", "Trackbars")
    u_h = cv2.getTrackbarPos("Upper Hue", "Trackbars")
    l_s = cv2.getTrackbarPos("Lower Saturation", "Trackbars")
    u_s = cv2.getTrackbarPos("Upper Saturation", "Trackbars")
    l_v = cv2.getTrackbarPos("Lower Value", "Trackbars")
    u_v = cv2.getTrackbarPos("Upper Value", "Trackbars")
    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv_img, lower_range, upper_range)
    result = cv2.bitwise_and(img, img, mask=mask)
    result = cv2.resize(result, (result.shape[1]//5, img.shape[0]//5), cv2.INTER_LANCZOS4)
    mask = cv2.resize(mask, (mask.shape[1]//5, mask.shape[0]//5), cv2.INTER_LANCZOS4)
    cv2.imshow("Original", img)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
