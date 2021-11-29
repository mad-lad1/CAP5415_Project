import carla
from time import sleep
import numpy as np
from agents.navigation.local_planner import LocalPlanner
from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.navigation.global_route_planner_dao import GlobalRoutePlannerDAO
import matplotlib.pyplot as plt
import random
import cv2
import torch
from skimage import color

def get_carla_image_data_array(carla_image):    
    carla_image_data_array = np.ndarray(
        shape=(carla_image.height, carla_image.width, 4),
        dtype=np.uint8, buffer=carla_image.raw_data)
    
    carla_image_data_array = carla_image_data_array[:, :, :3]
    
    carla_image_data_array =  carla_image_data_array/255.0
    model = torch.load('model_v2.pt')
    carla_tensor = torch.Tensor(carla_image_data_array).to('cuda')
    carla_tensor = carla_tensor.view(1, 3, 480, 480)
    output =  model(carla_tensor)['out'].cpu()
    output = output[0].argmax(0)
    output = output.numpy()   
    result_image = color.label2rgb(output, carla_image_data_array)
    del output
    cv2.imshow("", result_image)
    cv2.waitKey(1)


client = carla.Client('localhost', 2000)
client.set_timeout(20.0)
world = client.get_world()
map = world.get_map()

waypoints = world.get_map().generate_waypoints(distance=1.0)
filtered_waypoints = []
spawn_points = []
for waypoint in waypoints:
  if(waypoint.road_id == 2):
    filtered_waypoints.append(waypoint)
    
    
vehicle_blueprint = world.get_blueprint_library().filter('model3')[0]
spawn_point1 = filtered_waypoints[100].transform
spawn_point1.rotation.yaw = 0
spawn_point1.location.z += 1
spawn_point1.location.x += 0.2

                                   
waypoints = world.get_map().generate_waypoints(distance=1.0)
vehicle_blueprint = world.get_blueprint_library().filter('model3')[0]

filtered_waypoints = []
spawn_points = []
for waypoint in waypoints:
  if(waypoint.road_id == 2):
    filtered_waypoints.append(waypoint)


spawn_point1 = filtered_waypoints[10].transform
spawn_point1.rotation.yaw = 0
spawn_point1.location.z += 1
spawn_point1.location.x += 0.2

vehicle1 = world.spawn_actor(vehicle_blueprint, spawn_point1)
vehicle1.set_autopilot(True)

blueprint = world.get_blueprint_library().find('sensor.camera.rgb')
blueprint.set_attribute('image_size_x', '480')
blueprint.set_attribute('image_size_y', '480')
blueprint.set_attribute('fov', '110')
blueprint.set_attribute('sensor_tick', '1.0')
transform = carla.Transform(carla.Location(x=0.8, z=1.7))
sensor = world.spawn_actor(blueprint, transform, attach_to=vehicle1)
sensor.listen(lambda data: get_carla_image_data_array(data))

sleep(10000)
