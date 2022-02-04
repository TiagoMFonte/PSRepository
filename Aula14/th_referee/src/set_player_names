#!/usr/bin/env python3

# --------------------------------------------------
# Miguel Riem Oliveira.
# PSR, September 2020.
# Adapted from http://wiki.ros.org/tf2/Tutorials/Writing%20a%20tf2%20broadcaster%20%28Python%29
# -------------------------------------------------

# ------------------------
#   IMPORTS
# ------------------------
import math, random
import subprocess
from colorama import Fore, Back, Style
from functools import partial
import rospy
import tf_conversions  # Because of transformations
import tf2_ros
import geometry_msgs.msg
from gazebo_msgs.msg import ModelState, ModelStates, ContactsState

# ------------------------
#   DATA STRUCTURES
# ------------------------
from gazebo_msgs.srv import SetModelState


def bash(cmd, blocking=True, verbose=False):
    if verbose:
        print("Executing command: " + cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if blocking:
        for line in p.stdout.readlines():
            print(line)
            p.wait()


rospy.init_node('set_player_names')  # initialize the ros node
rospy.sleep(0.2)  # make sure the rospy time works

# Create a dictionary so we can retrieve the players of a team using the team color
players = {'red': rospy.get_param('/red_players'),
           'green': rospy.get_param('/green_players'),
           'blue': rospy.get_param('/blue_players')}

# Make sure all gazebo markers are deleted

bash(cmd="gz marker -m 'action: ADD_MODIFY, type: TEXT, id: 7, scale: {x:0.3, y:0.3, z:0.3}, text: \"red1\", parent: \"red1::base_footprint\", pose: {position: {x:0, y:0, z:0.5}, orientation: {x:0, y:0, z:0, w:1}}'",
    verbose=True)  # just to send something which can be deleted afterwards
rospy.sleep(0.2)
rospy.loginfo('Removing all markers from Gazebo')
bash(cmd='gz marker -x', verbose=True)
rospy.sleep(0.2)
rospy.loginfo('List existing markers from Gazebo')
bash(cmd='gz marker -l', verbose=True)
rospy.sleep(0.2)

# Create an instance for each player
count = 1
for player in players['red'] + players['green'] + players['blue']:
    # Add gazebo marker text with the name of the player
    cmd = "gz marker -m 'action: ADD_MODIFY, type: TEXT, id: " + str(count) + \
          ", scale: {x:0.3, y:0.3, z:0.3}, text: \"" + player + "\", parent: \"" + player + \
          "::base_footprint\", pose: {position: {x:0, y:0, z:0.5}, orientation: {x:0, y:0, z:0, w:1}}'"
    bash(cmd, verbose=True)
    count += 1
    rospy.sleep(0.2)
