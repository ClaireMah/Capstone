# Indoor Drone Photogrammetry and Navigation
## ENGO 500 Geomatics Engineering Capstone Design Project

Claire Mah
Hannah Poon
Mabel Heffring

April 4th, 2023

### Python Environment: 
- Use Python3
- In your python environment, install the following packages
    - untangle
    - zeroconf
    - pyparrot
    - opencv-python
- More detailed instructions in LearnToFly/ReadMe
- https://pyparrot.readthedocs.io/en/latest/ 
- Pyparrot must be modified to properly connect to the drone (due to versioning issues)
    - Install pyparrot so that you have a local, editable verson
    - If FTP connection is commented out, uncomment this section (check in MiniDrone.py and wifiConnection.py)

### Flying the drone:
- Attach FPV camera to the drone. 
- Turn on the drone, wait for flashing green eyes.
- Look for a wifi connection called Mambo_XXXXXX (each drone will have a unique 6 digit ID). Sometimes it takes a few minutes to show up. 
- Connect to this network, you will not have internet access. 
- Run your script (start with the ones in LearnToFly folder)

### Landing:
If you lose connection, the drone will keep flying. To land, either:
- Make sure you are still connected to the drones network and run "panic.py". This will reconnect to the drone and safely land it. 
- Firmly tap the drone's propeller guards from the side. This will activate an emergency crash feature of the drone and will immediately cut it's flight. Be ready to catch it. 

### Other tips: 
- To reset, hold down power button. Eyes will turn red. Keep holding power button until eyes are green again. 
- Fly in large open space, ideally at least 2m radius of space on all sides of the drone. It is very lightweight and will drift near walls or other obstacles. 
- Symbol detection works best with a white background for contrast
- Pyparrot is an open source library, not designed by the drone manufacturers. Some features may not work. The drones and the library are no longer supported. 


---- 

### Main Flight (main_flight.py):
- This script is designed to collect images in a semi-autonomous manner to be used in a photogrammetric bundle adjustment
- To set up, find a large open indoor space with bright lighting. 
- Choose 2 distinct symbols. Currently, the program is coded to use red squares as boundary points for navigation and green circles for bundle adjustment points. 
- Note: If symbol detection is difficult, it is recommended to attach a white background to each symbol to improve the contrast
- Clearly number each symbol so that the numbers are easily visible from the drone imagery
- Tape symbols to the floor. 
    - Boundary points should make a circle, approximately 2m across. 
    - Photogrammetry points can be placed anywhere within the circle. Recommended to use at least 15. 
- Define a local coordinate system. (0,0,0) should be the drone's takeoff location, roughly in the middle of the circle. Our coordinate system was defined as left handed, with Z pointing down. 
- Measure approximate locations of photogrammetry points in your local coordinate system, cm accuracy. 
- Connect to the drone and run main_flight.py. It will fly the drone within the defined boundary and collect up to 20 images. 

### Nadir Camera Calibration:
- Install Matlab with the Computer Vision Toolbox included
- Print out checkerboard (calibrationpattern_checkerboard.pdf)
- Collect 10-20 images of the checkerboard using only_pictures.py
- Start the Matlab calibrator app by entering "cameraCalibrator" into the command prompt
- Follow the calibration steps outlined here: https://www.mathworks.com/help/vision/ug/using-the-single-camera-calibrator-app.html
- Export the camera IOPs and their precisions

### Tie Point Detection (detectTie.py):
- This script contains a function for detecting and measuring object points in the nadir drone imagery.
- The inputs to this function are as follows:
	- main_folder: Path to the primary folder
    - output_file: Path to output file for image space observations
    - img_subfolder: Name of current image folder
    - minCon: minimum area for an acceptable contour (e.g. 200)
    - maxCon: maximum area for an acceptable contour (e.g. 2000)
- Run the script for the desired drone images
- For each image, manual organization and cleaning is required:
	- For each point, input the visible corresponding point number into the command prompt and press enter.
	- If the contour is not a point, input -1 as the point number and it will be removed.
	- Go over each image after detection to ensure no points are missed. If a point has been missed, consider adjusting the area threshold (minCon and maxCon) or acceptable colour range.
	- Manually measure the missing point coordinates using an external software (e.g. IrfanView) and add it to the output file.

### Bundle Adjustment:
- Set up 6 input files
    - .con > Control points, known coordinates (PointID X Y Z)
    - .tie > Tie points, approximate coordinates (PointID X Y Z)
    - .int > Camera internal orientation parameters (CameraID x_principalpoint y_princialpoint focallength)
    - .pho > Points from image observations (PointID ImageID X Y)
    - .ext > External orientation parameters/approximate camera pose (ImageID CameraID X Y Z omega phi kappa)
        - X Y Z and kappa can be estimated manually or by coordinate estimates in main_flight. 
        - Assume omega and phi to be approximately 0 (Drone is level)
- main.py line 22 > Make sure path points to your data
- read_inputs.py line 29 to 61 > Optionally uncomment/write code to modify or filter images, points, or EOPS
- Run main.py
- Read output_file.txt for results 


----- 

### To access drone directly:
- Connect to a computer via USB
- Drone should appear in file explorer
- Press power button 4 times to enter debug mode
- Can connect to the linux terminal with Telenet connection to 192.168.2.1 on PuTTY, or other terminal emulator software. 
- Tutorial here: https://sites.google.com/view/minidronefirmwarefun 

### Firmware issues:
- Drones were initially bought with firmware 3.0.6. 
- If you want to use the app (Parrot FreeFlight Mini), it will ask you to upgrade to 3.0.26. 
- Drones were tested using both 3.0.6 and 3.0.26, both versions will work. 
- There are known bugs with 3.0.26 that broke access to the groundcam. Access is still possible using pyparrot. Ignore error messages that say otherwise. 