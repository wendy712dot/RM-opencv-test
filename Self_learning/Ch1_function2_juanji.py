import cv2
import numpy as np

img=cv2.imread("Resources/lena.png")
kernel = np.ones((5,5),np.uint8)

imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#高斯滤波
imgBlur=cv2.GaussianBlur(imgGray,(7,7),0)
#边缘检测 数值越大，边缘越少
imaCanny=cv2.Canny(img,150,200)
#膨胀
imaDialation=cv2.dilate(imaCanny,kernel,iterations=1)
#腐蚀
imgEroded=cv2.erode(imaDialation,kernel,iterations=1)

cv2.imshow("Gray Image",imgGray)
cv2.imshow("Blur Image",imgBlur)
cv2.imshow("Canny Image",imaCanny)
cv2.imshow("Dialation Image",imaDialation)
cv2.imshow("Eroded Image",imgEroded)
cv2.waitKey(0)