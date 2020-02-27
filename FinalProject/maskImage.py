# import the necessary packages
import numpy as np
import argparse
import random
import time
import cv2
import os

def maskImage(source):
    directory = "mask-rcnn-coco"
    # load the COCO class labels our Mask R-CNN was trained on
    labelsPath = os.path.sep.join([directory,"object_detection_classes_coco.txt"])
    LABELS = open(labelsPath).read().strip().split("\n")
    colorsPath = os.path.sep.join([directory, "colors.txt"])
    COLORS = open(colorsPath).read().strip().split("\n")
    COLORS = [np.array(c.split(",")).astype("int") for c in COLORS]
    COLORS = np.array(COLORS, dtype="uint8")
    print(COLORS)
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

maskImage("images/example_01.jpg")
