import cv2
import numpy as np
#定义空函数，给滑动条做回调函数用
def empty(a):
    pass

# 创建滑条窗口,并设定大小
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
# 创建6个滑条，分别控制 HSV 的最小值和最大值
cv2.createTrackbar("h min","TrackBars",4,180,empty)
cv2.createTrackbar("h max","TrackBars",24,180,empty)
cv2.createTrackbar("s min","TrackBars",101,255,empty)
cv2.createTrackbar("s max","TrackBars",254,255,empty)
cv2.createTrackbar("v min","TrackBars",144,255,empty)
cv2.createTrackbar("v max","TrackBars",213,255,empty)

# 无限循环，实时读取滑动条的值并更新图像，从而确定 HSV 范围
while True:
    h_min = cv2.getTrackbarPos("h min", "TrackBars")
    img_bgr = cv2.imread("resources/test.png")
    # 将图片从 BGR 格式 转为 HSV 格式，便于颜色提取
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    # 获取所有6个滑动条的当前值并实时更新
    h_min = cv2.getTrackbarPos("h min", "TrackBars")
    h_max = cv2.getTrackbarPos("h max", "TrackBars")
    s_min = cv2.getTrackbarPos("s min", "TrackBars")
    s_max = cv2.getTrackbarPos("s max", "TrackBars")
    v_min = cv2.getTrackbarPos("v min", "TrackBars")
    v_max = cv2.getTrackbarPos("v max", "TrackBars")
    # 把最小值和最大值转成 numpy 数组（OpenCV需要这种格式）
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    #生成掩码，白色部分保留
    img_mask = cv2.inRange(img_hsv, lower, upper)
    # 按位与运算：用掩码把原图中符合颜色的部分提取出来
    img_out = cv2.bitwise_and(img_bgr, img_bgr, mask=img_mask)
# img_h, img_s, img_v = cv2.split(img_hsv)
# mask_h = cv2.inRange(img_h, 20, 30)
# mask_s = cv2.inRange(img_h, 20, 30)
# mask_v = cv2.inRange(img_h, 20, 30)
# mask_h_and_s = cv2.bitwise_and(mask_h, mask_s)
# mask = cv2.bitwise_and(mask_h_and_s, mask_v)
# img_out = cv2.bitwise_and(img_bgr, img_bgr, mask = mask)

# cv2.imshow("img", img_out)
# cv2.imwrite("img_out.png", img_out)

    # cv2.imshow("ori",img_bgr)
    # cv2.imshow("hsv",img_hsv)
    cv2.imshow("mask",img_mask)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # 按 esc 键退出
        break
# 退出循环后，关闭所有OpenCV打开的窗口，只显示最终效果图，并保存到本地
cv2.destroyAllWindows()
cv2.imshow("img", img_out)
cv2.imwrite("img_out.png", img_out)
cv2.waitKey(0)