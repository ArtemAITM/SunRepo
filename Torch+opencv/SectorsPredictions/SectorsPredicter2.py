import cv2
import numpy as np
from sklearn.cluster import DBSCAN


def extract_contour_centers(contours):
    centers = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        centers.append((x + w // 2, y + h // 2))
    return np.array(centers)


def count_groups_and_members(contours, distance_threshold=30):
    centers = extract_contour_centers(contours)
    dbscan = DBSCAN(eps=distance_threshold, min_samples=1)
    labels = dbscan.fit_predict(centers)
    unique_labels = np.unique(labels)
    group_count = len(unique_labels)
    group_members = {label: 0 for label in unique_labels}
    for label in labels:
        group_members[label] += 1

    return group_count, group_members


def shift_contours(contours, sector_x, sector_y, sector_size):
    shifted_contours = []
    for cnt in contours:
        shifted_contours.append(cnt + [sector_x * sector_size, sector_y * sector_size])
    return shifted_contours


def merge_close_contours(contours, threshold=2):
    merged_contours = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        merged = False
        for i, mc in enumerate(merged_contours):
            mx, my, mw, mh = cv2.boundingRect(mc)
            if abs(x - mx) <= threshold and abs(y - my) <= threshold:
                merged_contours[i] = np.vstack((mc, cnt))
                merged = True
                break
        if not merged:
            merged_contours.append(cnt)
    return merged_contours


null = [0, 0]
end = [63, 63]
contours = []

for i in range(null[0], end[0] + 1):
    for j in range(null[1], end[1] + 1):
        img = cv2.imread(f"../sectors/sector_{i}_{j}.jpg")
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (0, 0, 0), (255, 255, 225))
        white_pixels = np.all(img == [255, 255, 255], axis=-1)
        white_pixel_count = np.sum(white_pixels)
        if white_pixel_count > 5000:
            continue
        c, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in c:
            if cv2.contourArea(contour) < 50:
                continue
            shift_contours(contours, i, j, 512)
            contours.append(contour)
#        cv2.imshow("img", img)
#        cv2.imshow("th", mask)
#        cv2.waitKey(1)

print(len(contours))
k = merge_close_contours(contours, 3)
print(len(k))

distance_threshold = 60
group_count, group_members = count_groups_and_members(k, distance_threshold)
print(f"Общее количество групп: {group_count}")
for group, members in group_members.items():
    print(f"Группа {group}: {members} контуров")


