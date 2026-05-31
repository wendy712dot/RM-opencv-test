import cv2

#接入电脑摄像头，由于本电脑只有一个摄像头，故为0
cap = cv2.VideoCapture(0)
#分别设置高度（3）和宽度（4）
cap.set(3,640)
cap.set(4,480)
#设置亮度
cap.set(10,720)

while True:
    success, img = cap.read()
    cv2.imshow("Video",img)
    #等待时间到1或者q加回车，跳出语句
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
