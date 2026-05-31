import cv2
import numpy as np

cap = cv2.VideoCapture(0)


def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    return imgCanny


# ===================== 新增：四点排序函数（左上、右上、右下、左下）=====================
def sort_points(points):
    """
    对4个角点进行排序：左上 → 右上 → 右下 → 左下
    :param points: 4个点的数组 [N,2]
    :return: 排序后的4个点
    """
    # 1. 计算中心点
    center = np.mean(points, axis=0)
    # 2. 计算每个点相对于中心的极角
    angles = np.arctan2(points[:, 1] - center[1], points[:, 0] - center[0])
    # 3. 按极角逆时针排序
    sorted_idx = np.argsort(angles)
    sorted_pts = points[sorted_idx]

    # 修正：确保第一个点是 左上
    # 找到x最小且y最小的点作为左上起点
    sum_pts = np.sum(sorted_pts, axis=1)
    left_up_idx = np.argmin(sum_pts)
    sorted_pts = np.roll(sorted_pts, -left_up_idx, axis=0)
    return sorted_pts

objectPoints = np.array([
    [-95, -95, 0],   # 左上
    [95, -95, 0],    # 右上
    [95, 95, 0],     # 右下
    [-95, 95, 0]     # 左下
], dtype=np.float32)

# ===================== 【位姿可视化】3D坐标轴点 =====================
# 画一个3D坐标系：原点O(0,0,0) + X轴 + Y轴 + Z轴（长度100mm）
# 更改远点坐标可以改变可视化坐标系的位置，从而与任务示例中的相同。这里先不改了
axis_points = np.float32([
    [0, 0, 0],        # 原点
    [100, 0, 0],      # X轴
    [0, 100, 0],      # Y轴
    [0, 0, 100]       # Z轴
])

while True:
    ret, img = cap.read()
    if not ret:
        break

    imgContour = img.copy()
    imgCanny = preProcessing(imgContour)

    contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(imgContour, contours, -1, (0, 255, 0), 2)    # 边缘可视化
    corner_markers = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 500:
            continue

        epsilon = 0.03 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        if len(approx) < 4 or len(approx) > 6:
            continue
        # # 调试时验证检测到的图案正确与否
        # # 计算一个简单的边界框
        # x, y, w, h = cv2.boundingRect(approx)
        # # 画出边界框
        # cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 0, 255), 2)
        corner_markers.append(approx)

    # 只在检测到4个特殊图案时执行
    if len(corner_markers) == 4:
        # 1. 求整体中心
        all_pts = []
        for marker in corner_markers:
            pts = marker.reshape(-1, 2)
            all_pts.extend(pts)
        all_pts = np.array(all_pts)
        x_min, y_min = np.min(all_pts, axis=0)
        x_max, y_max = np.max(all_pts, axis=0)
        board_center_x = int((x_min + x_max) / 2)
        board_center_y = int((y_min + y_max) / 2)
        board_center = (board_center_x, board_center_y)

        # 2. 提取每个L形的外角点
        outer_corners = []
        for marker in corner_markers:
            pts = marker.reshape(-1, 2)
            dists = np.linalg.norm(pts - np.array(board_center), axis=1)
            farthest_idx = np.argmax(dists)
            outer_pt = pts[farthest_idx]
            outer_corners.append(outer_pt)
        outer_corners = np.array(outer_corners, dtype=np.float32)

        # ===================== 核心：外角点排序 =====================
        ordered_corners = sort_points(outer_corners)

        # ===================== imagePoints 格式 =====================
        imagePoints = np.array([
            [ordered_corners[0][0], ordered_corners[0][1]],  # 左上
            [ordered_corners[1][0], ordered_corners[1][1]],  # 右上
            [ordered_corners[2][0], ordered_corners[2][1]],  # 右下
            [ordered_corners[3][0], ordered_corners[3][1]]  # 左下
        ], dtype=np.float32)

        # # 打印查看坐标（调试用）
        # print("imagePoints 坐标：\n", imagePoints)


        # # 这一段通过将四个外角点用不同的颜色和数字标注出来，验证四个外角点的排序情况
        # # 可视化
        # cv2.circle(imgContour, board_center, 8, (255, 0, 255), -1)
        # for marker in corner_markers:
        #     cv2.drawContours(imgContour, [marker], 0, (0, 0, 255), 2)
        #     for point in marker:
        #         x, y = point[0]
        #         cv2.circle(imgContour, (x, y), 4, (0, 255, 0), -1)
        #
        # # 按顺序绘制排序后的角点（1-蓝 2-青 3-黄 4-白）
        # colors = [(255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 255, 255)]
        # for i, pt in enumerate(ordered_corners):
        #     x, y = int(pt[0]), int(pt[1])
        #     cv2.circle(imgContour, (x, y), 12, colors[i], -1)
        #     cv2.putText(imgContour, str(i + 1), (x + 10, y + 10),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 1, colors[i], 2)


        #相机内参
        cameraMatrix = np.array([
            [632.0255, 0, 640.1870],
            [0, 632.1507, 366.0805],
            [0, 0, 1]
        ], dtype=np.float32)

        distCoeffs = np.array([0.089985, -0.189613, 0, 0, 0], dtype=np.float32)

        # 使用solvePnP求解相机姿态
        _, rvec, tvec = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, distCoeffs)

        # ===================== 【核心补全】3D位姿坐标轴绘制 =====================
        # 投影3D坐标轴到2D图像
        projected_axis_points, _ = cv2.projectPoints(axis_points, rvec, tvec, cameraMatrix, distCoeffs)
        projected_axis_points = np.int32(projected_axis_points).reshape(-1, 2)

        # 绘制3D坐标系：X红、Y绿、Z蓝
        origin = tuple(projected_axis_points[0])
        cv2.line(imgContour, origin, tuple(projected_axis_points[1]), (0, 0, 255), 2)  # X 红
        cv2.line(imgContour, origin, tuple(projected_axis_points[2]), (0, 255, 0), 2)  # Y 绿
        cv2.line(imgContour, origin, tuple(projected_axis_points[3]), (255, 0, 0), 2)  # Z 蓝

        # 标注XYZ
        cv2.putText(imgContour, "X", tuple(projected_axis_points[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(imgContour, "Y", tuple(projected_axis_points[2]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(imgContour, "Z", tuple(projected_axis_points[3]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow('frame', imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()