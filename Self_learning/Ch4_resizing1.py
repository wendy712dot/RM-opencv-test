import cv2

img = cv2.imread("Resources/lambo.PNG")
print(img.shape)

#resizing 改变大小
imgResize = cv2.resize(img,(300,200))
print(imgResize.shape)

#cropping 剪裁
imgCropped = img[0:200,200:400]

cv2.imshow("img",img)
cv2.imshow("Resize",imgResize)
cv2.imshow("Cropped",imgCropped)
cv2.waitKey(0)