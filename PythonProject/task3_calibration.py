import cv2
import numpy as np
import os  #

# ===================== 指定保存文件夹 =====================
save_dir = "my_photos"  # 想保存到的文件夹名
os.makedirs(save_dir, exist_ok=True)  # 自动创建文件夹，不存在就新建
# ===============================================================

# 获取摄像头设备的指针(设备管理器 -> 照相机)
capture = cv2.VideoCapture(0)
ret = True

num = 0
# 摄像头的读取是连续不断的，需要循环读取
while ret:
    ret, frame = capture.read()

    cv2.imshow("camera", frame)
    # 监听键盘
    key = cv2.waitKey(1) & 0xFF

    # 按 s 键 拍照保存
    if key == ord('s'):
        cv2.imwrite(f"{save_dir}/photo_{num}.jpg", frame)  # 保存到指定文件夹
        print(f"照片已保存：{save_dir}/photo_{num}.jpg")
        num +=1
    # 按 q 键 退出
    elif key == ord('q'):
        break

capture.release()  # 释放指针
cv2.destroyAllWindows()