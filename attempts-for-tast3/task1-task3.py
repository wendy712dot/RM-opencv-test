import cv2
import numpy as np

img = cv2.imread('resources/initial_image.png')

def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)


    return imgCanny





imgContour = img.copy()
imgCanny = preProcessing(imgContour)
    # 根据二值化图像框选图像轮廓
contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # 再根据contours的内容draw出来
# cv2.drawContours(imgContour, contours, -1, (0, 255, 0), 2)

# 存储每个L形的顶点集合
corner_markers = []

# # 存储所有角点
# all_corner_points = []

for cnt in contours:
    # 可选：过滤掉太小的噪声轮廓（根据你的场景调整阈值）
    area = cv2.contourArea(cnt)
    if area < 500:  # 比如面积小于100的轮廓直接跳过
        continue

    epsilon = 0.03 * cv2.arcLength(cnt, True)
    # 对contour做多边形逼近，epsilon定义了原始轮廓和逼近多边形之间的最大距离，
    # epsilon越小逼近的多边形就越接近原始的轮廓
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    #增加对多边形顶点数的限制（L 形目标的顶点数是固定的），减少噪声影响
    if len(approx) < 4 or len(approx) > 6:
        continue

    corner_markers.append(approx)

# ---------------------- 1. 修正：用所有L形顶点求标记板的边界中心 ----------------------
all_pts = []
for marker in corner_markers:
    pts = marker.reshape(-1, 2)
    all_pts.extend(pts)
all_pts = np.array(all_pts)

# 计算整个标记板的外接矩形
x_min, y_min = np.min(all_pts, axis=0)
x_max, y_max = np.max(all_pts, axis=0)

# 标记板的几何中心（这个才是真正的中心）
board_center_x = int((x_min + x_max) / 2)
board_center_y = int((y_min + y_max) / 2)
board_center = (board_center_x, board_center_y)

cv2.circle(imgContour, board_center, 8, (255, 0, 255), -1)

# ---------------------- 2. 对每个L形找外角点 ----------------------
outer_corners = []
for marker in corner_markers:
    pts = marker.reshape(-1, 2)
    dists = np.linalg.norm(pts - np.array(board_center), axis=1)
    farthest_idx = np.argmax(dists)
    outer_pt = pts[farthest_idx]
    outer_corners.append(outer_pt)

outer_corners = np.array(outer_corners, dtype=np.float32)

# ---------------------- 3. 可视化 ----------------------
# 画L形轮廓和顶点
for marker in corner_markers:
    cv2.drawContours(imgContour, [marker], 0, (0, 0, 255), 2)
    for point in marker:
        x, y = point[0]
        cv2.circle(imgContour, (x, y), 4, (0, 255, 0), -1)

# 画外角点
for pt in outer_corners:
    x, y = int(pt[0]), int(pt[1])
    cv2.circle(imgContour, (x, y), 10, (255, 0, 0), -1)


    # 这里仅在调试过程中用于验证筛选的区域正确与否
    # # 计算一个简单的边界框
    # x, y, w, h = cv2.boundingRect(approx)
    # # 画出边界框
    # cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 0, 255), 2)


    # # 1. 计算最小外接旋转矩形
    # rect = cv2.minAreaRect(cnt)
    # # 2. 获取矩形的4个顶点坐标（浮点型）
    # box = cv2.boxPoints(rect)
    # # 3. 转成整数坐标（方便绘图）
    # box = box.astype(int)

    # # 保存角点
    # all_corner_points.append(approx)

    # # 画轮廓和角点（可视化用）
    # cv2.drawContours(imgContour, [approx], 0, (0, 0, 255), 2)
    # for point in approx:
    #     x = point[0][0]
    #     y = point[0][1]
    #     cv2.circle(imgContour, (x, y), 6, (0, 255, 0), -1)  # 画角点


cv2.imshow('frame', imgContour)
cv2.waitKey(0)
cv2.destroyAllWindows()
