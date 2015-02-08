import cv2
import numpy as np
import os


def compress(filename, background_quality=10, face_quality=75, show_faces=False):
  """Compresses file while keeping the faces at a higher fidelity."""
  
  # check for/make output dir
  if not os.path.exists("output"):
    os.makedirs("output")


  cascade = cv2.CascadeClassifier("models/haarcascade_frontalface_default.xml")

  filename_compressed = "output/compressed.jpg"
  filename_fpeg = "output/fpeg.jpg"


  # load source and compressed version
  source = cv2.imread(filename)
  
  # save source with jpeg compression set to background_quality
  cv2.imwrite(filename_compressed,
              source,
              [cv2.IMWRITE_JPEG_QUALITY, background_quality])

  compressed = cv2.imread(filename_compressed)

  # find faces as rects
  faces = cascade.detectMultiScale(source, scaleFactor = 1.1,
                                   minNeighbors = 5, minSize=(30,30),
                                   flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

  print "INFO: compressor identified {} faces".format(faces.size/4)


  # move faces from source to compressed source
  for (x, y, w, h) in faces:
    compressed[y:(y + h), x:(x + w)] = source[y:(y + h), x:(x + w)]
    
    if show_faces:
      cv2.rectangle(compressed, (x, y), (x + w, y + h), (0, 255, 0), 2)

  
  cv2.imwrite(filename_fpeg,
              compressed,
              [cv2.IMWRITE_JPEG_QUALITY, face_quality])
              
  cv2.imwrite("output/source_test.jpg",
              source,
              [cv2.IMWRITE_JPEG_QUALITY, face_quality]) 
              
  print "INFO: result saved to: {}".format(filename_fpeg)            
              
  
