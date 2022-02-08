#!/usr/bin/env python3

import rospy

def configurarEquipa(player_name):

    equipa = {'red': rospy.get_param('/red_players'),
            'blue': rospy.get_param('/blue_players'),
            'green': rospy.get_param('/green_players')}

    # print (equipa['red'])

    if player_name in equipa['red']:
        equipa['minhaquipa'], equipa['presas'], equipa['cacador'] = 'red','green','blue'
    elif player_name in equipa['green']:
        equipa['minhaquipa'], equipa['presas'], equipa['cacador'] = 'green', 'blue', 'red'
    elif player_name in equipa['blue']:
        equipa['minhaquipa'], equipa['presas'], equipa['cacador'] = 'blue', 'red', 'green'
    else:
        rospy.loginfo('o jogador '+player_name+' nao tem equipa')
        return equipa

    equipa['colegas']=equipa[equipa['minhaquipa']]
    equipa['m_presas'] = equipa[equipa['presas']]
    equipa['m_cacador'] = equipa[equipa['cacador']]

    rospy.loginfo('OK Equipas definidas ::' + player_name + '  tem equipa')

    return equipa

def configurarEstrategia(player_team):

    estrategia = {'red1': rospy.get_param('/'+player_team+'jogador1'),
                'red2': rospy.get_param('/'+player_team+'jogador2'),
                'red3': rospy.get_param('/'+player_team+'jogador3')}

    # TODO: verificar se é erategia 3 e atribuir uma nova conforme os pontos de apanhar e ser apanhado

    return estrategia
