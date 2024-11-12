import glob
import os
import sys
import time
import argparse
import random
import carla

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


def main():
    argparser = argparse.ArgumentParser(
        description="CARLA GPS Spoofing Simulation with HUD")
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=3000,
        type=int,
        help='TCP port to listen to (default: 3000)')
    argparser.add_argument(
        '--tm-port',
        metavar='P',
        default=6000,
        type=int,
        help='Port to communicate with Traffic Manager (default: 6000)')
    argparser.add_argument(
        '--sync',
        action='store_true',
        help='Activate synchronous mode execution')
    args = argparser.parse_args()

    client = carla.Client(args.host, args.port)
    client.set_timeout(10.0)
    world = client.get_world()

    # Move the spectator camera to get a better view
    spectator = world.get_spectator()
    spectator.set_transform(carla.Transform(carla.Location(x=0, y=0, z=50), carla.Rotation(pitch=-90)))

    # Setup Traffic Manager
    traffic_manager = client.get_trafficmanager(args.tm_port)
    traffic_manager.set_global_distance_to_leading_vehicle(2.5)
    print(f"Traffic Manager bound to port {args.tm_port}")
    time.sleep(2)

    # Enable synchronous mode if specified
    settings = world.get_settings()
    if args.sync:
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)

    # Retrieve a vehicle blueprint
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.filter('vehicle.*')[0]

    # Define spoofed GPS coordinates
    spoofed_latitude = 52.0
    spoofed_longitude = 4.0

    # Spawn vehicles and attach GPS sensors
    num_vehicles = 2  # Number of vehicles to spawn
    vehicles = []
    gps_sensors = []
    spawn_location = carla.Location(x=0, y=0, z=1)

    for i in range(num_vehicles):
        spawn_point = carla.Transform(
            location=carla.Location(
                x=spawn_location.x + i * 10,  # Spread vehicles
                y=spawn_location.y,
                z=spawn_location.z
            ),
            rotation=carla.Rotation(yaw=0)
        )

        vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
        if vehicle:
            vehicle.set_autopilot(True, traffic_manager.get_port())
            vehicles.append(vehicle)
            print(f"Vehicle {i} successfully spawned at {spawn_point.location}")

            # Attach a GPS sensor to the vehicle
            gps_bp = blueprint_library.find('sensor.other.gnss')
            gps_transform = carla.Transform(carla.Location(x=1.0, z=2.8))
            gps_sensor = world.spawn_actor(gps_bp, gps_transform, attach_to=vehicle)

            # Define a callback function for GPS spoofing with HUD output
            def gps_callback(event, vehicle_id=vehicle.id):
                original_lat = event.latitude
                original_long = event.longitude
                print(f"[Vehicle {vehicle_id}] Original GPS: Latitude={original_lat}, Longitude={original_long}")
                print(f"[Vehicle {vehicle_id}] Spoofed GPS: Latitude={spoofed_latitude}, Longitude={spoofed_longitude}")

            # Set the GPS sensor to use the spoofing callback
            gps_sensor.listen(lambda event, id=vehicle.id: gps_callback(event, id))
            gps_sensors.append(gps_sensor)
        else:
            print("Spawn failed due to collision or other issues.")

    # Run the simulation loop
    try:
        while True:
            if args.sync:
                world.tick()
            else:
                world.wait_for_tick()
    finally:
        # Cleanup: Destroy actors after the simulation ends
        print("Destroying actors...")
        for gps_sensor in gps_sensors:
            gps_sensor.stop()
            gps_sensor.destroy()
        for vehicle in vehicles:
            vehicle.destroy()
        if args.sync:
            settings.synchronous_mode = False
            world.apply_settings(settings)
        print("Simulation ended")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Simulation interrupted by user")
