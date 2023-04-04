
from xml.dom.expatbuilder import makeBuilder
from pyparrot.Minidrone import Mambo
from pyparrot.Minidrone import Minidrone
from pyparrot.Minidrone import MamboGroundcam
import cv2
import os
import inspect
from os.path import join

def we_are_here():
    return os.getcwd()

mambo = Mambo(None, use_wifi=True) #address is None since it only works with WiFi anyway
print("trying to connect to mambo now")
success = Minidrone.connect(mambo, num_retries=3)
print("connected: %s" % success)

def save_picture(mambo_object,pictureName,filename):


    fullPath = inspect.getfile(we_are_here)
    shortPathIndex = fullPath.rfind("/")
    if (shortPathIndex == -1):
        # handle Windows paths
        shortPathIndex = fullPath.rfind("\\")
    shortPath = fullPath[0:shortPathIndex]
    print(shortPath)
    # filename="marker.jpg"
    storageFile = join(shortPath, filename)
    print('Your Mambo groundcam files will be stored here',storageFile)

    if (mambo_object.groundcam.ftp is None):
        print("No ftp connection")

    # otherwise return the photos
    mambo_object.groundcam.ftp.cwd(mambo.groundcam.MEDIA_PATH)
    try:
        mambo_object.groundcam.ftp.retrbinary('RETR ' + pictureName, open(storageFile, "wb").write) #download


    except Exception as e:
        print('error')

def is_in_the_list(l1,l2):
    for i in range(min(len(l1),len(l2))):
        if l1[i]!=l2[i]:
            return [i,l2[i]]
    return [len(l2)-1,l2[len(l2)-1]]

if (success):
    # get the state information
    print("sleeping")
    mambo.smart_sleep(1)
    mambo.ask_for_state_update()
    mambo.smart_sleep(1)

    #print("taking off!")
    #mambo.safe_takeoff(5)

    picture_names = mambo.groundcam.get_groundcam_pictures_names() #get list of availible files
    print(picture_names)
    print(len(picture_names))

    #reset the memory of the mambo
    if picture_names!=[]:
        for i in range(len(picture_names)):
            filename=picture_names[i]
            mambo.groundcam._delete_file(filename)

    #check if the pictures were deleted
    picture_names = mambo.groundcam.get_groundcam_pictures_names() #get list of availible files
    print(picture_names)
    print(len(picture_names))

    mambo.smart_sleep(1)

    #taking a picture
    pic_success = mambo.take_picture()
    print("picture")
    mambo.smart_sleep(0.5)

    #get list of all the files stored inside the Mambo
    picture_names_new = mambo.groundcam.get_groundcam_pictures_names()
    print(len(picture_names_new))

    #get the right picture
    picture_name=is_in_the_list(picture_names,picture_names_new)[1]
    print(picture_name)
    #filename=input("Filename ?")
    filename="img20.jpg"

    save_picture(mambo,picture_name,filename)
    mambo.smart_sleep(1)


    mambo.disconnect()
