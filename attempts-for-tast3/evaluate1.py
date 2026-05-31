import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

# 【务必按实物真实尺寸修改这里】
objectPoints = np.array([
    [-75, -75, 0],
    [75, -75, 0],
    [75, 75, 0],
    [-75, 75, 0]
], dtype=np.float32)

axis_points = np.float32([
    [0, 0, 0],
    [80, 0, 0],
    [0, 80, 0],
    [0, 0, 80]
])

cameraMatrix = np.array([
    [632.0255, 0, 640.1870],
    [0, 632.1507, 366.0805],
    [0, 0, 1]
], dtype=np.float32)

distCoeffs = np.array([0.089985, -0.189613, 0, 0, 0], dtype=np.float32)

while True:
    success, img = cap.read()
    if not success or img is None:
        continue

    # 原图处理，取消缩放，保证坐标精准
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 0)
    imgCanny = cv2.Canny(imgBlur, 80, 160)

    contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    corner_list = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 100 or area > 800:
            continue

        epsilon = 0.03 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if 4 <= len(approx) <= 6:
            M = cv2.moments(contour)
            if M["m00"] == 0:
                continue
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            points = approx.reshape(-1, 2)
            max_dist = 0
            best_point = None
            for (x, y) in points:
                dist = (x - cx) ** 2 + (y - cy) ** 2
                if dist > max_dist:
                    max_dist = dist
                    best_point = (x, y)

            if best_point is not None:
                corner_list.append([best_point[0], best_point[1]])

    if len(corner_list) >= 4:
        corners = np.array(corner_list[:4], dtype=np.float32)
        left_up = corners[np.argmin(corners[:, 0] + corners[:, 1])]
        right_up = corners[np.argmax(corners[:, 0] - corners[:, 1])]
        right_down = corners[np.argmax(corners[:, 0] + corners[:, 1])]
        left_down = corners[np.argmin(corners[:, 0] - corners[:, 1])]

        imagePoints = np.array([left_up, right_up, right_down, left_down], dtype=np.float32)

        # 可选：画出检测的角点，肉眼校验
        for pt in imagePoints:
            cv2.circle(img, (int(pt[0]), int(pt[1])), 8, (0,255,255), -1)

        _, rvec, tvec = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, distCoeffs)
        projected_axis, _ = cv2.projectPoints(axis_points, rvec, tvec, cameraMatrix, distCoeffs)
        projected_axis = np.int32(projected_axis).reshape(-1, 2)

        origin = tuple(projected_axis[0])
        cv2.line(img, origin, tuple(projected_axis[1]), (0, 0, 255), 3)
        cv2.line(img, origin, tuple(projected_axis[2]), (0, 255, 0), 3)
        cv2.line(img, origin, tuple(projected_axis[3]), (255, 0, 0), 3)
        cv2.circle(img, origin, 5, (255, 255, 255), -1)

    cv2.imshow("Real-Time Pose", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()