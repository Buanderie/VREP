#!/usr/bin/python

import vrep
import rl_helper

from pynput.keyboard import Key, Listener
import threading

thrustValue = 0.0

def on_press(key):
    print('{0} pressed'.format(
        key))
    global thrustValue
    if key == Key.up:
        thrustValue += 0.1
    if key == Key.down:
        thrustValue -= 0.1

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False

def worker():
    """thread worker function"""
    print 'Worker'
    # Collect events until released
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    return

t = threading.Thread(target=worker)
t.start()

rl_functions = None
try:
    vrep.simxFinish(-1)
    clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

    if clientID != -1:
        rl_functions = rl_helper.RL(clientID)
        print('Main Script Started')

        rl_functions.init_sensors()
        rl_functions.start_sim()

        while vrep.simxGetConnectionId(clientID) != -1:
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
