import cv2
import copy

image = cv2.imread("images/friends.jpg")

faceCascade = cv2.CascadeClassifier("models/haarcascade_profileface.xml")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("gray.jpg", gray)

# detectMultiScale is a general function that detects objects
# scaleFactor compensates from some faces being closer than others
faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.1,
                                     minNeighbors = 5, minSize=(30,30),
                                     flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

i = 0
for (x, y, w, h) in faces:
  i += 1
  cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
  face_img = image[y:(y + h), x:(x + w)]
  gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
  gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
  image[y:(y + h), x:(x + w)] = gray_bgr
  cv2.imwrite("face" + str(i) + ".jpg", face_img)

print str(len(faces)) + " faces found"

cv2.imwrite("faces.jpg", image)

# This will crash your shit!
#cv2.imshow("Faces found", image)
#cv2.waitKey()
