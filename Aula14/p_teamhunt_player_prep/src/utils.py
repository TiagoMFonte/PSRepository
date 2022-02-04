#!/usr/bin/env python3

import rospy

def configureTeam(player_name):

    team = {'red': rospy.get_param('/red_players'),
            'blue': rospy.get_param('/blue_players'),
            'green': rospy.get_param('/green_players')}

    # print (team['red'])

    if player_name in team['red']:
        team['minhaquipa'], team['presas'], team['cacador'] = 'red','green','blue'
    elif player_name in team['green']:
        team['minhaquipa'], team['presas'], team['cacador'] = 'green', 'blue', 'red'
    elif player_name in team['blue']:
        team['minhaquipa'], team['presas'], team['cacador'] = 'blue', 'red', 'green'
    else:
        rospy.loginfo('o jogador '+player_name+' nao tem team')
        return team

    team['colegas'] = team[team['minhaquipa']]
    team['m_presas'] = team[team['presas']]
    team['m_cacador'] = team[team['cacador']]

    rospy.loginfo('OK Equipas definidas ::' + player_name + '  tem team')

    return team