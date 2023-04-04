"""
ENGO 531: Lab #1 - Bundle Adjustment Software Development
 Authors: Claire Mah, Seema Mustaqeem and Mabel Heffring
    Date: October 11, 2022
    File: read_inputs.py
"""
import calc_coll_pds_misc as calc
import pandas as pd 
import math 
import numpy.linalg as mat
import numpy as np
import sys

# A function to read the input lab data
def read(path,lab_num):
    # path = sys.path[0] 
    # lab_num = "\\files\\engo531_lab1"
    data_int = pd.read_csv(path+lab_num+".int", delim_whitespace=True, header=None, engine='python')
    data_int.columns = ["camera", "xp", "yp", "c"]
    data_ext = pd.read_csv(path+lab_num+".ext", delim_whitespace=True, header=None, engine='python')
    data_ext.columns = ["image", "camera", "Xc", "Yc", "Zc", "omega", "phi", "kappa"]
    data_pho = pd.read_csv(path+lab_num+".pho", delim_whitespace=True, header=None, engine='python')
    data_pho.columns = ["point", "image", "x", "y"]
    data_tie = pd.read_csv(path+lab_num+".tie", delim_whitespace=True, header=None, engine='python')
    data_tie.columns = ["Point", "X", "Y", "Z"]
    data_con = pd.read_csv(path+lab_num+".con", delim_whitespace=True, header=None, engine='python')
    data_con.columns = ["Point", "X", "Y", "Z"]
    
    #List of points to remove
    # data_pho=data_pho.loc[~data_pho["point"].isin([1])]

    #list of images to remove
    # data_ext=data_ext.loc[~data_ext["image"].isin([3])]
    # data_pho=data_pho.loc[~data_pho["image"].isin([3])]
    
    #list of images to include
    data_ext=data_ext.loc[data_ext["image"].isin([0,2,6,8,10,19,21,25])] #0,2,4,6,8,10,19,21,25
    data_pho=data_pho.loc[data_pho["image"].isin([0,2,6,8,10,19,21,25])]

    pho_ids=data_pho['point'].unique()
    pho_ids.sort()

    # for i in pho_ids:
    #     temp = data_pho.loc[data_pho["point"] == i]
    #     # Filter points that are observed in less than 3 images 
    #     if len(temp) < 3:
    #         data_pho = data_pho.loc[data_pho["point"]!=i]
    # # Filter any duplicate observations
    # data_pho = data_pho.drop_duplicates(subset=["point","image"])

    for i in range(len(data_ext)):
        # data_ext.iloc[i,7] = data_ext.iloc[i,7]+90                  #Use to change Kappa angles
        if data_ext.iloc[i,7] >360:
            data_ext.iloc[i,7] = data_ext.iloc[i,7]-360
        elif data_ext.iloc[i,7] < 0:
            data_ext.iloc[i,7] = data_ext.iloc[i,7]+360
    
    # for i in range(len(data_con)):
    #     temp = data_con.loc[i,'X']
    #     data_con.loc[i,'X'] = -data_con.loc[i,'Y']
    #     data_con.loc[i,'Y'] = temp


    #make sure all input files match
    data_ext = data_ext.loc[data_ext['image'].isin(data_pho['image'])]

    data_con = data_con.loc[data_con["Point"].isin(data_pho["point"])]

    data_pho = data_pho.loc[data_pho["point"].isin(data_tie["Point"])]

    # Clean up tie points, remove points not present in observations, remove points that are used as control
    data_tie_clean = data_tie
    data_tie_clean = data_tie.loc[data_tie["Point"].isin(data_pho["point"])]
    data_tie_clean = data_tie_clean.loc[~data_tie["Point"].isin(data_con["Point"])]
    data_tie = pd.DataFrame(data_tie_clean).reset_index(drop=True)
    data_pho = data_pho.reset_index(drop=True)
    data_ext = data_ext.reset_index(drop=True)
    data_con = data_con.reset_index(drop=True)

    print('\nint: \n',data_int)
    print('\next: \n',data_ext)
    print('\npho: \n',data_pho)
    print('\ntie: \n',data_tie)
    print('\ncon: \n',data_con, '\n\n')
    return data_int,data_ext,data_pho,data_tie,data_con