#!/usr/bin/env python

from __future__ import print_function
import cv2
from ar_markers import detect_markers

import numpy as np

import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage

bridge = CvBridge()

cur_im  = None
new_image = False

coordinates = {1: (0, 0), 2: (1, 0), 3: (0, 1), 4: (1, 1)}

def callback(data):
    global bridge, cur_im, new_image
    try:
        cur_im = bridge.imgmsg_to_cv2(data, "bgr8")
        #cur_im = bridge.compressed_imgmsg_to_cv2(data, "bgr8")
        new_image = True
    except CvBridgeError as e:
        print(e)


if __name__ == '__main__':
    global cur_im, new_image  

    rospy.init_node("arscanner_node", anonymous=False)
    #rospy.Subscriber("camera/color/image_raw/compressed", CompressedImage, callback)
    rospy.Subscriber("camera/color/image_raw", Image, callback)

    while not rospy.is_shutdown():

        if cur_im is None:
            continue
        if new_image:
            color_image = np.asanyarray(cur_im)
            frame = np.array(color_image)
            markers = detect_markers(frame)
            for marker in markers:
                    marker.highlite_marker(frame)
            cv2.imshow('Test Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            new_image = False
    cv2.destroyAllWindows()
