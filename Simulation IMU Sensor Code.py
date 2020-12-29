from __future__ import print_function


# ==============================================================================
# -- find carla module ---------------------------------------------------------
# ==============================================================================


import glob
import os
import sys
import random
import time
import numpy as np
import cv2
import csv
from csv import writer
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================


import carla

IM_WIDTH = 640
IM_HEIGHT = 480
img_no = 0
actor_list = []

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
    # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

try:
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    bp = blueprint_library.filter("model3")[0]
    print(bp)
    spawn_point = random.choice(world.get_map().get_spawn_points())
    vehicle = world.spawn_actor(bp, spawn_point)
    #vehicle.set_autopilot(True)
    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
    actor_list.append(vehicle)

    imu_bp = world.get_blueprint_library().find('sensor.other.imu')
    imu_location = carla.Location(0,0,0)
    imu_rotation = carla.Rotation(0,0,0)
    imu_transform = carla.Transform(imu_location,imu_rotation)
    #imu_bp.set_attribute("sensor_tick",str(3.0))
    ego_imu = world.spawn_actor(imu_bp,imu_transform,attach_to=vehicle)
    #spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
    #sensor = world.spawn_actor(imu_bp, spawn_point, attach_to=vehicle)
    #actor_list.append(sensor)


    def imu_callback(imu):
        print("IMU measure:\n"+str(imu)+'\n')
        l = []
        global img_no
        img_no = img_no + 1
        l.append("IMU Sensor")
        l.append(str(time.time()))
        append_list_as_row('IMU_Sensor.csv', l)
    ego_imu.listen(lambda imu: imu_callback(imu))
    time.sleep(5)

finally:
    for actor in actor_list:
        actor.destroy()
    print("Vedant Ghodke - IMU Sensor Data Extraction Completed!")
