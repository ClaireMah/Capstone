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
    # data_out = pd.read_csv(path+lab_num+".int", delim_whitespace=True, header=None, engine='python')
    # data_out.columns = ["col1", "col2", "col3", "col4"]
    data_con = pd.read_csv(path+lab_num+".con", delim_whitespace=True, header=None, engine='python')
    data_con.columns = ["Point", "X", "Y", "Z"]
    
    #print('\nint: \n',data_int)
    #print('\next: \n',data_ext)
    #print('\npho: \n',data_pho)
    #print('\ntie: \n',data_tie)
    #print('\ncon: \n',data_con, '\n\n')
    return data_int,data_ext,data_pho,data_tie,data_con