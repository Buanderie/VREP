#!/usr/bin/python

import vrep
import rl_helper
import rlcontroller

from pynput.keyboard import Key, Listener
import threading

import torch
from torch.autograd import Variable

from rlcontroller import Actor

thrustValue = 0.0
rl_functions = None

actor = rlcontroller.Actor(2)

try:
    vrep.simxFinish(-1)
    clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

    if clientID != -1:
        rl_functions = rl_helper.RL(clientID)
        print('Main Script Started')

        rl_functions.init_sensors()
        rl_functions.start_sim()

        while vrep.simxGetConnectionId(clientID) != -1:

            for i in range(10000):  # number episodes
                print "episode"
                # Reset environment
                done = False
                while not done:
                    # Check if drone is underground ?
                    print "pol"
                    a = Variable(torch.randn(4))
                    coucou = actor(a)

            rl_functions.rotor_data = [thrustValue, thrustValue, thrustValue, thrustValue]
            rl_functions.do_action()
            rl_functions.target_z = 5.0
            # print(rl_functions.get_reward())

    else:
        print "Failed to connect to remote API Server"
        rl_functions.stop_sim()
        vrep.simxFinish(clientID)
except KeyboardInterrupt:
    rl_functions.stop_sim()
    vrep.simxFinish(clientID)
