# Source: String, The source of the image (user gives this to us)
# Color dictionary: Int truple, Takes a category as a key and returns an RGB color (int truple, each having range 0-255)
# price range: Int Tuple, Value range for objects we will display
# Categories: String list, List of categories of objects we will mask

# three views for the image- one of uniform opacity where color is the category and a text annotation gives the type
# the other is a value view in which all the masks are yellow but opacity details the value of the object.
# last is weight view in which all the masks are red but opacity details the weight of the object
# color_dictionary is a dictionary with string keys and int truple values
# need a value_dictionary with string keys and int values


# import the necessary packages
import numpy as np
import argparse
import random
import time
import cv2
import os

def maskImage(source,color_dictionary):
    directory = "mask-rcnn-coco"
    # load the COCO class labels our Mask R-CNN was trained on
    labelsPath = os.path.sep.join([directory,"object_detection_classes_coco.txt"])
    LABELS = open(labelsPath).read().strip().split("\n")
    colorsPath = os.path.sep.join([directory, "colors.txt"])
    #COLORS = open(colorsPath).read().strip().split("\n")
    #COLORS = [np.array(c.split(",")).astype("int") for c in COLORS]
    #COLORS = np.array(COLORS, dtype="uint8")
    #print(COLORS)
    # derive the paths to the Mask R-CNN weights and model configuration
    weightsPath = os.path.sep.join([directory,"frozen_inference_graph.pb"])
    configPath = os.path.sep.join([directory,
		"mask_rcnn_inception_v2_coco_2018_01_28.pbtxt"])
    # load our Mask R-CNN trained on the COCO dataset (90 classes)
    # from disk
    print("[INFO] loading Mask R-CNN from disk...")
    net = cv2.dnn.readNetFromTensorflow(weightsPath, configPath)
    # load our input image and grab its spatial dimensions
    image = cv2.imread(source)
    (H, W) = image.shape[:2]
    # construct a blob from the input image and then perform a forward
    # pass of the Mask R-CNN, giving us (1) the bounding box  coordinates
    # of the objects in the image along with (2) the pixel-wise segmentation
    # for each specific object
    blob = cv2.dnn.blobFromImage(image, swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    (boxes, masks) = net.forward(["detection_out_final", "detection_masks"])
    end = time.time()
    # show timing information and volume information on Mask R-CNN
    #print("[INFO] Mask R-CNN took {:.6f} seconds".format(end - start))
	#print("[INFO] boxes shape: {}".format(boxes.shape))
	#print("[INFO] masks shape: {}".format(masks.shape))
    # clone our original image so we can draw on it
    # POI: Clone is our image. We should be saving it after we do the for loop
    clone = image.copy()
    #visualize = 0
	#way to save clone: clone = clone.save(filename)
    # loop over the number of detected objects
    for i in range(0, boxes.shape[2]):
        # extract the class ID of the detection along with the confidence
        # (i.e., probability) associated with the prediction
        classID = int(boxes[0, 0, i, 1])
        confidence = boxes[0, 0, i, 2]
        # filter out weak predictions by ensuring the detected probability
        # is greater than the minimum probability
        if confidence > 0.5:

            # scale the bounding box coordinates back relative to the
            # size of the image and then compute the width and the height
            # of the bounding box
            box = boxes[0, 0, i, 3:7] * np.array([W, H, W, H])
            (startX, startY, endX, endY) = box.astype("int")
            boxW = endX - startX
            boxH = endY - startY
            # extract the pixel-wise segmentation for the object, resize
            # the mask such that it's the same dimensions of the bounding
            # box, and then finally threshold to create a *binary* mask
            mask = masks[i, classID]
            mask = cv2.resize(mask, (boxW, boxH),interpolation=cv2.INTER_NEAREST)
            mask = (mask > 0.3)
            # extract the ROIs of the image
            roi = (clone[startY:endY, startX:endX])

            # in the boolean mask array as our slice condition
            roi = roi[mask]
            # randomly select a color that will be used to visualize this
            # particular instance segmentation then create a transparent
            # overlay by blending the randomly selected color with the ROI
            ## TODO: get data from radio button choice and check for view type for color and opacity

            color = np.array(color_dictionary[LABELS[classID]])
            '''POI: This is how opacity is defined, with the right flow being high opacity and the left
    		being low. THey should add to 1.0'''
            blended = ((0.4 * color) + (0.6 * roi)).astype("uint8")
            # store the blended ROI in the original image
            clone[startY:endY, startX:endX][mask] = blended

            # draw the bounding box of the instance on the image
            color = [int(c) for c in color]
            cv2.rectangle(clone, (startX, startY), (endX, endY), color, 2)

            # draw the predicted label and associated probability of the
            # instance segmentation on the image
            text = "{}: {:.4f}".format(LABELS[classID], confidence)
            cv2.putText(clone, text, (startX, startY - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # show the output image
    cv2.imshow("Output", clone)
    cv2.waitKey(0)

cd = {"car":(140,33,255)}
maskImage("images/example_01.jpg",cd)
