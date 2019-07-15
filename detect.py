#!/usr/bin/env python

from __future__ import print_function
import cv2
from ar_markers import detect_markers
import sys

def detect_corners(frame):
    corners = {}
    is_valid = False
    corner_list = []
    markers = detect_markers(frame)
    for marker in markers:
        if marker.id > 0 and marker.id <= 4:
            corners[marker.id] = marker.center
        print(markers)
        marker.highlite_marker(frame)
    if len(corners) == 4:
        is_valid = True
        corner_list = [corners[1], corners[2], corners[3], corners[4]]

    return is_valid, corner_list

'''
Corners are ordered in the following index in the return list:
-------------->x
|  0       1
|   --------
|   |      |
|   |      |
|   --------
|  2       3
|
\/
y
'''
def reorder_corners(corner_list):
    if len(corner_list) != 4:
        return None

    order_dict = {}
    corner_list.sort()
    corner_sort_by_x = list(corner_list)
    corner_list.sort(key=lambda x: x[1])
    corner_sort_by_y = list(corner_list)

    corner = corner_sort_by_x[0]
    index = corner_sort_by_y.index(corner)
    if index <= 1:
        order_dict[0] = corner
        order_dict[3] = corner_sort_by_x[1]
    else:
        order_dict[3] = corner
        order_dict[0] = corner_sort_by_x[1]
    
    corner = corner_sort_by_x[2]
    index = corner_sort_by_y.index(corner)
    if index <= 1:
        order_dict[1] = corner
        order_dict[2] = corner_sort_by_x[3]
    else:
        order_dict[2] = corner
        order_dict[1] = corner_sort_by_x[3]

    result = []
    for i in range(4):
        result.append(order_dict[i])
    return result

if __name__ == '__main__':
        filename = sys.argv[1]
        print('Press "q" to quit')
        frame = cv2.imread(filename)

        is_valid, corner_list = detect_corners(frame)
        print(is_valid)
        print(corner_list)
        corner_list = reorder_corners(corner_list)
        print(corner_list)
        cv2.imshow('Test Frame', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
