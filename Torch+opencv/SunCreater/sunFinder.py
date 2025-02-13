import os
import subprocess
import cv2
import numpy as np

f = cv2.imread("../output.png")
c = cv2.inRange(f, (0, 20, 50), (255, 255, 255))
cnt, _ = cv2.findContours(c, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(len(cnt))
img = np.zeros_like(c)
cnt = sorted(cnt, key=lambda x: -cv2.contourArea(x))
print(cnt[0])

moments = cv2.moments(cnt[0])
if moments["m00"] != 0:
    cx = moments["m10"] / moments["m00"]
    cy = moments["m01"] / moments["m00"]
else:
    cx, cy = 0, 0

cnew = []
for point in cnt[0]:
    x, y = point[0]
    x_new = cx + (x - cx) * (1 - 50 / cv2.arcLength(cnt[0], True))
    y_new = cy + (y - cy) * (1 - 50 / cv2.arcLength(cnt[0], True))
    cnew.append([[int(x_new), int(y_new)]])


cv2.drawContours(img, [np.array(cnew)], -1, (255, 255, 255), cv2.FILLED)
res = cv2.bitwise_and(f, f, mask=img)
print(res.shape)
res[img < 5] = [255, 255, 255]

cv2.imwrite("res.jpg", res)

cv2.imshow("c", res)
cv2.imshow("cjk", img)
cv2.waitKey(100000)