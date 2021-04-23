import locate
import cv2
import recognise

locate.load_model()
frame = cv2.imread('C:\\Users\\lenovo\\Desktop\\test_images\\test3.jpg')
locate.run_locate(frame)
