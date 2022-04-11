#!/usr/bin/env python
from asyncio.constants import SENDFILE_FALLBACK_READBUFFER_SIZE
from re import A
import rospy
import cv2

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from cv2 import aruco

global send_image
send_image = []

CAMERA_NAME = '/cam1'

def main():
    rospy.init_node(CAMERA_NAME[1:] + "_receiver")
    rospy.loginfo(CAMERA_NAME[1:]+'_magia_comienza')
    
    rospy.Subscriber(CAMERA_NAME,Image,findAruco)
    pub = rospy.Publisher(CAMERA_NAME+'_aruco_img',Image,queue_size=2)
    
    #pub.publish(send_image)
    rospy.spin()

def findAruco(img, draw=True):
    global send_image
    
    img = CvBridge().imgmsg_to_cv2(img,"bgr8")
    
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    arucodict = aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    arucoparam = aruco.DetectorParameters_create()
    (bbox, ids, rej) = aruco.detectMarkers(gray, arucodict, parameters=arucoparam)
    if len(bbox) > 0:
        aruco.drawDetectedMarkers(img, bbox, ids=ids)
    
    cv2.imshow('image',img)
    cv2.waitKey(10)
    
    img = CvBridge().cv2_to_imgmsg(img,desired_encoding="bgr8")
    send_image = img
        

if __name__ == '__main__':
    try:        
        main()
    except rospy.ROSInterruptException:
        pass

