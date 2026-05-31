import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# ===================== 【关键加速：降低分辨率！最重要！】 =====================
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

objectPoints = np.array([
    [-75, -75, 0], [75, -75, 0], [75, 75, 0], [-75, 75, 0]
], dtype=np.float32)

cameraMatrix = np.array([
    [632.0255, 0, 640.1870],
    [0, 632.1507, 366.0805],
    [0, 0, 1]
], dtype=np.float32)

axis_points = np.float32([
    [0,   0,   0],   # 原点（物体中心）
    [80,  0,   0],   # X轴：向右 80mm
    [0,   80,  0],   # Y轴：向下 80mm
    [0,   0,   80]   # Z轴：向外 80mm
])

distCoeffs = np.array([0.089985, -0.189613, 0, 0, 0], dtype=np.float32)

while True:
    success, img = cap.read()
    if not success:
        break

    # ===================== 【加速：缩小图像】 =====================
    img_small = cv2.resize(img, (320, 240))
    scale = 2  # 因为缩小了，坐标要乘回去

    # 预处理（轻量化）
    imgGray = cv2.cvtColor(img_small, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 0)  # 变小核，更快
    imgCanny = cv2.Canny(imgBlur, 80, 160)  # 提高阈值，减少轮廓

    # 只找外轮廓，加速
    contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    corner_list = []

    for contour in contours:
        area = cv2.contourArea(contour)

        # ===================== 【加速：严格过滤面积】 =====================
        if area < 30 or area > 3000:  # 太小太大都不要
            continue

        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if 4 <= len(approx) <= 6:
            # 取中心点（超快）
            M = cv2.moments(contour)
            if M["m00"] == 0:
                continue
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # 找最远点
            points = approx.reshape(-1, 2)
            max_dist = 0
            best = None
            for (x, y) in points:
                dist = (x - cx) ** 2 + (y - cy) ** 2
                if dist > max_dist:
                    max_dist = dist
                    best = (x, y)
            if best is not None:
                corner_list.append((best[0] * scale, best[1] * scale))  # 坐标还原

    # ===================== 实时打印 4 个角点 =====================
    if len(corner_list) >= 4:
        corners = np.array(corner_list[:4], dtype=np.float32)

        left_up = corners[np.argmin(corners[:, 0] + corners[:, 1])]
        right_up = corners[np.argmax(corners[:, 0] - corners[:, 1])]
        right_down = corners[np.argmax(corners[:, 0] + corners[:, 1])]
        left_down = corners[np.argmin(corners[:, 0] - corners[:, 1])]

        imagePoints = np.array([left_up, right_up, right_down, left_down], dtype=np.float32)

        # 实时打印
        print("实时4角点：")
        print(imagePoints)
        print("-" * 50)

        # _, rvec, tvec = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, distCoeffs)
        #
        # projected_axis_points, _ = cv2.projectPoints(axis_points, rvec, tvec, cameraMatrix, distCoeffs)
        # projected_axis_points = np.int32(projected_axis_points)
        # for i in range(1, len(projected_axis_points)):
        #     cv2.line(img, tuple(projected_axis_points[0].ravel()), tuple(projected_axis_points[i].ravel()),
        #              (255, 0, 0), 2)

    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
