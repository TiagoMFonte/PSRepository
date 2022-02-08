#!/usr/bin/env python3


import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image, LaserScan
from utilitario import configurarEquipa, configurarEstrategia

import time
import copy
import math
import rospy
import tf2_ros
import numpy as np
from geometry_msgs.msg import Twist, PoseStamped
import tf2_geometry_msgs  # **Do not use geometry_msgs. Use this instead for PoseStamped

debugmode = True
equipa = []
estrategia = []
resolucaox = 1280
viramuito = 0.7
virapouco = 0.1
vira = 0.3
lowergreen = np.array([0, 90, 0])
uppergreen = np.array([40, 256, 40])
lowerred = np.array([0, 0, 90])
upperred = np.array([40, 40, 256])
lowerblue = np.array([90, 0, 0])
upperblue = np.array([256, 40, 40])

class Driver:

    def __init__(self):
        self.goal = PoseStamped()
        # 0 parado, 1 goal, 2 procura, 3 caça, 4 foge
        self.goal_active = 0
        self.last_goal_active = 0
        self.estrategia = 0
        self.encontra = 0
        self.equipa = ''
        self.tempoturn = 0
        self.imagesize = 0

        self.last_angle = 0
        self.angle = 0
        self.speed = 0

        self.name = rospy.get_name()
        self.name = self.name.strip('/')  # remove initial /
        # print('My player name is ' + self.name)

        self.publisher_command = rospy.Publisher('/' + self.name + '/cmd_vel', Twist, queue_size=1)
        # self.publisher_command = rospy.Publisher('/p_bpereira/cmd_vel', Twist, queue_size=1)

        self.tf_buffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tf_buffer)

        self.timer = rospy.Timer(rospy.Duration(0.1), self.sendCommandCallback)

        self.goal_subscriber = rospy.Subscriber('/move_base_simple/goal', PoseStamped, self.goalReceivedCallback)

    def action(self):
       # print('action image_subscriber')
        self.image_subscriber = rospy.Subscriber("/" + self.name + "/camera/rgb/image_raw", Image, self.goalImageCallback)

        self.laser_scan = rospy.Subscriber("/" + self.name + "/scan", LaserScan, self.obstacle)

        rospy.spin()
    def goalImageCallback(self, msg):
     # if debugmode:
        #     print('goalImageCallback  self.equipa' + self.equipa + '  EStrategia:' + str(self.estrategia))

        my_team = self.equipa

     #   print('action goalImageCallback') estrategia

        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")  # "passthrough" ) #

        _, w, _ = cv_image.shape
        #print('width:  ', w)
        self.imagesize = w

        # mascaras que vao detectar apresas ou os caçadores
        green_mask = cv2.inRange(cv_image, lowergreen, uppergreen)
        red_mask = cv2.inRange(cv_image, lowerred, upperred)
        blue_mask = cv2.inRange(cv_image, lowerblue, upperblue)
     #TODO:  alterar a atribuição dos ifs de acordo com a variavel equipa
        if my_team == 'blue':
            presa_mask = red_mask
            cacador_mask = green_mask
        elif my_team == 'red':
            presa_mask = green_mask
            cacador_mask = blue_mask
        elif my_team == 'green':
            presa_mask = blue_mask
            cacador_mask = red_mask


     # TODO: procedimento
    #     1 - se nao vires nada andas à volta
    #     2 - ves uma presa atacas
    #     3 - ves um cacador foges, aqui temos um problema porque quando está a fugir nao ve nada, tem que estar num
    # estado de fuga, nunca sai deste estado? se lhe passar um presa à frente vai atras dela? depende do numero de pontos?
    # curvas a 90º antes de bater na parede? velocidades? sempre a topo ee fica todo descontrolado, pode ter vantagens ou desvantagens.
     # TODO: procedimento

        if self.estrategia != 2:
            cx = 0
            contoursm, _ = cv2.findContours(presa_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contoursmi in contoursm:
                self.encontra = 1
                M = cv2.moments(contoursmi)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])

                    self.drivetoKill(cx, cy, 1)
                    if debugmode:
                        cv2.putText(cv_image, "presa", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
               # break

            # não encontra a presa vai parar
            # TODO: vai rodar à procura dela
            # TODO: se o caçador for maior deve estar mais perto, fugir?????

            if cx == 0:
                self.drivetoKill(-1, -1, 0)

        # está na altura de fugir
        # MODO DE FUGITIVO
        if self.estrategia == 2:

            self.goal_active = 4
            cx = 0
            contoursm, _ = cv2.findContours(cacador_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contoursmi in contoursm:
                self.encontra = 1
                M = cv2.moments(contoursmi)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])

                    self.driveforlife(cx, cy)
                    if debugmode:
                        cv2.putText(cv_image, "cacador", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
               # break
            if cx == 0:
                self.driveforlife(-1, -1)

        if debugmode:
            cv2.imshow("red1", cv_image)
            cv2.waitKey(1)

    def driveforlife(self, x, y, minumum_speed=0.3, maximum_speed=0.8):

        if ((x > 0) and (x < self.imagesize)):
            if (x < (self.imagesize/2)):
                self.angle = -8 * viramuito
                self.speed = 0
                self.tempoturn = time.time()
            # TODO: VIRAR pouco pu nao virar quando está no centro da imagem
            else:
                self.angle = 8 * viramuito
                self.speed = 0
                self.tempoturn = time.time()
        else:
            alo = time.time() - self.tempoturn
            # print("tempo::::" + str(alo) )
            if ((time.time() - self.tempoturn) < 3):
                self.speed = minumum_speed
                self.angle = 0
            elif ((time.time() - self.tempoturn) < 5):
                self.angle = 0
                self.speed = 1.2 * minumum_speed
            else:
                self.angle = 0
                self.tempoturn = 0
                self.speed = maximum_speed

        if (self.encontra == 0):
            self.speed = 0
            self.angle = 2 * viramuito

        if debugmode:
            print(
                "driveforlife x:" + str(x) + " y:" + str(y) + "  self.angle:" + str(self.angle) + " self.speed:" + str(
                    self.speed) + " cacador:" + str(self.encontra))

    def drivetoKill(self, x, y, op, minumum_speed=0.3, maximum_speed=1.0 ):

        temp = (self.imagesize/2)

        if op == 1:
            if ((x > 0) and (x < temp)):
                if (x < (int(temp*0.6))):
                    self.angle = viramuito
                    self.speed = minumum_speed
                elif (x < (int(temp*0.9))):
                    self.angle = vira
                    self.speed = 0.8*maximum_speed
                else:
                    self.angle = virapouco
                    self.speed = 1.3 * maximum_speed
            # TODO: VIRAR pouco pu nao virar quando está no centro da imagem
            elif ((x > temp ) ):
                if (x < (int(temp*1.1))):
                    self.angle = -1*virapouco
                    self.speed = 1.3 * maximum_speed
                elif x < (int(temp*1.3)):
                    self.angle = -1*vira
                    self.speed = 0.8*maximum_speed
                else:
                    self.angle = -1*viramuito
                    self.speed = minumum_speed

            self.last_angle = self.angle
        else:
            if (self.encontra == 0):
                self.angle = viramuito
                self.speed = minumum_speed
            else:
                self.speed = minumum_speed
                self.angle = self.last_angle

        if debugmode:
            print("drivetokill x:" + str(x) + "  y:" + str(y)    + " self.angle:" + str(self.angle )+ " self.speed:" + str(self.speed ))

        # distance_to_goal = math.sqrt(x ** 2 + y ** 2)
        # self.speed = max(minumum_speed, 0.3 * distance_to_goal)  # limit minimum speed
        # self.speed = min(maximum_speed, self.speed)  # limit maximum speed

        self.goal_active = 3
        #self.goal_active = 0

    def obstacle(self, msg, minumum_speed=0.3, maximum_speed=1.0):
        lim = 0.8

        if msg.ranges[0] < lim and msg.ranges[15] < lim and msg.ranges[345] < lim:
            self.speed = 0
            self.angle = viramuito
        else:
            if (self.encontra == 0):
                self.angle = viramuito
                self.speed = minumum_speed
            else:
                self.speed = minumum_speed
                self.angle = self.last_angle




    def goalReceivedCallback(self, msg):
        # TODO verify is goal is on odom frame
        print('Received new goal on frame id' + msg.header.frame_id)

        target_frame = self.name + '/odom'

        try:
            self.goal = self.tf_buffer.transform(msg, target_frame, rospy.Duration(1))
            self.goal_active = 1
            rospy.logwarn('Setting new goal')
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            self.goal_active = 0
            rospy.logerr('Could not transform goal from ' + msg.header.frame_id + ' to ' + target_frame + '. Will ignore this goal.')

        # print('Received new goal')
        # self.goal = copy.copy(msg)  # store goal
        # self.goal_active = True



    def driveStraight(self, minumum_speed=0.2, maximum_speed=1.5):
        goal_copy = copy.deepcopy(self.goal)  # make sure we don't change the stamp field of the goal
        goal_copy.header.stamp = rospy.Time.now()

        # goal_tf = tf2_geometry_msgs.PoseStamped()
        # goal_tf.header.stamp = rospy.Time.now()
        # goal_tf.header.frame_id = self.goal.header.frame_id

        #print('Transforming pose')
        goal_in_base_link = self.tf_buffer.transform(goal_copy, self.name + '/base_footprint', rospy.Duration(1))
        # goal_in_base_link = self.tf_buffer.transform(goal_copy, 'p_bpereira/base_footprint', rospy.Duration(1))
        #print('Pose trasnformed')

        x = goal_in_base_link.pose.position.x
        y = goal_in_base_link.pose.position.y

        self.angle = math.atan2(y, x)

        distance_to_goal = math.sqrt(x ** 2 + y ** 2)
        self.speed = max(minumum_speed, 0.5 * distance_to_goal)  # limit minimum speed
        self.speed = min(maximum_speed, self.speed)  # limit maximum speed

    def sendCommandCallback(self, event):

        if (self.goal_active == 0):  # no goal, no movement
            self.angle = 0
            self.speed = 0
        elif (self.goal_active == 1):  # move_base_simple/goal
            self.driveStraight()

        if debugmode:
            print('Sending twist command ' + str(self.goal_active) + ' last_goal_active::' + str(
                self.last_goal_active) + ' speed::' + str(self.speed) + "  angulo::" + str(self.angle))

        twist = Twist()
        twist.linear.x = self.speed
        twist.angular.z = self.angle
        self.last_angle = self.angle
        self.publisher_command.publish(twist)
       # self.goal_active == 0

def main():

    rospy.init_node('p_bpereira_driver', anonymous=False)
    driver = Driver()

    equipa = configurarEquipa( driver.name )

    estrategia = configurarEstrategia(equipa['minhaquipa'])

    driver.equipa = equipa['minhaquipa']
    driver.estrategia = estrategia[driver.name]

    if debugmode:
        print("vai começar com " + driver.name)
        print("estratégia do  " + driver.name + " é ::" + str(driver.estrategia))
        print (equipa)

    rate = rospy.Rate(5)

    while True:

        driver.action()

        if cv2.waitKey(1) == ord('q'):
            break

        rate.sleep()

        rospy.spin()

    cv2.destroyAllWindows()

    # rospy.init_node('p_bpereira_driver', anonymous=False)
    # pub = rospy.Publisher('p_bpereira/cmd_vel', Twist, queue_size=1)
    #
    # rate =rospy.Rate(10)
    #
    # while not rospy.is_shutdown():
    #
    #     twist = Twist()
    #     twist.linear.x = 0.5
    #     twist.angular.z = -1
    #
    #     pub.publish(twist)
    #     rate.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
