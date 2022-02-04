#!/usr/bin/env python3

import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from utils import configureTeam

import copy
import math
import rospy
import tf2_ros
from geometry_msgs.msg import Twist, PoseStamped
import tf2_geometry_msgs  # **Do not use geometry_msgs. Use this instead for PoseStamped

resolucaox = 1280
viramuito = 0.7
virapouco = 0.1
vira = 0.3


class Driver:

    def __init__(self):
        self.goal = PoseStamped()
        # 0 parado, 1 goal, 2 procura, 3 caça, 4 foge
        self.goal_active = 0
        self.last_goal_active = 0

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
        self.image_subscriber = rospy.Subscriber("/" + self.name + "/camera/rgb/image_raw", Image,
                                                 self.goalImageCallback)
        rospy.spin()

    def goalImageCallback(self, msg):

        #   print('action goalImageCallback')
        my_team = 'red'
        debugmode = True

        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")  # "passthrough" ) #

        # TODO: fazer com no airpaint
        # lower = np.array([35, 150, 20])
        # upper = np.array([70, 255, 255])
        # mask = cv2.inRange(imagehsv, lower, upper)
        # TODO: fazer com no airpaint
        green_mask = cv2.inRange(cv_image, (0, 100, 0), (50, 256, 50))
        red_mask = cv2.inRange(cv_image, (0, 0, 100), (50, 50, 256))
        blue_mask = cv2.inRange(cv_image, (100, 0, 0), (256, 50, 50))
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
        #     1 -  se nao vires nada andas à volta
        #     2 - ves uma presa atacas
        #     3 - ves um cacador foges, aqui temos um problema porque quando está a fugir nao ve nada, tem que estar num
        # estado de fuga, nunca sai deste estado? se lhe passar um presa à frente vai atras dela? depende do numero de pontos?
        # curvas a 90º antes de bater na parede? velocidades? sempre a topo ee fica todo descontrolado, pode ter vantagens ou desvantagens.
        # TODO: procedimento

        encontrapresa = 0
        contoursm, _ = cv2.findContours(presa_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contoursmi in contoursm:
            encontrapresa = 1
            M = cv2.moments(contoursmi)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])

                self.drivetoKill(cx, cy)
                if debugmode:
                    cv2.putText(cv_image, "presa", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            break

        # não encontra a presa vai parar
        # TODO: vai rodar à procura dela
        # TODO: se o caçador for maior deve estar mais perto, fugir?????

        if encontrapresa == 0:
            if not (self.goal_active == 0):
                self.last_goal_active = self.goal_active
            self.goal_active = 0

        encontracacador = 0
        contoursm, _ = cv2.findContours(cacador_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contoursmi in contoursm:
            encontracacador = 1
            M = cv2.moments(contoursmi)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                if debugmode:
                    cv2.putText(cv_image, "cacador", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        if debugmode:
            cv2.imshow("red1", cv_image)
            cv2.waitKey(1)
        # rospy.sleep(0.02)
        # cv2.imshow("prey", prey_mask)
        # rospy.sleep(0.02)
        # cv2.imshow("hunter", hunter_mask)

    def drivetoKill(self, x, y, minumum_speed=0.4, maximum_speed=1.0):

        if ((x > 0) and (x < 640)):
            if (x < 320):
                self.angle = viramuito
            elif (x < 550):
                self.angle = vira
            else:
                self.angle = virapouco
        # TODO: VIRAR pouco pu nao virar quando está no centro da imagem
        elif ((x > 640)):
            if (x < 700):
                self.angle = -1 * virapouco
            elif (x < 960):
                self.angle = -1 * vira
            else:
                self.angle = -1 * viramuito

        print("drivetokill  x::" + str(x) + "   y::" + str(y) + "   self.angle ::" + str(self.angle))

        distance_to_goal = math.sqrt(x ** 2 + y ** 2)
        self.speed = max(minumum_speed, 0.3 * distance_to_goal)  # limit minimum speed
        self.speed = min(maximum_speed, self.speed)  # limit maximum speed

        self.goal_active = 3
        # self.goal_active = 0

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
            rospy.logerr(
                'Could not transform goal from ' + msg.header.frame_id + ' to ' + target_frame + '. Will ignore this goal.')

        # print('Received new goal')
        # self.goal = copy.copy(msg)  # store goal
        # self.goal_active = True

    def driveStraight(self, minumum_speed=0.2, maximum_speed=1.5):
        goal_copy = copy.deepcopy(self.goal)  # make sure we don't change the stamp field of the goal
        goal_copy.header.stamp = rospy.Time.now()

        # goal_tf = tf2_geometry_msgs.PoseStamped()
        # goal_tf.header.stamp = rospy.Time.now()
        # goal_tf.header.frame_id = self.goal.header.frame_id

        # print('Transforming pose')
        goal_in_base_link = self.tf_buffer.transform(goal_copy, self.name + '/base_footprint', rospy.Duration(1))

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
            if not (self.last_goal_active == 0):
                self.angle = self.last_angle
        elif (self.goal_active == 1):  # move_base_simple/goal
            self.driveStraight()

        print('Sending twist command ' + str(self.goal_active) + ' last_goal_active::' + str(
            self.last_goal_active) + ' speed::' + str(self.speed) + "  angulo::" + str(self.angle))

        twist = Twist()
        twist.linear.x = self.speed
        twist.angular.z = self.angle
        self.last_angle = self.angle
        self.publisher_command.publish(twist)

def main():
    rospy.init_node('p_teamhunt_driver', anonymous=False)
    driver = Driver()

    print("vai começar com " + driver.name)

    equipa = configureTeam(driver.name)

    print(equipa)

    rate = rospy.Rate(5)

    while True:

        driver.action()

        if cv2.waitKey(1) == ord('q'):
            break

        rate.sleep()

        rospy.spin()

    cv2.destroyAllWindows()
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
