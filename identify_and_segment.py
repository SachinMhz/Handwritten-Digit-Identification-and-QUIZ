#impoting packages
import imageio
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import os
import cv2

# load the model
from keras.models import load_model
model = load_model("test_model.h5")

#paths to images
Images_path = os.getcwd() + '\\Images\\'
non_segmented_image_path = Images_path + 'answer.jpg'
imageLocation = Images_path + 'Segmented_Images\\'

def image_segmentation():
    img = cv2.imread(non_segmented_image_path)

    #segmenting the image with counter from openCV
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchies = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("Number of contours = " + str(len(contours)))
    print("Format of hieraechy = [[Next, Previous, First_Child, Parent]]")

    cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
    #cv2.imshow("img",img)

    #deleting the images already in the directory
    imageLocation = Images_path + 'Segmented_Images\\'
    for file in os.listdir(imageLocation):
            os.remove(imageLocation+file) 

    #sorted_ctrs = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0]  )

    #removing unnecessary contours        
    #hierarchy[0,i,3] #hierarchy=[[Next, Previous, First_Child, Parent]]
    contours_list = []

    for contour,hierarchy in zip(contours,hierarchies[0]):
        #print(hierarchy)
        if hierarchy[3] == 0 or cv2.contourArea(contour) > 1000 and hierarchy[2] != -1 :
        #if cv2.contourArea(contour) > 100 or hierarchy[3] == 0:
            contours_list.append(contour)
    print('Number of countours after filtering = ',len(contours_list[1:]) ) 
    #sorting contours
    contours_list = sorted(contours_list, key=lambda ctr: cv2.boundingRect(ctr)[0]  )
    print('Number of countours after filtering = ',len(contours_list[1:]) )        

    #saving and naming Contours in images
    for i,contour in enumerate(contours_list[1:]):
            (x, y, w, h) = cv2.boundingRect(contour)
            
            #padding images and cropping
            p = 10  
            x,y,w,h = x-p,y-p,w+p+10,h+p+10
            roi = img[y:y+h, x:x+w] #roi = region of image
            
            #saving the image
            name = imageLocation + 'roi'+str(i)+'.png'
            cv2.imwrite(name, roi)
            
            #saving image with aspect-ratio
            img2 = Image.open(name)
            w1,h1 = img2.size
            background = Image.open(Images_path + 'number_background.png')
            w2,h2 = background.size
            pasteLocation = int(w2/2) - int(w1/2), int(h2/2) - int(h1/2)
            background.paste(img2,pasteLocation)
            background.save(name,"PNG")

def image_identification():
    predicted_number = []
    prediction_accuracy = 0
    No_of_images = 0
    for image in os.listdir(imageLocation):
        No_of_images += 1
        im = imageio.imread(imageLocation+image)
        #getting image
        #im = imageio.imread(imageLocation+'roi2.png')
        dim = (28,28)

        #preprocessing image
        im = cv2.resize(im, dim, interpolation = cv2.INTER_AREA)
        #plt.imshow(im)
        gray = np.dot(im[...,:3], [0.299, 0.587, 0.114])
        gray = gray.reshape(1, 28, 28, 1)
        gray = 255-gray
        gray = gray/255

        # predict digit
        prediction = model.predict(gray)
        predicted_number.append(str(prediction.argmax()))
        prediction_accuracy += max(prediction[0])
    answer = ''.join(predicted_number)
    accuracy = 0
    if No_of_images != 0:
        accuracy = prediction_accuracy/No_of_images
    #print('Predicted Number =', answer)
    return answer , accuracy