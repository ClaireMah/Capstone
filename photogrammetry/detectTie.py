import cv2
import imutils
import numpy as np
import symbols
from PIL import Image
import os
from pathlib import Path


def detectTie(main_folder,output_file):
    #Inspired by: https://pyimagesearch.com/2016/02/01/opencv-center-of-contour/

    pho_mat=np.empty((0,4),int)

    img_folder=main_folder+"\\img\\"
    for name in os.listdir(img_folder):
        image_file=img_folder+name
        image_num=name[0]
        print("Image:  "+image_num)

        image = cv2.imread(image_file)
        image_control=np.copy(image)
        image_tie=np.copy(image)
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        #blurred=image

        #thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
        #thresh=cv2.inRange(blurred,(0, 50, 0), (110, 255,110))
        thresh=cv2.inRange(blurred,(0, 50, 0), (180, 255,180))
        #thresh = cv2.bitwise_not(thresh)-1
        cv2.imwrite(main_folder+"\\mask"+image_num+".jpg",thresh)

        #edge_image=cv2.Canny(thresh,200,400)
        edge_image=thresh
        cnts = cv2.findContours(edge_image.copy(), cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE)
        #cnts=draw_contour(image_file)
        cnts = imutils.grab_contours(cnts)

        sd = symbols.ShapeDetector()

        for c in cnts:
            shape = sd.detect(c)

            if shape=="circle":
                M=cv2.moments(c)

                #print(M["m00"])
                if M["m00"]<500 or M["m00"]>200000:
                    continue
                #print(M["m00"])

                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                cv2.drawContours(image, [c], -1, (255, 0, 0), 2)
                cv2.circle(image, (cX, cY), 2, (0, 0, 0), -1)
                cv2.putText(image, "("+str(cX)+","+str(cY)+")", (cX, cY-10),
                    cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0), 2)

                window=100
                minx=cX-window
                if minx<0:
                    minx=0
                maxx=cX+window
                if maxx>image.shape[1]-1:
                    maxx=image.shape[1]-1
                miny=cY-window
                if miny<0:
                    miny=0
                maxy=cY+window
                if maxy>image.shape[0]-1:
                    maxy=image.shape[0]-1

                cropped_image = image[miny:maxy, minx:maxx]
                cv2.imshow("cropped", cropped_image)
                cv2.waitKey(0)

                id=float(input("Point ID:"))

                if id<1:
                    continue

                cv2.drawContours(image_tie, [c], -1, (255, 0, 0), 2)
                cv2.circle(image_tie, (cX, cY), 2, (0, 0, 0), -1)
                cv2.putText(image_tie, "("+str(cX)+","+str(cY)+")", (cX, cY-10),
                    cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0), 2)
                
                pho_mat = np.append(pho_mat, np.array([[int(id),image_num,cX,cY]]), axis=0)
            
            elif shape=="square" or shape=="rectangle":
                M=cv2.moments(c)

                #print(M["m00"])
                if M["m00"]<500 or M["m00"]>200000:
                    continue
                #print(M["m00"])

                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                cv2.drawContours(image, [c], -1, (255, 0, 0), 2)
                cv2.circle(image, (cX, cY), 2, (0, 0, 0), -1)
                cv2.putText(image, "("+str(cX)+","+str(cY)+")", (cX, cY-10),
                    cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0), 2)
        
                window=100
                minx=cX-window
                if minx<0:
                    minx=0
                maxx=cX+window
                if maxx>image.shape[1]-1:
                    maxx=image.shape[1]-1
                miny=cY-window
                if miny<0:
                    miny=0
                maxy=cY+window
                if maxy>image.shape[0]-1:
                    maxy=image.shape[0]-1

                cropped_image = image[miny:maxy, minx:maxx]
                cv2.imshow("cropped", cropped_image)
                cv2.waitKey(0)

                id=float(input("Point ID:"))

                if id<1:
                    continue
                cv2.drawContours(image_control, [c], -1, (255, 0, 0), 2)
                cv2.circle(image_control, (cX, cY), 2, (0, 0, 0), -1)
                cv2.putText(image_control, "("+str(cX)+","+str(cY)+")", (cX, cY-10),
                    cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0), 2)
                
                pho_mat = np.append(pho_mat, np.array([[int(id),image_num,cX,cY]]), axis=0)

        cv2.imwrite(main_folder+"\\tie"+image_num+".jpg",image_tie)
        cv2.imwrite(main_folder+"\\control"+image_num+".jpg",image_control)
        cv2.imwrite(main_folder+"\\all"+image_num+".jpg",image)
        np.savetxt(output_file, pho_mat, fmt='%s')


out="C:\\Users\\mabel\\OneDrive\\Desktop\\Year 4\\ENGO 500\\tie_point_detection\\photo.pho"
folder="C:\\Users\\mabel\\OneDrive\\Desktop\\Year 4\\ENGO 500\\tie_point_detection\\"
detectTie(folder,out)