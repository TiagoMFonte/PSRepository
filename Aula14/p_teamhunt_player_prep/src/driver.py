#!/usr/bin/env python3
import math
import rospy
import copy
import tf2_ros
from geometry_msgs.msg import Twist, PoseStamped
import tf2_geometry_msgs

class Driver():
    def __init__(self):
        self.publisher_command = rospy.Publisher('p_teamhunt/cmd_vel', Twist, queue_size=1)

        self.tf_buffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tf_buffer)

        self.timer = rospy.Timer(rospy.Duration(0.1), self.sendCommandCallback)

        self.goal_subscriber = rospy.Subscriber('/move_base_simple/goal', PoseStamped, self.goalReceivedCallback)
        self.goal = PoseStamped()
        self.goal_active = False

        self.angle = 0
        self.speed = 0
    def goalReceivedCallback(self, msg):
        # TODO verify if goal is on odom frame
        try:
            self.pose = self.tf_buffer.transform(msg, 'p_teamhunt/odom', rospy.Duration(1))
            goal_active = True
            rospy.logwarn('Setting new goal')
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            goal_active = False
            rospy.logerr('Could not transform to odom frame. Will ignore this goal.')

        #print('Received new goal')
        #self.goal = copy.copy(msg)  #store goal
        #self.goal = copy.copy(msg)  #store goal
        #self.goal_active = True


    def driveStraight(self, minimum_speed=0.1, maximum_speed=0.5):
        goal_copy = copy.deepcopy(self.goal)
        goal_copy.header.stamp = rospy.Time.now()

        print('Transforming pose')
        goal_in_base_link = self.tf_buffer.transform(goal_copy, 'p_teamhunt/base_footprint', rospy.Duration(1))
        print('Pose transformed')

        x = goal_in_base_link.pose.position.x
        y = goal_in_base_link.pose.position.y

        self.angle = math.atan2(y, x)

        distance_to_goal = math.sqrt(x**2 + y**2)
        self.speed = max(minimum_speed, 0.5 * distance_to_goal)    # TODO vary speed according to distance to goal
        self.speed = min(maximum_speed, self.speed)

    def sendCommandCallback(self, event):
        print('Sending twist command')
        if not self.goal_active:
            self.angle = 0
            self.speed = 0
        else:
            self.driveStraight()
        twist = Twist()
        twist.linear.x = self.speed
        twist.angular.z = self.angle
        self.publisher_command.publish(twist)

def main():
    rospy.init_node('p_teamhunt_driver', anonymous=False)
    driver = Driver()

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass