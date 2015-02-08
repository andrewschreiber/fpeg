import cv2
import numpy as np
import os

# make output dir
if not os.path.exists("output"):
  os.makedirs("output")


cascade = cv2.CascadeClassifier("models/haarcascade_frontalface_default.xml")

filename = "images/got.jpg"
filename_compressed = "output/compressed.jpg"
filename_fpeg = "output/fpeg.jpg"

BACKGROUND_QUALITY = 10
FACE_QUALITY = 75


# load source and compressed version
source = cv2.imread(filename)
cv2.imwrite(filename_compressed, source, [cv2.IMWRITE_JPEG_QUALITY, BACKGROUND_QUALITY])

compressed = cv2.imread(filename_compressed)

# find faces as rects
faces = cascade.detectMultiScale(source, scaleFactor = 1.1,
                                 minNeighbors = 5, minSize=(30,30),
                                 flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

print "found {} faces!".format(faces.size/4)


# move faces from source to compressed source
for (x, y, w, h) in faces:
  compressed[y:(y + h), x:(x + w)] = source[y:(y + h), x:(x + w)]
  cv2.rectangle(compressed, (x, y), (x + w, y + h), (0, 255, 0), 2)


cv2.imwrite(filename_fpeg, compressed, [cv2.IMWRITE_JPEG_QUALITY, FACE_QUALITY])


cv2.imwrite("output/test1.jpg", source, [cv2.IMWRITE_JPEG_QUALITY, BACKGROUND_QUALITY])
tmp = cv2.imread("output/test1.jpg")
cv2.imwrite("output/test2.jpg", tmp, [cv2.IMWRITE_JPEG_QUALITY, 100])
cv2.imwrite("output/sourceTest.jpg", source, [cv2.IMWRITE_JPEG_QUALITY, FACE_QUALITY])
