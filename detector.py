import rospy
import numpy as np
import cv2
import time

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header

# red = [0, 0, 255]
# blue = [255, 0, 0]
# green = [0, 255, 0]
# yellow = [0, 255, 255]
# white = [0, 0 ,0]
# black = [255, 255, 255]


class DetermineColor:
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.callback)
        self.color_pub = rospy.Publisher('/rotate_cmd', Header, queue_size=10)
        self.bridge = CvBridge()
        self.count = 0

    def callback(self, data):
        try:
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            msg = Header()
            msg = data.header
            msg.frame_id = '0'  # default: STOp      
            cv2.imshow('rgb_Image', image)
            cv2.imshow('hsv_image', hsv)
            
            red_lower, red_upper = (0, 0, 100), (85, 120, 255)
            blue_lower, blue_upper = (80, 30, 30), (115, 255, 255)
            green_lower, green_upper = (40, 100, 0), (80, 255, 255)
            yellow_lower, yellow_upper = (20, 100, 100), (40, 255, 255)
            white_lower, white_upper = (200, 200, 200), (255, 255, 255)
            
            
            
            red_part = cv2.inRange(image, red_lower, red_upper)
            blue_part = cv2.inRange(hsv, blue_lower, blue_upper)
            green_part = cv2.inRange(hsv, green_lower, green_upper)
            yellow_part = cv2.inRange(hsv, yellow_lower, yellow_upper)
            white_part = cv2.inRange(image, white_lower, white_upper)
            

            red_picture = cv2.bitwise_and(image, image, mask= red_part)
            blue_picture = cv2.bitwise_and(image, image, mask=blue_part)
            green_picture = cv2.bitwise_and(image, image, mask = green_part)
            yellow_picture = cv2.bitwise_and(image, image, mask = yellow_part)
            white_picture = cv2.bitwise_and(image, image, mask = white_part)
            


            added = red_picture +  blue_picture + green_picture + yellow_picture + white_picture

            cv2.imshow('result', added)
            cv2.imshow('red', red_picture)
            cv2.imshow('blue', blue_picture)
            cv2.imshow('green', green_picture)
            cv2.imshow('yellow', yellow_picture)
            cv2.imshow('white', white_picture)

            red_pixels = cv2.countNonZero(red_part)
            blue_pixels = cv2.countNonZero(blue_part)
            yellow_pixels = cv2.countNonZero(yellow_part)
            green_pixels = cv2.countNonZero(green_part)
            white_pixels = cv2.countNonZero(white_part)
            print(f'빨강 : {red_pixels}, 파랑 : {blue_pixels}, 노랑 : {yellow_pixels}, 초록 : {green_pixels}, 하양 : {white_pixels}')
            
            #print(red_pixels, blue_pixels, yellow_mask, green_mask)
            
            if ((red_pixels+30>=blue_pixels)&(red_pixels+30>=green_pixels)&(red_pixels+30>=yellow_pixels)&(red_pixels+30>=white_pixels)):
            	print("red!")
            	msg.frame_id = '-1'
            	#print(msg.frame_id)
            elif((blue_pixels+30>=red_pixels)&(blue_pixels+30>=green_pixels)&(blue_pixels+30>=yellow_pixels)&(blue_pixels+30>=white_pixels)):
            	print("blue!")
            	msg.frame_id = '+1'
            	#print(msg.frame_id)
            else: 
            	print("unknown!")
            	msg.frame_id = '0'
            	#print(msg.frame_id)
            cv2.waitKey(1)
            self.color_pub.publish(msg)
            
        except CvBridgeError as e:
        	print(e)


    def rospy_shutdown(self, signal, frame):
        rospy.signal_shutdown("shut down")
        sys.exit(0)

if __name__ == '__main__':
    detector = DetermineColor()
    rospy.init_node('CompressedImages1', anonymous=False)
    rospy.spin()
