#!/usr/bin/env python3
# coding=utf-8

# imports


import cv2
import numpy as np

import rospy

from cv_bridge import CvBridge
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image, LaserScan


class driver():

    def __init__(self):
        self.node_init = rospy.init_node('Robot_Send', anonymous=True)
        self.name = rospy.get_name().strip('/')
        self.velocity_publisher = rospy.Publisher('/' + self.name + '/cmd_vel', Twist, queue_size=10)
        self.my_team = None
        self.sub_image = rospy.Subscriber("/" + self.name + "/camera/rgb/image_raw", Image, self.Image_GET)
        self.center_x = None  # Pixel x do meu centroide
        self.chase_forward = False  # Esta variavel fica on se o robot vir outros
        self.flee = False
        self.center_x_flee = None
        self.laser_scan = rospy.Subscriber("/" + self.name + "/scan", LaserScan, self.laser)
        self.wall_R = False
        self.wall_L = False
        self.wall_F = False
        # Defining teams
        name = rospy.get_name().strip('/')
        names_red = rospy.get_param('/red_players')
        names_green = rospy.get_param('/green_players')
        names_blue = rospy.get_param('/blue_players')
        self.myteam = None
        self.prey_team_players = None
        self.hunter_team_players = None
        self.Limits_hunter = None
        self.Limits_prey = None
        self.regions = None

        if name in names_red:
            self.myteam = "red"
            self.prey_team_players = names_green
            self.hunter_team_players = names_blue
            self.Limits_hunter = [(0, 10, 0), (0, 255, 0)]  # BGR
            self.Limits_prey = [(10, 0, 0), (255, 0, 0)]
        elif name in names_green:
            self.myteam = "green"
            self.prey_team_players = names_blue
            self.hunter_team_players = names_red
            self.Limits_hunter = [(10, 0, 0), (255, 0, 0)]  # é cacado
            self.Limits_prey = [(0, 0, 10), (0, 0, 255)]  #
        elif name in names_blue:
            self.myteam = "blue"
            self.prey_team_players = names_red
            self.hunter_team_players = names_green
            self.Limits_hunter = [(0, 0, 10), (0, 0, 255)]
            self.Limits_prey = [(0, 10, 0), (0, 255, 0)]
        else:
            rospy.logerr('Something is wrong')
        print("My name is " + self.name + ". I am team " + str(self.myteam) + " huntig " + str(
            self.prey_team_players) + " and fleeing from " + str(self.hunter_team_players))

    def Image_GET(self, image):
        window_name = "Imagem do Robot" + self.name
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        bridge = CvBridge()

        cv_image = bridge.imgmsg_to_cv2(image, desired_encoding='passthrough')
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)  # convert to rgb

        # Máscara
        mask = cv2.inRange(cv_image, self.Limits_hunter[0], self.Limits_hunter[1])
        mask_to_flee = cv2.inRange(cv_image, self.Limits_prey[0], self.Limits_prey[1])
        # cv2.imshow("Hunter Mask", mask)

        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, 8, cv2.CV_32S)
        num_labelss, labelss, statss, centroidss = cv2.connectedComponentsWithStats(mask_to_flee, 8, cv2.CV_32S)
        max_areaa = 0
        labell = 0
        max_area = 0
        label = 0

        # --------------Chase----------------------------------
        for i in range(1, num_labels):
            area = stats[i][cv2.CC_STAT_AREA]
            if area > max_area:
                max_area = area
                label = i
        if not label == 0:
            center = centroids[label]
            c = (int(center[0]), int(center[1]))  # C[0] é x
            cv2.line(cv_image, (c[0] - 20, c[1]), (c[0] + 20, c[1]), (0, 0, 255), 3)
            cv2.line(cv_image, (c[0], c[1] - 20), (c[0], c[1] + 20), (0, 0, 255), 3)
            self.center_x = int(center[0])
            self.chase_forward = True
        else:
            self.center_x = None
            self.chase_forward = False

        # ------------------------FLEE-------------------------------
        for n in range(1, num_labelss):
            area = statss[n][cv2.CC_STAT_AREA]
            if area > max_areaa:
                max_areaa = area
                labell = n
        if not labell == 0:
            center = centroidss[labell]
            self.center_x_flee = int(center[0])
            self.flee = True
        else:
            self.center_x_flee = None
            self.flee = False

        # cv2.imshow(window_name, cv_image)

        # Só apanhar a parte branca -Hunt and flee
        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=4)
        img2 = np.zeros(output.shape)
        img2[output == label] = 255
        # cv2.imshow("Biggest Area", img2)

        # Passar para a funcao de chase - x centroide, variavel para andar, largura imagem
        self.chasing(self.center_x, self.chase_forward, output.shape[1], self.flee, self.center_x_flee)
        cv2.waitKey(1)

    def laser(self, msg):
        lim = 1.5
        self.regions = {
            'right': min(min(msg.ranges[245:296]), 10),
            'fright': min(min(msg.ranges[345:355]), 10),
            'front': (msg.ranges[0]),
            'fleft': min(min(msg.ranges[5:15]), 10),
            'left': min(min(msg.ranges[70:120]), 10),
        }

        if msg.ranges[0] < lim:

            self.wall_F = True

        elif msg.ranges[1] < lim or msg.ranges[15] < lim or msg.ranges[30] < lim or msg.ranges[45] < lim or msg.ranges[
            60] < lim:
            self.wall_L = True
            self.wall_R = False
        elif msg.ranges[345] < lim or msg.ranges[330] < lim or msg.ranges[315] < lim:

            self.wall_R = True
            self.wall_L = False

        else:
            self.wall_R = False
            self.wall_L = False
            self.wall_F = False

    def chasing(self, center_x, chase_forward, image_width, flee, center_x_flee):
        lim = 1.5
        vel_msg = Twist()
        wall_R = self.wall_R
        wall_L = self.wall_L
        wall_F = self.wall_F
        regions = self.regions
        # ------Only hunting----------
        if chase_forward == True and flee == False:
            vel_msg.linear.x = 1  # change constant value to change linear velocity
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0
            if center_x < image_width / 2:
                if center_x < round(0.94 * (image_width / 2)):  # 0.94 foi o valor para treinado
                    vel_msg.angular.z = 0.5
                else:
                    vel_msg.angular.z = 0.1

            if center_x > image_width / 2:
                if center_x > round(1.07 * (image_width / 2)):
                    vel_msg.angular.z = -0.5
                else:
                    vel_msg.angular.z = -0.1
            self.velocity_publisher.publish(vel_msg)
            rospy.loginfo("chase")
        # ------------Fugir------------------------------
        elif flee == True and wall_R == False and wall_L == False and wall_F == False:
            vel_msg.linear.x = 1  # change constant value to change linear velocity
            if center_x_flee < image_width / 2:
                vel_msg.angular.z = -1
            if center_x_flee > image_width / 2:
                vel_msg.angular.z = 1
            self.velocity_publisher.publish(vel_msg)
            rospy.loginfo("flee")
        # ---------------Dont' see anything-----------------------------
        elif chase_forward == False and flee == False and wall_R == False and wall_L == False and wall_F == False:
            vel_msg.linear.x = 1
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)
            rospy.loginfo("nothing")
        # ---------------Walls-----------------------------
        elif regions['front'] < lim and regions['front'] > lim / 3 and regions['fleft'] > lim / 2 and regions[
            'fright'] > lim / 2 and chase_forward == False:  # and regions['fleft'] < lim and regions['fright'] < lim

            if regions['fright'] > regions['fleft']:
                rospy.loginfo(' wall on front, right has more space')
                vel_msg.linear.x = 0.6
                vel_msg.angular.z = -1
                self.velocity_publisher.publish(vel_msg)
            else:
                vel_msg.linear.x = 0.6
                vel_msg.angular.z = 1
                self.velocity_publisher.publish(vel_msg)
                rospy.loginfo(' wall on front, left has more space')


        elif regions['front'] < lim / 4 and regions['fleft'] > lim and regions[
            'fright'] > lim and chase_forward == False:
            rospy.loginfo(' wall on front, cant wheel (go back)')
            vel_msg.linear.x = -1
            vel_msg.angular.z = -1

            self.velocity_publisher.publish(vel_msg)
        elif regions['front'] > lim and regions['fleft'] > lim and regions['right'] < lim and chase_forward == False:
            rospy.loginfo('wall on right')
            vel_msg.linear.x = 0.6
            vel_msg.angular.z = 1
            self.velocity_publisher.publish(vel_msg)
        elif regions['front'] > lim and regions['fleft'] < lim and regions['fright'] > lim and chase_forward == False:
            rospy.loginfo('wall on left')
            vel_msg.linear.x = 0.6
            vel_msg.angular.z = -1
            self.velocity_publisher.publish(vel_msg)
        elif regions['front'] < lim and regions['fleft'] > lim and regions['right'] < lim and chase_forward == False:
            rospy.loginfo('wall on  front and right')
            vel_msg.linear.x = 0.6
            vel_msg.angular.z = 1
            self.velocity_publisher.publish(vel_msg)
        elif regions['front'] < lim and regions['left'] < lim and regions['fright'] > lim and chase_forward == False:
            rospy.loginfo('wall on front and left')
            vel_msg.linear.x = 0.6
            vel_msg.angular.z = -1
            self.velocity_publisher.publish(vel_msg)
        elif regions['front'] < lim and regions['left'] < lim and regions['right'] < lim and chase_forward == False:
            rospy.loginfo('wall on  front and left and right')
            vel_msg.linear.x = 0
            vel_msg.angular.z = 1
            self.velocity_publisher.publish(vel_msg)
        elif regions['front'] > lim and regions['left'] < lim and regions['right'] < lim and chase_forward == False:
            rospy.loginfo('wall on left and right')

            vel_msg.linear.x = 0.6
            vel_msg.angular.z = 1
            self.velocity_publisher.publish(vel_msg)


def main():
    """Create object from the class TurtleBot"""
    player = driver()
    rospy.spin()


if __name__ == '__main__':
    main()