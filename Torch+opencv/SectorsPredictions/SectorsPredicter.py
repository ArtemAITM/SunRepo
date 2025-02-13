import cv2
import numpy as np
from scipy.spatial import distance


def merge_close_contours(contours, threshold):
    merged_contours = []
    used = [False] * len(contours)

    for i, cnt1 in enumerate(contours):
        if used[i]:
            continue
        merged = cnt1.copy()
        used[i] = True
        for j, cnt2 in enumerate(contours):
            if used[j]:
                continue
            if is_close(merged, cnt2, threshold):
                merged = np.vstack((merged, cnt2))
                used[j] = True
        merged_contours.append(merged)
    return merged_contours


def is_close(cnt1, cnt2, threshold):
    for pt1 in cnt1:
        for pt2 in cnt2:
            if distance.euclidean(pt1[0], pt2[0]) < threshold:
                return True
    return False


null = [0, 0]
end = [63, 63]
contours = []
for i in range(null[0], end[0] + 1):
    for j in range(null[1], end[1] + 1):
        img = cv2.imread(f"sectors/sector_{i}_{j}.jpg")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_gray = clahe.apply(gray)
        black = cv2.inRange(enhanced_gray, 0, 40)
        c, _ = cv2.findContours(black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in c:
            contour[:, 0, 0] += 32 * i
            contour[:, 0, 1] += 32 * j
            contours.append(contour)

k = merge_close_contours(contours, 3)
print(f"Конечное число контуров: {len(k)}")
