from pyparrot.Minidrone import Mambo
from pyparrot.Minidrone import Minidrone
from pyparrot.Minidrone import MinidroneSensors
from pyparrot.DroneVisionGUI import DroneVisionGUI
import inspect
import cv2
import os
import sys
import symbols
import math
import numpy as np

def save_picture(mambo_object,pictureName,path,filename):

    storageFile = path +'\\'+ filename
    print('Your Mambo groundcam files will be stored here',storageFile)

    if (mambo_object.groundcam.ftp is None):
        print("No ftp connection")

    # otherwise return the photos
    mambo_object.groundcam.ftp.cwd(mambo_object.groundcam.MEDIA_PATH)
    try:
        mambo_object.groundcam.ftp.retrbinary('RETR ' + pictureName, open(storageFile, "wb").write) #download


    except Exception as e:
        print('error')

def is_in_the_list(l1,l2):
    for i in range(min(len(l1),len(l2))):
        if l1[i]!=l2[i]:
            return [i,l2[i]]
    return [len(l2)-1,l2[len(l2)-1]]

def main():

    mambo = Mambo(None, use_wifi=True) #address is None since it only works with WiFi anyway

    print("trying to connect to mambo now")
    success = Minidrone.connect(mambo, num_retries=3)
    print("connected: %s" % success)

    if (success):
        # get the state information
        # mambo.set_flat_trim()
        mambo.flat_trim()
        print("sleeping")
        mambo.smart_sleep(1)
        mambo.ask_for_state_update()
        mambo.smart_sleep(1)
        mambo.safe_takeoff(5)
        mambo.hover()
        x = 0
        y = 0
        z = 1500 #mambo.sensors.altitude()

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

        # print("Preparing to open vision")
        # mamboVision = DroneVisionGUI(mambo, is_bebop=False, buffer_size=200,
        #                                 user_code_to_run=demo_mambo_user_vision_function(mambo), user_args=(mambo, ))
        # userVision = symbols.UserVision(mamboVision)
        # mamboVision.set_user_callback_function(userVision.save_pictures, user_callback_args=None)
        # mamboVision.open_video()


#****************************************************************************

        # flight_control(mambo, x,y,z)

         # mambo.set_max_altitude(2)
        c=0

        picture_names = mambo.groundcam.get_groundcam_pictures_names()    #take picture
        mambo.hover()
        pic_success = mambo.take_picture()
        
        # need to wait a bit for the photo to show up
        mambo.smart_sleep(0.5)

        #Get z orientation and altitude
        mambo.sensors.set_user_callback_function(None, "DroneAltitude_altitude")
        direction = 360-mambo.sensors.get_estimated_z_orientation()
        expected_direction = 0
        # z = mambo.sensors.altitude_ts()
        print("\nheading: ", direction)
        print("\nheight: ", z)

        list_of_images = []
        picture_names_new = []
        flying = True

        x = 0
        y = 0
        coords = np.empty(shape=(25, 5), dtype='object')


        #LOOP:
        while flying == True:
            #ask which direction to fly
            picture_names = mambo.groundcam.get_groundcam_pictures_names()    #take picture

            mambo.smart_sleep(1)
            # mambo.hover()
            mambo.take_picture()
            mambo.smart_sleep(1)
            mambo.hover()

            z = 1000 # mambo.sensors.altitude()
            dist = 500

            coords[c] = [c,x,y,z,direction]

            # need to wait a bit for the photo to show up
            mambo.smart_sleep(0.5)

            #upload the new list after the picture
            
            picture_names_new = mambo.groundcam.get_groundcam_pictures_names()#essential to reload it each time; does not update automaticaly
            print("New length is",len(picture_names_new))

            #finding the new picture in the list
            index=is_in_the_list(picture_names, picture_names_new)
            list_of_images.append(index[1])
            mambo.hover()

                #get the right picture
            picture_name=is_in_the_list(picture_names,picture_names_new)[1]
            print(picture_name)
            #filename=input("Filename ?")
            # filename="img20.jpg"


            frame = mambo.groundcam.get_groundcam_picture(list_of_images[c],True)
            path = sys.path[0]
            print(path)

            if (frame is not None):
                filename = "test_image_%02d.png" % c
                # cv2.imwrite(path + '//' + filename, frame)
                save_picture(mambo,picture_name,path,filename)

                picturePath = path + '\\' + filename # symbols.get_path(filename)

                if symbols.is_red_square_here(picturePath):
                    print("There is a red square in this picture")
                    # expected_direction = 90 + expected_direction
                    # turn = expected_direction - direction-5
                    # print('turn\n', turn)
                    # print('direction\n', direction)
                    # print('expected_direction\n', expected_direction)
                    mambo.turn_degrees(165)
                    mambo.smart_sleep(1)
                    mambo.fly_direct(0,15,0,0,duration=1)
                    direction = 360-mambo.sensors.get_estimated_z_orientation()
                    x = x + dist*math.cos(math.radians(direction))
                    y = y + dist*math.sin(math.radians(direction))
                    # increment coordinates
                    mambo.hover()
                # elif symbols.is_green_square_here(picturePath):
                #     print("There is a green square in this picture")
                #     mambo.turn_degrees(90)
                #     mambo.fly_direct(0,20,0,0,duration=1)
                #     # increment coordinates
                #     mambo.hover()
                else:
                    mambo.fly_direct(0,15,0,0,duration=1)
                    mambo.smart_sleep(0.5)
                    mambo.hover()
                    direction = 360-mambo.sensors.get_estimated_z_orientation()
                    x = x + dist*math.cos(math.radians(direction))
                    y = y + dist*math.sin(math.radians(direction))
                # filename = "contour_image_%02d.png" % c
                # contour = symbols.draw_contour(picturePath)
                # cv2.imwrite(path+ '\\' +filename, contour)
                # save_picture(mambo,picture_name,path,filename)

                c = c+1
            if c > 20:
                flying = False
                break

            # z = MinidroneSensors.altitude()
            # print("\nz: ", z)
            print("\nheading: ", direction)
            
            if frame is not None:
                if frame is not False:
                    # cv2.imshow("Groundcam", frame)
                    cv2.waitKey(4000)
                    cv2.destroyAllWindows()
        print(coords)

#*********************************************************************

        mambo.safe_land(5)
        print("landed")
        mambo.disconnect()

# def flight_control(mambo,x,y,z):
        #set movement parameters
    # mambo.set_max_tilt(20) #equivalent to speed control

    # # mambo.set_max_altitude(2)
    # c=0

    # picture_names = mambo.groundcam.get_groundcam_pictures_names()    #take picture
    # mambo.hover()
    # pic_success = mambo.take_picture()
    
    # # need to wait a bit for the photo to show up
    # mambo.smart_sleep(0.5)

    # #Get z orientation and altitude
    # mambo.sensors.set_user_callback_function(None, "DroneAltitude_altitude")
    # direction = mambo.sensors.get_estimated_z_orientation()
    # expected_direction = 0
    # # z = mambo.sensors.altitude_ts()
    # print("\nheading: ", direction)
    # print("\nheight: ", z)

    # list_of_images = []
    # picture_names_new = []
    # flying = True

    # x = 0
    # y = 0

    # #LOOP:
    # while flying == True:
    #     #ask which direction to fly
    
    #     mambo.hover()
    #     mambo.take_picture()
    #     mambo.hover()

    #     z = 1500 # mambo.sensors.altitude()
    #     dist = 1000

    #     coords = np.empty(shape=(25, 5), dtype='object')
    #     coords[c] = [c,x,y,z,direction]

    #     # need to wait a bit for the photo to show up
    #     mambo.smart_sleep(0.5)

    #     #upload the new list after the picture
    #     picture_names_new = mambo.groundcam.get_groundcam_pictures_names()#essential to reload it each time; does not update automaticaly
    #     print("New length is",len(picture_names_new))

    #     #finding the new picture in the list
    #     index=is_in_the_list(picture_names, picture_names_new)
    #     list_of_images.append(index[1])
    #     mambo.hover()

    #         #get the right picture
    #     picture_name=is_in_the_list(picture_names,picture_names_new)[1]
    #     print(picture_name)
    #     #filename=input("Filename ?")
    #     # filename="img20.jpg"


    #     frame = mambo.groundcam.get_groundcam_picture(list_of_images[c],True)
    #     path = sys.path[0]
    #     print(path)

    #     if (frame is not None):
    #         filename = "test_image_%02d.png" % c
    #         # cv2.imwrite(path + '//' + filename, frame)
    #         save_picture(mambo,picture_name,path,filename)

    #         picturePath = path + '\\' + filename # symbols.get_path(filename)

    #         if symbols.is_red_square_here(picturePath):
    #             print("There is a red square in this picture")
    #             # expected_direction = 90 + expected_direction
    #             # turn = expected_direction - direction-5
    #             # print('turn\n', turn)
    #             # print('direction\n', direction)
    #             # print('expected_direction\n', expected_direction)
    #             mambo.turn_degrees(170)
    #             mambo.smart_sleep(1)
    #             mambo.fly_direct(0,15,0,0,duration=1)
    #             direction = mambo.sensors.get_estimated_z_orientation()
    #             x = x + dist*math.sin(math.radians(direction))
    #             y = y + dist*math.cos(math.radians(direction))
    #             # increment coordinates
    #             mambo.hover()
    #         # elif symbols.is_green_square_here(picturePath):
    #         #     print("There is a green square in this picture")
    #         #     mambo.turn_degrees(90)
    #         #     mambo.fly_direct(0,20,0,0,duration=1)
    #         #     # increment coordinates
    #         #     mambo.hover()
    #         else:
    #             mambo.fly_direct(0,15,0,0,duration=1)
    #             mambo.hover()
    #             direction = mambo.sensors.get_estimated_z_orientation()
    #             x = x + dist*math.sin(math.radians(direction))
    #             y = y + dist*math.cos(math.radians(direction))
    #         # filename = "contour_image_%02d.png" % c
    #         # contour = symbols.draw_contour(picturePath)
    #         # cv2.imwrite(path+ '\\' +filename, contour)
    #         # save_picture(mambo,picture_name,path,filename)

    #         c = c+1
    #     if c > 20:
    #         flying = False
    #         break

    #     # z = MinidroneSensors.altitude()
    #     # print("\nz: ", z)
    #     print("\nheading: ", direction)
        
    #     if frame is not None:
    #         if frame is not False:
    #             # cv2.imshow("Groundcam", frame)
    #             cv2.waitKey(4000)
    #             cv2.destroyAllWindows()
    # print(coords)

if __name__ == "__main__":
    main()