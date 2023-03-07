"""
ENGO 531: Lab #1 - Bundle Adjustment Software Development
 Authors: Claire Mah, Seema Mustaqeem and Mabel Heffring
    Date: October 11, 2022
    File: main.py 
"""
# from pickle import FALSE, TRUE
import calc_coll_pds_misc as calc
import read_inputs as input
import lsa
import pandas as pd 
import math 
import numpy.linalg as mat
import numpy as np
import sys

def main():
    # input test data
    input_path=sys.path[0]
    lab_num = "\\files\\engo531_lab1"
    data_int,data_ext,data_pho,data_tie,data_con = input.read(input_path,lab_num)
    data_pho_in=data_pho.copy(deep=True)
    data_con_in=data_con.copy(deep=True)
    data_tie_in=data_tie.copy(deep=True)
    data_ext_in=data_ext.copy(deep=True)
    data_int_in=data_int.copy(deep=True)

    #standard deviation of observations (should probably not be hard coded lol)
    pho_std = 5.0
    con_std= 5.0
    pho_std_array= [pho_std for i in range(len(data_pho))] 
    con_std_array= [con_std for i in range(len(data_con))] 

    data_pho_in.insert(loc=4,column="sd x",value=pho_std_array)
    data_pho_in.insert(loc=5,column="sd y",value=pho_std_array)
    data_con_in.insert(loc=4,column="sd X",value=con_std_array)
    data_con_in.insert(loc=5,column="sd Y",value=con_std_array)
    data_con_in.insert(loc=6,column="sd Z",value=con_std_array)

    outfile=sys.path[0]+"\\output_file.txt"

    data_gcps_in= [data_con, data_tie]
    data_gcps_in = pd.concat(data_gcps_in)

    confidence=0.001

    #First iteration
    keepgoing = True
    delta,data_ext_adj,data_tie_adj,data_con_adj,v_obs,A,P,n,no,uo,ue,norm,gcp_ids,Po=lsa.adjust(data_int,data_ext,data_pho,data_tie,data_con,pho_std,con_std,data_gcps_in)
    num_iter=1
    print(delta)

    # Continue iterating (need to fix tolerance)
    tolerance = 0.0001
    while keepgoing == True:
    #for i in range(3):
        delta,data_ext_adj,data_tie_adj,data_con_adj,v_obs,A,P,n,no,uo,ue,norm,gcp_ids,Po=lsa.adjust(data_int,data_ext_adj,data_pho,data_tie_adj,data_con_adj,pho_std,con_std,data_gcps_in)
        keepgoing = False
        print(delta)
        num_iter=num_iter+1
        for i in range(len(delta)):
            if abs(delta[i]) > tolerance:
                keepgoing = True
    

    #print("# of iterations:  \n",num_iter)

    df,data_pho_adj, data_con_adj, data_tie_adj, data_ext_adj, data_pho_res, data_con_res, apost, r, ttest,Cx_eops = lsa.postprocess(norm,A,P,v_obs,data_pho,data_ext_adj,data_tie_adj,data_con_adj,n,no,uo,ue,gcp_ids,Po,confidence,pho_std,con_std)
    
    #print("data_ext_adj:  \n", data_ext_adj)
    #print("")
    #print("data_con_adj : \n", data_con_adj)
    #print("")
    #print("data_tie_adj : \n", data_tie_adj)
    #print("")
    #print("data_pho_adj : \n", data_pho_adj)
    #print("")
    #print("data_pho_res : \n", data_pho_res)
    #print("")
    #print("data_con_res : \n", data_con_res)
    #print("")
    #print("aposteriori : \n", apost)
    #print("")
    #print("df:   \n", df)
    #print("total redundancy:  \n",r)
    lsa.output_file(outfile,num_iter,tolerance,df,r,n,no,uo,ue,confidence,ttest,apost,data_pho_in,data_con_in,data_tie_in,data_ext_in,data_int_in,data_pho_adj, data_con_adj, data_tie_adj, data_ext_adj, data_pho_res, data_con_res, Cx_eops)
    print("Program completed successfully.")


if __name__ == "__main__":
    main()