import cv2 as cv
import sys
import pytesseract

img = cv.imread("resources\\test1.png")
g = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

#r, img = cv.threshold(img,127, 255, cv.THRESH_BINARY)
# img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

dst = cv.cornerHarris(g, 2, 3, 0.04)
dst = cv.dilate(dst, None)
img[dst>0.01*dst.max()]=[0,0,255]

cv.imshow("t", img)
cv.waitKey(0)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

print(pytesseract.image_to_string(img))