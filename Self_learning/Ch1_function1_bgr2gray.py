import cv2
img=cv2.imread("Resources/lena.png")

imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#高斯滤波
imgBlur=cv2.GaussianBlur(imgGray,(7,7),0)
#边缘检测 数值越大，边缘越少
imaCanny=cv2.Canny(img,150,200)

cv2.imshow("Gray Image",imgGray)
cv2.imshow("Blur Image",imgBlur)
cv2.imshow("Canny Image",imaCanny)
cv2.waitKey(0)
