#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist

def callback(msg):
    rospy.loginfo(rospy.get_caller_id())
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('chatter', string, callback)
    rospy.spin()
#topic name is /turtle1/cmd_vel, topic type is Twist


if __name__ == '__main__':
    listener()

