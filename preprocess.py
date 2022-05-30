import cv2
import numpy as np


def preprocess(img):
  #print(img)
  #img=cv2.imread(img)
  img=img[60:140, :, :]
  img=cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
  img = cv2.GaussianBlur(img, (3,3), 0)
  img = cv2.resize(img, (200,66))
  img = np.expand_dims(img, axis=0)
  img = img/255.0
  return img