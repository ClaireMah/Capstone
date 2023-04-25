### Before getting started : check the following requirements.

Hardware requirement : for this session, you will need a MAMBO parrot drone with a charged battery, a connexion cable and a FPV Camera. 


Software requirement :

1- Python3. It won't work with oldest version of python.

2-Visual studio. If you have to install Python3, choose to install Visual Studio with it. Otherwise, you could also install it separatly.

3-Vision software : install opencv and VLC. 
     Installing opencv : pip install opencv-python. Chek if the installation is sucessfull by trying to import cv2 (type import cv2 in your python Shell).
     Installing VLC : you will need to install the actual software, not just the python library. Ton install it, follow the instruction provides by the following link: https://www.videolan.org/vlc/index.html

3-Install untangle with this command : pip install untangle 

4-Install Zeroconf : pip install zeroconf
 
5- You can now install the parrot library : pip install pyparrot
 
 
 
 ### Getting started : once you met all of the requirement listed above, you can now try to connect you drone to your labtop.
 
 1- Turn on the drone and install the camera.
 
 2- Find the wifi connection that have the name of your drone. Select it to be connected to your drone. It WON'T provide you an internet connection but simply connect with your drone. 

 3- Wait until the drone is connected. Now you should be ready to fly !
 


If you have any questions about the pyparrot library, go to the following link: https://pyparrot.readthedocs.io/en/latest/index.html

Please run the files by order as the difficulty is increasing and you will need what you learned on previous file to run the next ones.

Order :
1_first_connection.py
2_first_flights.py
3_first_flight_flip.py
4_first_flight_direct.py
5_first_flight_figures.py
 
 
 GOOD LUCK !

If you want to use the drone with your phone, it might ask for an update.

To do this update :
1- Go to the following website adress  https://www.parrot.com/en/support/documentation/mambo-range and download the latest MAMBO Firmware update.

 
2-Insert the battery in the slot provided in this purpose as shown in the Quick start guide. Wait until the eyes of you Mambo are blincking green.

3-Connect the Manbo drone with the USB cable to your labtop. Wait until the eyes of your Mambo are green and not blincking anymore. Normally a folder name Parrot should appear.
 
4-Copy the update file you downloaded at the same emplacement as the Parrot folder but NOT in the folder. The eyes of the drone should be blincking in orange during the transfer. Once the transfer is finished,they will turn green again.

5-Eject the Mamno drone of you labptop. The eyes of the MAMBO will turn orange once again while the updates are done. Do NOT remove the battery during this. When it's finished, eyes will turn green again and the drone should be ready to fly.
 
