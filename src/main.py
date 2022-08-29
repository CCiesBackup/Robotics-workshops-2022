#!/usr/bin/env python3
import time

import ev3dev.ev3 as ev3
import logging
import os
import paho.mqtt.client as mqtt
import uuid
import signal

import CommunicationInterfaceForOdometry
import CommunicationInterfaceForOdometry as com
from CommunicationFactory import CommunicationFactory
from ExplorationManager import ExplorationManager
from MessageModelManager import OutgoingMessages
from communication import Communication
from odometry import Odometry
from planet import Direction, Planet

client = None  # DO NOT EDIT


def run():
    print('Bin online')
    # DO NOT CHANGE THESE VARIABLES
    #
    # The deploy-script uses the variable "client" to stop the mqtt-client after your program stops or crashes.
    # Your script isn't able to close the client after crashing.
    global client

    client_id = '202-' + str(uuid.uuid4())  # Replace YOURGROUPID with your group ID
    client = mqtt.Client(client_id=client_id,  # Unique Client-ID to recognize our program
                         clean_session=True,  # We want a clean session after disconnect or abort/crash
                         protocol=mqtt.MQTTv311  # Define MQTT protocol version
                         )
    # Setup logging directory and file
    curr_dir = os.path.abspath(os.getcwd())
    if not os.path.exists(curr_dir + '/../logs'):
        os.makedirs(curr_dir + '/../logs')
    log_file = curr_dir + '/../logs/project.log'
    logging.basicConfig(filename=log_file,  # Define log file
                        level=logging.DEBUG,  # Define default mode
                        format='%(asctime)s: %(message)s'  # Define default logging format
                        )
    logger = logging.getLogger('RoboLab')

    # THE EXECUTION OF ALL CODE SHALL BE STARTED FROM WITHIN THIS FUNCTION.
    # ADD YOUR OWN IMPLEMENTATION HEREAFTER.

    explorer = ExplorationManager()
    communication = CommunicationFactory.getInstance(client, logger, explorer)
    # Be careful: Initializing the communication module establishes a real connection to the server!


    # while loop mit Austauschbaren Verhalten
    # TEST ONlY - BITTE VOR DER PRÜFUNG ENTFERNEN!!!
    test_planet_name = "Conway"
    communication.send_test_planet(test_planet_name)
    odometer = Odometry(0, (0, 0))
    odometer.driving()
    communication.send_ready()
    time.sleep(3)
    odometer.setCoordinates(explorer.current_position)
    odometer.setCurrentDirection(explorer.current_orientation)
    unknown_paths_absolute = odometer.getDirections()
    explorer.push_scanning_results(unknown_paths_absolute, ready=True)
    direction = explorer.get_directions()
    communication.send_path_select(explorer.current_position[0], explorer.current_position[1], direction)
    time.sleep(3)
    direction = explorer.get_directions()

    while not direction == 128:
        path_status = 'free'
        odometer.turnRelative(direction)
        odometer.driving()
        time.sleep(2)
        absolute_direction = odometer.getdirection()
        coordinates = odometer.getTarget()
        
        if odometer.somethingInWay:
            path_status = 'blocked'
        communication.send_path(explorer.current_position[0], explorer.current_position[1], direction, coordinates[0],
                                coordinates[1], absolute_direction, path_status)
        time.sleep(3)
        direction = explorer.get_directions()
        if not direction == 128:
            communication.send_path_select(coordinates[0], coordinates[1], direction)
        
    ev3.Sound.beep()
    print("RIP")


# DO NOT EDIT
def signal_handler(sig=None, frame=None, raise_interrupt=True):
    if client and client.is_connected():
        client.disconnect()
    if raise_interrupt:
        raise KeyboardInterrupt()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    try:
        run()
        signal_handler(raise_interrupt=False)
    except Exception as e:
        signal_handler(raise_interrupt=False)
        raise e
