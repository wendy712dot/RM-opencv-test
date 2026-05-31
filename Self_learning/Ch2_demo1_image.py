import cv2
print("Package Imported")

img=cv2.imread("Resources/lena.png")

cv2.imshow("Output",img)
cv2.waitKey(1000)
cv2.destroyAllWindows()