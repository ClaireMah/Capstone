import cv2
import numpy as np
# import cv2.aruco as aruco
import inspect
from os.path import join
import argparse
import imutils
import matplotlib.pyplot as plt
from random import *
from pyparrot.Minidrone import Mambo
from pyparrot.DroneVisionGUI import DroneVisionGUI
import os
import shutil


# set this to true if you want to fly for the demo
testFlying = True

def we_are_here():
    return os.getcwd()

def get_path(filename):
    fullPath = inspect.getfile(we_are_here)
    shortPathIndex = fullPath.rfind("/")
    if (shortPathIndex == -1):
        # handle Windows paths
        shortPathIndex = fullPath.rfind("\\")
    Path = fullPath[0:shortPathIndex]
    picturesPath = join(Path, filename)
    return picturesPath
class UserVision:
    def __init__(self, vision):
        self.index = 0
        self.vision = vision

    def save_pictures(self, args):
        # print("in save pictures on image %d " % self.index)

        img = self.vision.get_latest_valid_picture()

        if (img is not None):
            filename = "test_image_%06d.png" % self.index
            # uncomment this if you want to write out images every time you get a new one
            #cv2.imwrite(filename, img)
            self.index +=1
            #print(self.index)

#Class Shapedetector
class ShapeDetector:
    def __init__(self):
        pass
    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        #print(len(approx))
        # if the shape is a triangle, it will have 3 vertices
        if len(approx) ==3:
            shape = "triangle"
        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"
        elif len(approx) == 6:
            shape = "hexagon"
        elif len(approx) == 10:
            shape = "star"
        elif len(approx) == 12:
            shape="cross"
            #print("it's a cross")
        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"
        # return the name of the shape
        return shape

def is_red_cross_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,200,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        print(shape)
        if shape=="cross":
            cimg = np.zeros_like(image)
            cv2.drawContours(cimg, [c], 0, (255, 255, 255), 5)
            pts = np.where(cimg == 255)
            mask1 = cv2.inRange(image, (50, 0, 0), (255, 50, 50))
            print(mask1[pts[0][0]][pts[1][0]])

            for i in range(0,len(pts[0]),100):
                for j in range(0,len(pts[1]),100):
                    #print(i,j)
                    if mask1[pts[0][i]][pts[1][j]]==255:
                        cv2.drawContours(image, [c], 0, (255, 255, 255), 5)
                        cv2.imshow("cross",image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return True
    return False

def is_green_cross_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,200,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        print(shape)
        if shape=="cross":
            cimg = np.zeros_like(image)
            cv2.drawContours(cimg, [c], 0, (255, 255, 255), 5)
            pts = np.where(cimg == 255)
            mask1 = cv2.inRange(image, (0, 50, 0), (50, 255,50))
            print(mask1[pts[0][0]][pts[1][0]])
            print(image[pts[0][100]][pts[1][100]])

            for i in range(0,len(pts[0]),100):
                for j in range(0,len(pts[1]),100):
                    #print(i,j)
                    if mask1[pts[0][i]][pts[1][j]]==255:
                        cv2.drawContours(image, [c], 0, (255, 255, 255), 5)
                        cv2.imshow("cross",image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return True
    return False

def is_blue_cross_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,100,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        print(shape)
        if shape=="cross":
            cimg = np.zeros_like(image)
            cv2.drawContours(cimg, [c], 0, (255, 255, 255), 5)
            pts = np.where(cimg == 255)
            mask1 = cv2.inRange(image, (0, 0, 50), (50, 50, 255))
            print(mask1[pts[0][0]][pts[1][0]])
            print(len(pts[0]))
            print(len(pts[1]))

            for i in range(0,len(pts[0]),100):
                for j in range(0,len(pts[1]),100):
                    #print(i,j)
                    if mask1[pts[0][i]][pts[1][j]]==255:
                        cv2.drawContours(image, [c], 0, (255, 255, 255), 5)
                        cv2.imshow("cross",image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return True
    return False


def is_blue_hexagon_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,100,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        print(shape)
        if shape=="hexagon":
            cimg = np.zeros_like(image)
            cv2.drawContours(cimg, [c], 0, (255, 255, 255), 5)
            pts = np.where(cimg == 255)
            mask1 = cv2.inRange(image, (0, 0, 50), (50, 50, 255))
            # print(mask1[pts[0][0]][pts[1][0]])
            # print(len(pts[0]))
            # print(len(pts[1]))

            for i in range(0,len(pts[0]),100):
                for j in range(0,len(pts[1]),100):
                    #print(i,j)
                    if mask1[pts[0][i]][pts[1][j]]==255:
                        print(image[pts[0][i]][pts[1][j]])
                        cv2.drawContours(image, [c], 0, (255, 255, 255), 5)
                        cv2.imshow(shape,image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return True
    return False

def is_blue_square_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,100,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        print(shape)
        if shape=="square" or shape=="rectangle":
            cimg = np.zeros_like(image)
            cv2.drawContours(cimg, [c], 0, (255, 255, 255), 5)
            pts = np.where(cimg == 255)
            mask1 = cv2.inRange(image, (0, 0, 50), (50, 50, 255))
            print(mask1[pts[0][0]][pts[1][0]])
            # print(len(pts[0]))
            # print(len(pts[1]))

            for i in range(0,len(pts[0]),100):
                for j in range(0,len(pts[1]),100):
                    #print(i,j)
                    if mask1[pts[0][i]][pts[1][j]]==255:
                        cv2.drawContours(image, [c], 0, (255, 255, 255), 5)
                        cv2.imshow(shape,image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return True
    return False


def is_red_square_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,100,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        print(shape)
        if shape=="square" or shape=="rectangle":
            cimg = np.zeros_like(image)
            cv2.drawContours(cimg, [c], 0, (255, 255, 255), 5)
            pts = np.where(cimg == 255)
            mask1 = cv2.inRange(image, (50, 0, 0), (255, 50, 50))
            print(mask1[pts[0][0]][pts[1][0]])
            print(len(pts[0]))
            print(len(pts[1]))

            for i in range(0,len(pts[0]),100):
                for j in range(0,len(pts[1]),100):
                    #print(i,j)
                    if mask1[pts[0][i]][pts[1][j]]==255:
                        cv2.drawContours(image, [c], 0, (255, 255, 255), 5)
                        cv2.imshow(shape,image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return True
    return False

def is_green_square_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,100,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        print(shape)
        if shape=="square" or shape=="rectangle":
            cimg = np.zeros_like(image)
            cv2.drawContours(cimg, [c], 0, (255, 255, 255), 5)
            pts = np.where(cimg == 255)
            mask1 = cv2.inRange(image, (0, 50, 0), (200, 255,200))
            print(mask1[pts[0][0]][pts[1][0]])
            print(len(pts[0]))
            print(len(pts[1]))

            for i in range(0,len(pts[0]),100):
                for j in range(0,len(pts[1]),100):
                    #print(i,j)
                    if mask1[pts[0][i]][pts[1][j]]==255:
                        cv2.drawContours(image, [c], 0, (255, 255, 255), 5)
                        cv2.imshow(shape,image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return True
    return False

def is_red_triangle_here(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,100,400)
    cnts = cv2.findContours(edge_image, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    for c in cnts:
        #detect shape from contour
        shape = sd.detect(c)
        print(shape)
        if shape=="triangle":
            cimg = np.zeros_like(image)
            cv2.drawContours(cimg, [c], 0, (255, 255, 255), 5)
            pts = np.where(cimg == 255)
            mask1 = cv2.inRange(image, (50, 0, 0), (255, 50, 50))

            for i in range(0,len(pts[0]),100):
                for j in range(0,len(pts[1]),100):
                    #print(i,j)
                    if mask1[pts[0][i]][pts[1][j]]==255:
                        cv2.drawContours(image, [c], 0, (255, 255, 255), 5)
                        cv2.imshow(shape,image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return True
    return False


def draw_contour(picturepath):
    image=cv2.imread(picturepath)
    edge_image=cv2.Canny(image,100,400)
    cv2.imshow("cross_edge",edge_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    contours,_=cv2.findContours( edge_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        cv2.drawContours(image, [contour], 0, (0, 0, 255), 5)
    cv2.imshow("cross_edge_contours",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def demo_mambo_user_vision_function(mamboVision, args):
    """
    Demo the user code to run with the run button for a mambo

    :param args:
    :return:
    """
    mambo = args[0]

    if (testFlying):
        print("taking off!")
        mambo.safe_takeoff(5)

        if (mambo.sensors.flying_state != "emergency"):
            #mambo.smart_sleep(2)
            filename="color10.png"
            img=userVision.vision.get_latest_valid_picture()
            cv2.imwrite(filename,img)
            file_source=join(we_are_here(),filename)
            file_destination=get_path(filename)
            shutil.move(file_source, file_destination)
            picturePath=get_path(filename)
            draw_contour(picturePath)
            cv2.imshow("Image", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            c=0

            #processing the picture
            if is_red_cross_here(picturePath):
                print("There is a red cross in this picture ")
                c=c+1

            if is_green_cross_here(picturePath):
                print("There is a green cross in this picture ")
                c=c+1

            if is_green_square_here(picturePath):
                print("There is red square or rectangle in this picture")
                c=c+1

            if is_blue_cross_here(picturePath):
                print("There is a blue cross in this picture ")
                c=c+1

            if is_blue_square_here(picturePath):
                print("There is a blue square or rectangle in this picture")
                c=c+1

            if is_red_triangle_here(picturePath):
                print("There is a red triangle is this picture")
                c=c+1


            if c==0:
                print("Impossible to determine what is on this picture")
                #mambo.flip(direction='left')

            mambo.smart_sleep(2)


        print("landing")
        print("flying state is %s" % mambo.sensors.flying_state)
        mambo.safe_land(5)
    else:
        print("Sleeeping for 15 seconds - move the mambo around")
        mambo.smart_sleep(15)

    # done doing vision demo
    print("Ending the sleep and vision")
    mamboVision.close_video()

    mambo.smart_sleep(5)

    print("disconnecting")
    mambo.disconnect()


if __name__ == "__main__":

    # make my mambo object
    # remember to set True/False for the wifi depending on if you are using the wifi or the BLE to connect
    mambo = Mambo(None, use_wifi=True)
    print("trying to connect to mambo now")
    success = mambo.connect(num_retries=3)
    print("connected: %s" % success)

    if (success):
        # get the state information
        print("sleeping")
        mambo.smart_sleep(1)
        mambo.ask_for_state_update()
        mambo.smart_sleep(1)

        print("Preparing to open vision")
        mamboVision = DroneVisionGUI(mambo, is_bebop=False, buffer_size=200,
                                     user_code_to_run=demo_mambo_user_vision_function, user_args=(mambo, ))
        userVision = UserVision(mamboVision)
        mamboVision.set_user_callback_function(userVision.save_pictures, user_callback_args=None)
        mamboVision.open_video()