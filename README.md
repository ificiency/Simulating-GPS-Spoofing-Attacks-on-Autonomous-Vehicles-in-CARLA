## Simulating GPS Spoofing Attacks on Autonomous Vehicles in CARLA
Overview (ongoing) ##


This project demonstrates a basic cybersecurity threat scenario using CARLA 0.9.15, where multiple autonomous vehicles experience GPS spoofing attacks. Each vehicle is equipped with 	a GPS sensor, and the simulation manipulates GPS coordinates to simulate an attack. This scenario can help researchers and developers study the effects of GPS spoofing on autonomous vehicle behavior and develop mitigation strategies.



## Features ##

	Multi-Vehicle Simulation: Spawns multiple autonomous vehicles in the CARLA environment.
	GPS Spoofing: Overrides GPS output for each vehicle, providing both original and spoofed coordinates.
	Cybersecurity Simulation: Models a realistic GPS spoofing threat, relevant for studying autonomous vehicle security.



## Prerequisites ##

	CARLA 0.9.15 (Installation guide: CARLA Documentation)
	Python 3.7+
	Required Python libraries (see Installation section below)


## Installation ##
    
  1. Clone this repository:

 		git clone https://github.com/yourusername/gps-spoofing-cybersecurity
		
		cd gps-spoofing-cybersecurity


  2. Install required Python packages: Use the requirements.txt provided in the repository:

                pip install -r requirements.txt


  3. Set up CARLA:

	Ensure that CARLA 0.9.15 is installed and running. Launch CARLA by running CarlaUE4.exe in the CARLA root directory.






## Usage ##

   1. Run the CARLA Simulator: Open a terminal in the project directory where CarlaUE4.exe is kept and execute the Python script:

	CarlaUE4.exe -carla-rpc-port=3000

	CarlaUE4.exe -carla-rpc-port=3000 -map=Town03



   2. Run the GPS Spoofing Simulation:

	Open a terminal in the project directory where gps-spoofing.py is kept and execute the Python script with the below:


		py -3.7 generate_traffic.py --port 3000 --tm-port 6000

		py -3.7 generate_traffic.py --port 3000 --tm-port 6000 --number-of-vehicles 15


   3. Simulation Output:
 
        The script spawns multiple vehicles, attaches GPS sensors, and simulates GPS spoofing by overriding GPS coordinates. It will output both original and spoofed GPS data for each     	vehicle, allowing you to observe the effects of the spoofing attack in real time.




## Code Structure ##

  gps_spoofing.py: The main Python script for running the GPS spoofing simulation. It handles vehicle spawning, GPS sensor attachment, and GPS spoofing logic.




## Example Output ##

The output will display GPS data for each vehicle:


	Vehicle ID: 1
	Original GPS: (x: 51.5074, y: -0.1278)
	Spoofed GPS:  (x: 40.7128, y: -74.0060)
	...




## Contributing ##

Contributions are welcome! Please follow these steps:

	Fork the repository.
	Create a new branch (git checkout -b feature-branch).
	Make your changes and commit them (git commit -m "Add new feature").
	Push to the branch (git push origin feature-branch).
	Open a Pull Request.




## License ##

This project is licensed under the MIT License - see the LICENSE file for details.




## Acknowledgments ##

The CARLA simulator team for providing an open-source platform for autonomous vehicle simulation.
The open-source community for contributing to the tools and libraries used in this project.


