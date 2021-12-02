#!/usr/bin/env python
# license removed for brevity
import rospy
from psr_aula8_ex4.msg import Dog

def talker():
    pub = rospy.Publisher('chatter', Dog, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(0.5) # 0.5hz
    while not rospy.is_shutdown():
        dog = Dog()
        dog.name = 'Bobby'
        dog.age = 77
        dog.color = 'brown'
        dog.brothers.append('Rosita')
        rospy.loginfo('Sending dog...')

        pub.publish(dog)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass