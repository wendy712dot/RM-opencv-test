import cv2
import numpy as np

###################################
widthImg=540
heightImg =640
#####################################

cap = cv2.VideoCapture(1)
cap.set(10,150)

def preProcessing(img):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  # 转灰度
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)     # 模糊去噪
    imgCanny = cv2.Canny(imgBlur,200,200)            # 边缘检测
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=2) # 膨胀：让边缘变粗
    imgThres = cv2.erode(imgDial,kernel,iterations=1)  # 腐蚀：微调边缘
    return imgThres

def getContours(img):
    biggest = np.array([])
    maxArea = 0
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>5000:                     # 只看大面积轮廓
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True) # 多边形拟合
            if area >maxArea and len(approx) == 4: # 找 4 个角的图形
                biggest = approx           # 保存四个角坐标
                maxArea = area
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)
    return biggest                        # 返回最大四边形

def reorder (myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2),np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)] # 左上
    myPointsNew[3] = myPoints[np.argmax(add)] # 右下
    diff = np.diff(myPoints,axis=1)
    myPointsNew[1]= myPoints[np.argmin(diff)] # 右上
    myPointsNew[2] = myPoints[np.argmax(diff)] # 左下
    return myPointsNew

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
    success, img = cap.read()        # 读取摄像头画面
    img = cv2.resize(img,(widthImg,heightImg))
    imgContour = img.copy()

    imgThres = preProcessing(img)    # 预处理 → 边缘图
    biggest = getContours(imgThres)  # 找最大四边形

    if biggest is not None:
        left_up, right_up, right_down, left_down = biggest

        # ==============================================
        # 【核心】自动生成你要的 imagePoints 格式
        # ==============================================
        imagePoints = np.array([
            [left_up[0], left_up[1]],
            [right_up[0], right_up[1]],
            [right_down[0], right_down[1]],
            [left_down[0], left_down[1]]
        ], dtype=np.float32)

        success, rvec, tvec = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, distCoeffs)

        projected_axis_points, _ = cv2.projectPoints(axis_points, rvec, tvec, cameraMatrix, distCoeffs)
        projected_axis_points = np.int32(projected_axis_points)
        for i in range(1, len(projected_axis_points)):
            cv2.line(img, tuple(projected_axis_points[0].ravel()), tuple(projected_axis_points[i].ravel()),
                 (255, 0, 0), 2)


    cv2.imshow("WorkFlow", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break