#!/usr/bin/env python

from __future__ import print_function
import cv2
import numpy as np


def project_point(point, M):
    # formula from https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#warpperspective
    x_trans = (M[0][0] * point[0] + M[0][1] * point[1] + M[0][2]) / (M[2][0] * point[0] + M[2][1]  * point[1] + M[2][2])
    y_trans = (M[1][0] * point[0] + M[1][1] * point[1] + M[1][2]) / (M[2][0] * point[0] + M[2][1]  * point[1] + M[2][2])
    return (x_trans, y_trans)


def rectify(h):
    h = h.reshape((4,2))
    hnew = np.zeros((4,2),dtype = np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h,axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew

# orig and dest are both 4x2 matrix, which are the coordinates of four corners of the rectangle
# default dest is an 800x800 square
def map_matrix(orig, dest=None):
    orig = rectify(orig)
    if dest is None:
        dest = np.float32([[0,0],[800,0],[800,800],[0,800]])

    M = cv2.getPerspectiveTransform(orig, dest)

    return M

def mapping(point, orig, dest=None):
    M = map_matrix(orig, dest)
    point_dest = project_point(point, M)
    return point_dest

