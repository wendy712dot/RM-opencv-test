import cv2
import numpy as np

# 不再固定缩放画面，注释原有尺寸定义
# widthImg=540
# heightImg =640

cap = cv2.VideoCapture(1)
cap.set(10, 150)

def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imgDial, kernel, iterations=1)
    return imgThres

def getContours(img):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    return biggest

def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew

# 3D 标定参数
objectPoints = np.array([
    [-75, -75, 0],
    [75, -75, 0],
    [75, 75, 0],
    [-75, 75, 0],
], dtype=np.float32)

cameraMatrix = np.array([
    [632.0255,   0,    640.1870],
    [  0,    632.1507, 366.0805],
    [  0,      0,      1    ]
], dtype=np.float32)

distCoeffs = np.array([0.089985, -0.189613, 0, 0, 0], dtype=np.float32)

axis_points = np.float32([
    [0, 0, 0],
    [80, 0, 0],
    [0, 80, 0],
    [0, 0, 80]
])

while True:
    success, img = cap.read()
    if not success:
        break

    imgContour = img.copy()
    imgThres = preProcessing(img)
    biggest = getContours(imgThres)

    # 检测到有效四边形才执行PnP与坐标轴绘制
    if biggest.size != 0:
        biggest = reorder(biggest)
        imagePoints = biggest.reshape(4, 2).astype(np.float32)

        success_pnp, rvec, tvec = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, distCoeffs)
        if success_pnp:
            projected_axis_points, _ = cv2.projectPoints(axis_points, rvec, tvec, cameraMatrix, distCoeffs)
            projected_axis_points = np.int32(projected_axis_points).reshape(-1, 2)

            origin = tuple(projected_axis_points[0])
            cv2.line(img, origin, tuple(projected_axis_points[1]), (0, 0, 255), 2)  # X红
            cv2.line(img, origin, tuple(projected_axis_points[2]), (0, 255, 0), 2)  # Y绿
            cv2.line(img, origin, tuple(projected_axis_points[3]), (255, 0, 0), 2)  # Z蓝

    cv2.imshow("WorkFlow", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()