import cv2
import sys
from math import sin, cos, radians

camera =  cv2.VideoCapture(0)
face = cv2.CascadeClassifier(sys.argv[1])

settings = {
    'scaleFactor': 1.3, 
    'minNeighbors': 3, 
    'minSize': (50, 50), 
    'flags': cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT|cv2.cv.CV_HAAR_DO_ROUGH_SEARCH
}

def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def rotate_point(pos, img, angle):
    if angle == 0: return pos
    x = pos[0] - img.shape[1]*0.4
    y = pos[1] - img.shape[0]*0.4
    newx = x*cos(radians(angle)) + y*sin(radians(angle)) + img.shape[1]*0.4
    newy = -x*sin(radians(angle)) + y*cos(radians(angle)) + img.shape[0]*0.4
    return int(newx), int(newy), pos[2], pos[3]

framenum = 0
while True:
    ret, img = camera.read()

    if framenum % 5 == 0:
        for angle in [0, -25, 25]:
            rimg = rotate_image(img, angle)
            detected = face.detectMultiScale(rimg, **settings)
            if len(detected):
                detected = [rotate_point(detected[-1], img, -angle)]
                break
    framenum += 1
    # Display the resulting frame
    cv2.imshow('Video', img)
    cv2.waitKey(1)
    print detected

