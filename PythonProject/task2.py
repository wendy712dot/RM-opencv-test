import cv2
import numpy as np

img = cv2.imread('resources/initial_image.png')
imgContour = img.copy()

#这里先二值化（让findcounter能找），再降噪
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
imgCanny = cv2.Canny(imgBlur, 50, 50)
# img_Gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 根据二值化图像框选图像轮廓
contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# 再根据contours的内容draw出来
cv2.drawContours(imgContour, contours, -1, (0, 255, 0), 2)


for contour in contours:
    # 过滤掉太小的轮廓（避免噪声）
    area = cv2.contourArea(contour)
    if area < 500:
        continue
    # 计算每个封闭的contour的周长，乘0.03赋值给epsilon作为拟合的精度参数
    epsilon = 0.03 * cv2.arcLength(contour, True)
    # 对contour做多边形逼近，epsilon定义了原始轮廓和逼近多边形之间的最大距离，
    # epsilon越小逼近的多边形就越接近原始的轮廓
    approx = cv2.approxPolyDP(contour, epsilon, True)
    #增加对多边形顶点数的限制（L 形目标的顶点数是固定的），减少噪声影响
    if len(approx) < 4 or len(approx) > 6:
        continue

    # 计算一个简单的边界框
    x, y, w, h = cv2.boundingRect(approx)
    # 画出边界框
    cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 0, 255), 2)




cv2.imshow("imgcontour", imgContour)
# cv2.imshow("gray", imgGray)
# cv2.imshow("contours", contours)
cv2.waitKey(0)
cv2.destroyAllWindows()