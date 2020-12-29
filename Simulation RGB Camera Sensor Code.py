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
    spawn_point = (world.get_map().get_spawn_points()
    vehicle = world.spawn_actor(bp, spawn_point)
    #vehicle.set_autopilot(True)
    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
    actor_list.append(vehicle)
    
    cam_bp = blueprint_library.find("sensor.camera.rgb")
    cam_bp.set_attribute("image_size_x", f"{IM_WIDTH}")
    cam_bp.set_attribute("image_size_y", f"{IM_HEIGHT}")
    cam_bp.set_attribute("fov", "110")
    #spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
    sensor = world.spawn_actor(cam_bp, spawn_point, attach_to=vehicle)

    def process_img(image):
        l = []
        global img_no
        img_no = img_no+1
        l.append("RGB Camera Image")
        l.append(str(time.time()))
        #l.append(str[image.timestamp])
        append_list_as_row('RGB_Camera_Sensor_Prajwal.csv', l)
        #print(type(image.timestamp))
        #print(dir(image))
        i = np.array(image.raw_data)
        # print(i.shape)
        i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
        i3 = i2[:, :, :3]
        cv2.imshow("", i3)
        cv2.waitKey(1)
        return i3 / 255.0
        #actor_list.append(sensor)
    sensor.listen(lambda data: process_img(data))
    time.sleep(5)

finally:
    for actor in actor_list:
        actor.destroy()
    print("Vedant Ghodke - RGB Camera Sensor Data Extraction Completed!")
    