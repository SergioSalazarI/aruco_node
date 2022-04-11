#!/usr/bin/env python
import rospy
import cv2
import sys

from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import Float32

#from utils import image_filters as imf

global send_image

# CONSTANTS PARAMETERS FOR CAMERAS BELOW
CAMERA_NAME = '/cam1'
CAMERA_INDEX = 0

if len(sys.argv) > 1:
    print(sys.argv)
    CAMERA_NAME = sys.argv[1]
    CAMERA_INDEX = int(sys.argv[2])

send_image = 1


def main():
    try:
        pub = rospy.Publisher(CAMERA_NAME, Image, queue_size=2)
        #sub = rospy.Subscriber(CAMERA_NAME + '_signal', Float32, receive_signal)
        cap = cv2.VideoCapture(CAMERA_INDEX)
        #img = cv2.imread("/home/sergio/Imágenes/Cámara web/imagen_prueba.jpg")
        bridge = CvBridge()
        rospy.loginfo("About to start stream. Waiting for signal")
    except Exception as e:
        rospy.logwarn(e)

    while (not rospy.is_shutdown()):
        try:
            ret, frame = cap.read()
            
            #message = input("[INFO] Enter your filter  ")
            #send_image = int(message)
            rospy.loginfo("Aruco image Stream for {} opened".format(CAMERA_NAME))

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                raise KeyboardInterrupt

            #if send_image != 0:
            #    imgMsg = bridge.cv2_to_imgmsg(frame, "passthrough")
            #    pub.publish(imgMsg)
            #    rospy.Rate(100).sleep() # img instead of frame
            imagen = bridge.cv2_to_imgmsg(frame,encoding="bgr8")
            pub.publish(imagen)
            rospy.loginfo('imagen_publicada')
            rospy.Rate(100).sleep()
                
        except KeyboardInterrupt as ki:
            cap.release()
            cv2.destroyAllWindows()
            break
        except TypeError as te:
            cap.release()
            cv2.destroyAllWindows()
            rospy.logerr(te.message)
            rospy.logerr("Cannot read frame from index {}".format(CAMERA_INDEX))
            rospy.logerr("Camera connection closed")
            return
    rospy.loginfo("Manual shutdown, closing stream")

def receive_signal(data):
    global send_image
    send_image = data.data
    if send_image == 0:
        rospy.loginfo("Image Stream for {} closed".format(CAMERA_NAME))
    elif send_image == 1:
        rospy.loginfo("Raw image Stream for {} opened".format(CAMERA_NAME))
    elif send_image == 2:
        rospy.loginfo("Gray image Stream for {} opened".format(CAMERA_NAME))
    elif send_image == 3:
        rospy.loginfo("Threshold image Stream for {} opened".format(CAMERA_NAME))
    elif send_image == 4:
        rospy.loginfo("Aruco image Stream for {} opened".format(CAMERA_NAME))

if __name__ == '__main__':
    rospy.init_node(CAMERA_NAME[1:] + "_streamer")
    main()