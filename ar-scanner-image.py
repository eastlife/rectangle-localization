#!/usr/bin/env python

from __future__ import print_function
import cv2
from ar_markers import detect_markers
import sys

if __name__ == '__main__':
        filename = sys.argv[1]
        print('Press "q" to quit')
        frame = cv2.imread(filename)


        markers = detect_markers(frame)
        print(markers)
        for marker in markers:
                print(marker.center)
                marker.highlite_marker(frame)
        cv2.imshow('Test Frame', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
