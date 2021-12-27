#!/usr/bin/env python3
import colorama
import rospy
from std_msgs.msg import String
from psr_aula9_ex_tp.msg import Dog

def main():
    pub = rospy.Publisher('chatter', Dog, queue_size=10)
    rospy.init_node('publisher', anonymous=True)
    # read global parameter
    highlight_text_color = rospy.get_param("/highlight_text_color")
    # read private parameter
    frequency = rospy.get_param("~frequency", default=10)
    rate = rospy.Rate(frequency)  # 0.5hz
    while not rospy.is_shutdown():
        dog = Dog()
        dog.name = 'Bobby'
        dog.age = 77
        dog.color = 'brown'
        dog.brothers.append('Rosita')
        rospy.loginfo('Sending dog...' +
                      getattr(colorama.Fore, highlight_text_color))

        pub.publish(dog)
        rate.sleep()

if __name__ == '__main__':
    main()