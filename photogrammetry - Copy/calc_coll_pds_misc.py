import pandas as pd 
import math 
import numpy.linalg as mat
import numpy as np

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def tan(x):
    return math.tan(math.radians(x))


def calc_coll_pds_misc(XYZc,wpk,XYZ,xpypc,xy_obs,lhs):
# function to compute the partial derivatives of the collinearity equations
# and the misclosure elements
# 
# Derek Lichti, The University of Calgary 2022
#
# INPUTS:
#   XYZc        3x1 vector of perspective centre coordinates
#               usually in mm or m
#   wpk         3x1 vector of rotation angles in radians
#   XYZ         3x1 vector object point (tie or control) coordinates
#               usually in mm or m (same units as XYZc)
#   xpypc       3x1 basic IOPs: principal point and principal distance
#               usually in mm, um or pixels
#               shoudl have the same units as the image point observations
#   xy_obs      2x1 vector of observations
#               usually in mm, um or pixels
#               shoudl have the same units as the basic IOPs
# OUTPUTS:
#   ae_2x6      2x6 matrix of partial derivatives wrt the EOPs
#               column order: Xc Yc Zc w p k
#               row order: x y
#   ao_2x3      2x3 matrix of partial derivatives wrt the object point
#               coordinates
#               column order: X Y Z
#               row order: x y
#   ai_2x3      2x3 matrix of partial derivatives wrt the IOPs
#               column order: xp yp c
#               row order: x y
#   w_2x1       2x1 vector of misclosures (computed x,y - observed x,y)
#               row order: x y
#               units: mm, um or pixels

    if lhs == True:
        K=-1
    else:
        K=1


    # compute M
    w=wpk.iloc[0,0]
    p=wpk.iloc[1,0]
    k=wpk.iloc[2,0]

    R1 = pd.DataFrame([[1, 0, 0], [0, cos(w), sin(w)], [0, -sin(w), cos(w)]])
    R2 = pd.DataFrame([[cos(p), 0, -sin(p)], [0, 1, 0], [sin(p), 0, cos(p)]])
    R3 = pd.DataFrame([[cos(k), sin(k), 0], [-sin(k), cos(k), 0], [0, 0, 1 ]])

    # print(R1)

    M = pd.DataFrame(np.matmul(np.matmul(R3,R2),R1))

    # compute UVW
    dXYZ = pd.DataFrame(XYZ-XYZc)
    UVW = np.matmul(M,np.asarray(dXYZ))
    U = UVW.iloc[0,0]
    V = UVW.iloc[1,0]
    W = UVW.iloc[2,0]

    # compute misclosure
    xp=xpypc.iloc[0,0]
    yp=xpypc.iloc[1,0]
    c=xpypc.iloc[2,0]
    x_comp=xp-c*U/W
    y_comp=yp-c*V/W*K

    w_2x1 = pd.DataFrame([ x_comp-xy_obs[0][0],  y_comp-xy_obs[0][1]])

    # print(w_2x1)
    ae_2x6 = pd.DataFrame()
    # EOP PDs
    ae_2x6.loc[0,0] = -c/(W*W)*(M.iloc[2,0]*U-M.iloc[0,0]*W)
    ae_2x6.loc[0,1] = -c/(W*W)*(M.iloc[2,1]*U-M.iloc[0,1]*W)
    ae_2x6.loc[0,2] = -c/(W*W)*(M.iloc[2,2]*U-M.iloc[0,2]*W)

    ae_2x6.loc[0,3]=-c/(W*W)*(dXYZ.iloc[1,0]*(U*M.iloc[2,2]-W*M.iloc[0,2])-dXYZ.iloc[2,0]*(U*M.iloc[2,1]-W*M.iloc[0,1]))
    ae_2x6.loc[0,4]=-c/(W*W)*(dXYZ.iloc[0,0]*(-W*sin(p)*cos(k)-U*cos(p))+dXYZ.iloc[1,0]*(W*sin(w)*cos(p)*cos(k)-U*sin(w)*sin(p))+dXYZ.iloc[2,0]*(-W*cos(w)*cos(p)*cos(k)+U*cos(w)*sin(p)))
    # ae_2x6(1,5)=-c/UVW(3)^2*(dXYZ(1)*(-UVW(3)*sin(p)*cos(k)-UVW(1)*cos(p))+dXYZ(2)*(UVW(3)*sin(w)*cos(p)*cos(k)-UVW(1)*sin(w)*sin(p))+dXYZ(3)*(-UVW(3)*cos(w)*cos(p)*cos(k)+UVW(1)*cos(w)*sin(p)));
    ae_2x6.loc[0,5]=-c*V/W

    ae_2x6.loc[1,0]=K*(-c/(W*W)*(M.iloc[2,0]*V-M.iloc[1,0]*W))
    ae_2x6.loc[1,1]=K*(-c/(W*W)*(M.iloc[2,1]*V-M.iloc[1,1]*W))
    ae_2x6.loc[1,2]=K*(-c/(W*W)*(M.iloc[2,2]*V-M.iloc[1,2]*W))

    ae_2x6.loc[1,3]=K*(-c/(W*W)*(dXYZ.iloc[1,0]*(V*M.iloc[2,2]-W*M.iloc[1,2])-dXYZ.iloc[2,0]*(V*M.iloc[2,1]-W*M.iloc[1,1])))
    # ae_2x6.loc[1,4]=-c/(W*W)*(dXYZ.iloc[0,0]*(W*sin(p)*sin(k)-V*cos(p))+dXYZ.iloc[1,0]*(-W*sin(w)*cos(p)*sin(k)-V*sin(w)*sin(p))+dXYZ.iloc[2,0]*(W*cos(w)*cos(p)*sin(k)+V*cos(w)*sin(p)))
    ae_2x6.loc[1,4]=K*(-c/(W*W)*(dXYZ.iloc[0,0]*(W*sin(p)*sin(k)-V*cos(p))+dXYZ.iloc[1,0]*(-W*sin(w)*cos(p)*sin(k)-V*sin(w)*sin(p))+dXYZ.iloc[2,0]*(W*cos(w)*cos(p)*sin(k)+V*cos(w)*sin(p))))
    ae_2x6.loc[1,5]=K*(c*U/W)
    # print(ae_2x6)

    # object point PDs
    ao_2x3=-ae_2x6.iloc[:,0:3]
    # print(ao_2x3)

    # IOP PDs
    ai_2x3 = pd.DataFrame([[1, 0, -U/W], [0, 1, -V/W*K]])
    # print(ai_2x3)

    return ae_2x6,ao_2x3,ai_2x3,w_2x1

