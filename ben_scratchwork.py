import cv2
import copy

#model = "models/haarcascades/haarcascade_frontalface_default.xml"
pic = "images/friends.jpg"
model = "models/haarcascade_frontalface_default.xml"

#make sure model exists
f = open(model)
f.close()

faceCascade = cv2.CascadeClassifier(model)

image = cv2.flip(cv2.imread(pic), 1)
#image = cv2.imread(pic)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# detectMultiScale is a general function that detects objects
# scaleFactor of 1.1 -> at each iteration, the scale for faces increases 10%
# flags: 0 means no change in oinput image. CV_HARR_DO_CANNY_PRUNING skips flat
faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.01,
                                     minNeighbors = 4, minSize=(34, 34),
                                     flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

#cv2.cv.HAAR_DO_CANNY_PRUNING
#cv2.cv.CV_HAAR_SCALE_IMAGE

i = 0
for (x, y, w, h) in faces:
  i += 1
  cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
  face_img = image[y:(y + h), x:(x + w)]
  gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
  gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
  image[y:(y + h), x:(x + w)] = gray_bgr
  #cv2.imwrite("face" + str(i) + ".jpg", face_img)

print str(len(faces)) + " faces found"

cv2.imwrite("faces.jpg", image)


# This will crash your shit!
#cv2.imshow("Faces found", image)
#cv2.waitKey()
