#!/usr/bin/env python3
import rospy

from geometry_msgs.msg import Twist

def main():
    rospy.init_node('p_tfonte_driver', anonymous=False)
    publisher = rospy.Publisher('p_tfonte/cmd_vel', Twist, queue_size=1)
    rate = rospy.Rate(10)
    rospy.spin()
    while not rospy.is_shutdown():
        twist = Twist()
        twist.linear.x = 0.1
        twist.angular.z = -1

        publisher.publish(twist)
        rate.sleep()
if __name__ == '__main__':
        main()
