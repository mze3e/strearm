'''
Sources:
http://opencv2.willowgarage.com/documentation/python/cookbook.html
http://www.lucaamore.com/?p=638
'''

#Python 2.7.2
#Opencv2 2.4.2
#PIL 1.1.7
import numpy
import cv2 #Opencv2
from PIL import Image #Image from PIL
import glob
import os
import copy

print(cv2.__version__)
RED = (0, 0, 255)
scaleFactor = 1.1
minNeighbors = 5
minSize = (30, 30)


def DetectFace(image, faceCascade, returnImage=False):
    # This function takes a grey scale cv2 image and finds
    # the patterns defined in the haarcascade function
    # modified from: http://www.lucaamore.com/?p=638

    #variables    
    min_size = (20,20)
    haar_scale = 1.1
    min_neighbors = 3
    haar_flags = 0

    # Equalize the histogram
    cv2.EqualizeHist(image, image)

    # Detect the faces
    faces = cv2.HaarDetectObjects(
            image, faceCascade, cv2.CreateMemStorage(0),
            haar_scale, min_neighbors, haar_flags, min_size
        )

    # If faces are found
    if faces and returnImage:
        for ((x, y, w, h), n) in faces:
            # Convert bounding box to two Cv2Points
            pt1 = (int(x), int(y))
            pt2 = (int(x + w), int(y + h))
            cv2.Rectangle(image, pt1, pt2, cv2.RGB(255, 0, 0), 5, 8, 0)

    if returnImage:
        return image
    else:
        return faces


def cv2pil(cv2_im):
    # Convert the cv2 image to a PIL image
    return Image.fromstring("L", cv2.GetSize(cv2_im), cv2_im.tostring())

def imgCrop(image, cropBox, boxScale=1):
    # Crop a PIL image with the provided box [x(left), y(upper), w(width), h(height)]

    # Calculate scale factors
    xDelta=max(cropBox[2]*(boxScale-1),0)
    yDelta=max(cropBox[3]*(boxScale-1),0)

    # Convert cv2 box to PIL box [left, upper, right, lower]
    PIL_box=[cropBox[0]-xDelta, cropBox[1]-yDelta, cropBox[0]+cropBox[2]+xDelta, cropBox[1]+cropBox[3]+yDelta]

    return image.crop(PIL_box)


def detect(gray, img):
    rects = face_detector.detectMultiScale(gray, 
        scaleFactor=scaleFactor,
        minNeighbors=minNeighbors, 
        minSize=minSize, 
        flags=cv2.CASCADE_SCALE_IMAGE)

    print(f'found {len(rects)} face(s)')

    img = img.copy()
    for rect in rects:
        cv2.rectangle(img, rect, RED, 2)
    cv2.imshow('window', img)

def trackbar(x):
    global minSize, minNeighbors, scaleFactor
    i = cv2.getTrackbarPos('size','window')
    d = (24, 30, 60, 120)[i]
    minSize = (d, d)
    
    n = cv2.getTrackbarPos('neighbors','window') + 1
    minNeighbors = n

    i = cv2.getTrackbarPos('scale','window')
    s = (1.05, 1.1, 1.4, 2)[i]
    scaleFactor
    
    text = f'minNeighbors={n}, minSize={d}, scaleFactor={s}'
    cv2.displayOverlay('window', text)
    detect()


def faceCrop(imagePattern,boxScale=1):
    # Select one of the haarcascade files:
    #   haarcascade_frontalface_alt.xml  <-- Best one?
    #   haarcascade_frontalface_alt2.xml
    #   haarcascade_frontalface_alt_tree.xml
    #   haarcascade_frontalface_default.xml
    #   haarcascade_profileface.xml
    faceCascade = cv2.Load('haarcascade_frontalface_alt.xml')

    imgList=glob.glob(imagePattern)
    if len(imgList)<=0:
        print('No Images Found')
        return

    for img in imgList:
        pil_im=Image.open(img)
        cv2_im=pil2cv2Grey(pil_im)
        faces=DetectFace(cv2_im,faceCascade)
        if faces:
            n=1
            for face in faces:
                croppedImage=imgCrop(pil_im, face[0],boxScale=boxScale)
                fname,ext=os.path.splitext(img)
                croppedImage.save(fname+'_crop'+str(n)+ext)
                n+=1
        else:
            print('No faces found:', img)

def test(imageFilePath):

    img0 = cv2.imread(imageFilePath)
    img = img0.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    detect(gray, img)

    cv2.createTrackbar('neighbors', 'window', 0, 10, trackbar)
    cv2.createTrackbar('size', 'window', 0, 3, trackbar)
    cv2.createTrackbar('scale', 'window', 0, 3, trackbar)
    cv2.waitKey(0)

    """    
    img=cv2.imread(imageFilePath)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    # Select one of the haarcascade files:
    #   haarcascade_frontalface_alt.xml  <-- Best one?
    #   haarcascade_frontalface_alt2.xml
    #   haarcascade_frontalface_alt_tree.xml
    #   haarcascade_frontalface_default.xml
    #   haarcascade_profileface.xml
    
    classifier_list = [ 'haarcascade_frontalface_alt.xml',  #<-- Best iu8u8+9+one
                        'haarcascade_frontalface_alt2.xml',
                        'haarcascade_frontalface_alt_tree.xml',
                        'haarcascade_frontalface_default.xml',
                        'haarcascade_profileface.xml'
    ]    
    cv2.imshow('Original image', img)
    cv2.imshow('Gray image', gray_img)

    for classifier in classifier_list:
    
        img_copy = copy.copy(img)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + classifier)
        faces=face_cascade.detectMultiScale(gray_img,1.1,4)
)

        EXTRA_SPACE = .3

        for (x, y, w, h) in faces:
            extra_pixels = round(w*EXTRA_SPACE if w*EXTRA_SPACE > h*EXTRA_SPACE else h*EXTRA_SPACE)
            x1=(x-extra_pixels)
            y1=(y-extra_pixels)
            x2=(x+w+extra_pixels*2)
            y2=(y+h+extra_pixels*2)
            
            cv2.rectangle(img_copy, (x1, y1), (x2, y2), (255, 0, 0), 2)
            # Cropping an image
            cropped_image = img[y1:y2, x1:x2]

        cv2.imshow(classifier, img_copy)
        
        # Display cropped image
        cv2.imshow("cropped with "+classifier, cropped_image)
        
        # Save the cropped image
        #cv2.imwrite("Cropped Image.jpg", cropped_image)

        #cv2.imshow('Face Image', face_img)
        #img.save('test.png')
        cv2.waitKey(0)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """

# Test the algorithm on an image
test('assets/images/photos/000000.jpg')

# Crop all jpegs in a folder. Note: the code uses glob which follows unix shell rules.
# Use the boxScale to scale the cropping area. 1=opencv2 box, 2=2x the width and height
#faceCrop('/Users/mz/development/strearm/assets/images/photos/*.jpg',boxScale=1)