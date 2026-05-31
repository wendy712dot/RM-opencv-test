import cv2
import numpy as np

# ========================= 配置区域 =========================
# 替换为你通过Trackbars得到的最佳HSV范围
LOWER_H, LOWER_S, LOWER_V = 4, 101, 144
UPPER_H, UPPER_S, UPPER_V = 24, 254, 213

# 轮廓面积限制（只识别在这个范围内的目标）
MIN_CONTOUR_AREA = 200  # 最小面积（过滤小噪点）
MAX_CONTOUR_AREA = 5000  # 最大面积（过滤过大区域）

# 多边形拟合的精度系数
POLY_APPROX_EPSILON = 0.02
# ===========================================================

# 1. 打开视频
video_path = "resources/testVideo.mp4"

cap = cv2.VideoCapture(video_path)

# 检查视频是否成功打开
if not cap.isOpened():
    print("视频打开失败")
    exit()

print("视频打开成功！")

# 定义HSV范围
lower_bound = np.array([LOWER_H, LOWER_S, LOWER_V])
upper_bound = np.array([UPPER_H, UPPER_S, UPPER_V])

while True:
    ret, frame = cap.read()

    # 视频读取结束时提示
    if not ret:
        print("视频播放完毕，按 q 退出")
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        break

    # 颜色分割
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # 形态学操作
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # 查找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    result = frame.copy()

    for contour in contours:
        area = cv2.contourArea(contour)

        # 1. 过滤面积：太小 或 太大 都跳过
        if area < MIN_CONTOUR_AREA or area > MAX_CONTOUR_AREA:
            continue

        # 2. 多边形拟合
        perimeter = cv2.arcLength(contour, True)
        epsilon = POLY_APPROX_EPSILON * perimeter
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # 3. 四边形或五边形才继续
        if len(approx) < 4 or len(approx) > 5:
            continue

        # -------- 满足所有条件：面积合适 + 形状合适 --------
        # 绘制最小外接矩形（绿色）
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        cv2.drawContours(result, [box], 0, (0, 255, 0), 2)

        # 绘制拟合四边形（红色）
        cv2.drawContours(result, [approx], 0, (0, 0, 255), 2)

    # 显示
    cv2.imshow('Result', result)
    # cv2.imshow('Mask', mask)

    # 按 q 退出
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()