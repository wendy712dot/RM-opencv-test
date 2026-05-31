import cv2
import numpy as np

img = np.zeros((512,512,3), np.uint8)
print(img)
#让整个画板为蓝色
#img[:]=255,0,0

#画线
cv2.line(img,(0,0),(300,300),(0,255,0),3)
#贯穿到另一个角的线：img.shape[1]表示图片的深度（矩阵中的第二个参数）；img.shape[0]表示图片的高度（矩阵中的第一个参数）
cv2.line(img,(0,300),(img.shape[1],img.shape[0]),(0,0,255),3)

#画矩形
cv2.rectangle(img,(0,0),(300,300),(0,0,255),3)
#填充矩形
cv2.rectangle(img,(0,0),(300,300),(0,0,255),cv2.FILLED)

#画圆 （厚度指线条粗细）
cv2.circle(img,(400,50),30,(255,255,0),5)

#写字 （fontScale是字体大小，可以为小数）
cv2.putText(img,"WENDY WENG",(300,200),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)


cv2.imshow("img",img)
cv2.waitKey(0)