"""
ENGO 531: Lab #1 - Bundle Adjustment Software Development
 Authors: Claire Mah, Seema Mustaqeem and Mabel Heffring
    Date: October 11, 2022
    File: lsa.py
"""
#from typing import Concatenate
import calc_coll_pds_misc as calc
import read_inputs as input
import pandas as pd 
import math 
import numpy.linalg as mat
import numpy as np
import sys
from scipy import stats as s
from tabulate import tabulate
import statistics as stat

# A function to calculate Ae, Ao, A, w, and P for LSA
def adjust(data_int,data_ext,data_pho,data_tie,data_con,pho_std,con_std,data_gcps_in):
    print("Adjusting.... \n")
    # Image IDs and number of images in adjustment check
    img_ids_ext = data_ext['image'].unique()
    img_ids_pho = data_pho['image'].unique()
    if np.array_equal(np.sort(img_ids_ext), np.sort(img_ids_pho))==False:
        sys.exit("ERROR: Image IDs in PHO and EXT do not match!")
    else:
        num_img= len(img_ids_ext)
        img_ids= img_ids_ext
    

    # Camera IDs and number of cameras in adjustment check
    cam_ids_ext = data_ext['camera'].unique()
    cam_ids_int = data_int['camera'].unique()
    if np.array_equal(np.sort(cam_ids_ext), np.sort(cam_ids_int))==False:
        sys.exit("ERROR: Camera IDs in INT and EXT do not match!")
    else:
        num_cam= len(cam_ids_ext)
        cam_ids= cam_ids_ext
    
    # Number of Observations, Control Points and Tie Points
    pho_ids=data_pho['point'].unique()
    pho_ids.sort()
    num_pho=len(data_pho)
    con_ids=data_con['Point'].unique()
    con_ids.sort()
    num_con=len(con_ids)
    tie_ids=data_tie['Point'].unique()
    tie_ids.sort()
    num_tie=len(tie_ids)
    gcp_ids = np.concatenate((con_ids, tie_ids), axis = 0)
    gcp_ids.sort()

    # Initializing matrices for P, w, Ae and Ao
    n = 2 * num_pho
    ue = 6 * num_img
    uo = 3 * (num_con + num_tie)
    no = 3 * num_con

    Ae = np.zeros((n,ue))
    Ao = np.zeros((n,uo))
    w = np.zeros((n,1))
    wo = np.zeros((uo,1))
    P = np.zeros((n,n))
    Po = np.zeros((uo,uo))

    print('\nn : ', n+no)
    print('\nu : ', ue+uo)


    # Populating P
    np.fill_diagonal(P,(1/(pho_std*pho_std)))

    # Populate wo
    data_gcps_now=data_con
    for gcp in range(len(data_gcps_now)):
        current_xo=data_gcps_now.iloc[gcp,:]
        current_obs_in=data_gcps_in.loc[data_gcps_in['Point']==current_xo['Point']]
        diff_X=current_xo['X']-current_obs_in['X']
        diff_Y=current_xo['Y']-current_obs_in['Y']
        diff_Z=current_xo['Z']-current_obs_in['Z']
        wo_idx=np.where(gcp_ids==current_xo['Point'])
        wo_idx=wo_idx[0][0]*3
        wo[wo_idx]=diff_X
        wo[wo_idx+1]=diff_Y
        wo[wo_idx+2]=diff_Z 

    # loop through all observations in PHO to fill w, Ae, Ao and Po
    for i in range(len(data_pho)):
        #collecting data corresponding to observation
        current_obs=data_pho.iloc[i,:]
        current_img=current_obs['image']
        point=current_obs['point']
        EOPS=data_ext.loc[data_ext['image']==current_img]
        EOPS=EOPS.reset_index(drop=True)
        data_int=data_int.reset_index(drop=True)
        current_cam=EOPS['camera']
        IOPS=data_int.loc[data_int['camera']==current_cam]
        object_point=data_con.loc[data_con['Point']==point].reset_index(drop=True)
        current_tie=data_tie.loc[data_tie['Point']==point].reset_index(drop=True)

        # Populating Po
        if len(object_point)==0:
            object_point=current_tie
        else:
            idx=np.where(gcp_ids==point)
            idx=idx[0][0]*3
            Po[idx][idx] = 1
            Po[idx+1][idx+1] = 1
            Po[idx+2][idx+2] = 1
    

        # Preparing data for input into calc_coll_pds_misc.py
        om=EOPS.at[0,'omega']
        p=EOPS.at[0,'phi']
        k=EOPS.at[0,'kappa']
        XYZc = pd.DataFrame([[EOPS.at[0,'Xc']], [EOPS.at[0,'Yc']], [EOPS.at[0,'Zc']]])
        wpk = pd.DataFrame([[om],[p],[k]])
        XYZ = pd.DataFrame([[object_point.at[0,'X']], [object_point.at[0,'Y']], [object_point.at[0,'Z']]])
        xpypc = pd.DataFrame([[IOPS.at[0,'xp']], [IOPS.at[0,'yp']], [IOPS.at[0,'c']]])
        xy_obs = pd.DataFrame([[current_obs['x']], [current_obs['y']]])

        ae_2x6,ao_2x3,ai_2x3,w_2x1 = calc.calc_coll_pds_misc(XYZc,wpk,XYZ,xpypc,xy_obs,True)

        #Populating w matrix
        obs_index=2*i
        w[obs_index,0]=w_2x1.iloc[0,0]
        w[obs_index+1,0]=w_2x1.iloc[1,0]

        #Populating A matrices
        img_idx=np.where(img_ids==current_img)
        pho_idx=np.where(pho_ids==point)

        img_idx=img_idx[0][0]
        pho_idx=pho_idx[0][0]

        img_start=img_idx*6
        pho_start_obs=pho_idx*3

        for y in range(6):
            for x in range(2):
                Ae[obs_index+x][img_start+y]=ae_2x6.iloc[x][y]
        
        for b in range(3):
            for a in range(2):
                Ao[obs_index+a][pho_start_obs+b]=ao_2x3.iloc[a][b]

    Po=(1/(con_std*con_std))*Po
    #Calculating delta vector
    Ae_trans=np.transpose(Ae)
    Ao_trans=np.transpose(Ao)
    N_left = np.concatenate((np.matmul(np.matmul(Ae_trans,P),Ae), np.matmul(np.matmul(Ao_trans,P),Ae)), axis=0)
    N_right = np.concatenate((np.matmul(np.matmul(Ae_trans,P),Ao), np.matmul(np.matmul(Ao_trans,P),Ao)+Po), axis=0)
    norm = np.concatenate((N_left, N_right), axis = 1)
    A = np.concatenate((Ae,Ao), axis = 1)
    zero = np.zeros((uo,ue))
    I_uouo = np.zeros((uo,uo))
    np.fill_diagonal(I_uouo,1)
    A_lower = np.concatenate((zero, I_uouo),axis=1)
    A = np.concatenate((A,A_lower),axis=0)


    part2_upper = np.matmul(np.matmul(Ae_trans,P),w)
    part2_lower = np.matmul(np.matmul(Ao_trans,P),w)+np.matmul(Po,wo)
    part2 = np.concatenate((part2_upper,part2_lower),axis = 0)
    norm_inv= np.linalg.inv(norm)
    delta=-1*np.matmul(norm_inv,part2)


    data_ext_adj = pd.DataFrame(data_ext)
    data_tie_adj = pd.DataFrame(data_tie)
    data_con_adj = pd.DataFrame(data_con)
    #data_pho_adj = pd.DataFrame(data_pho)


    #Calculating residuals
    w = np.concatenate((w,wo),axis = 0)
    v_obs = np.matmul(A,delta) + w

    # Adjusting the EOPs
    start = 0
    x_int = 0
    for y in range(0,num_img):
        for x in ["Xc", "Yc", "Zc", "omega", "phi", "kappa"]:
            if x in ["Xc", "Yc", "Zc"]:
                data_ext_adj.loc[y,x] = data_ext_adj.loc[y,x]+delta[start+x_int]
            else:
                data_ext_adj.loc[y,x] = data_ext_adj.loc[y,x]+math.degrees(delta[start+x_int])
            x_int = x_int+1


    # Adjusting the control and tie points
    start = start + ue
    x_int = 0
    tie_int = 0 
    con_int = 0 
    for y in gcp_ids:
        if y in con_ids:
            for x in ["X", "Y", "Z"]:
                data_con_adj.loc[con_int,x] = data_con_adj.loc[con_int,x]+delta[start+x_int]
                x_int = x_int+1
            con_int = con_int+1
        elif y in tie_ids:
            for x in ["X", "Y", "Z"]:
                data_tie_adj.loc[tie_int,x] = data_tie_adj.loc[tie_int,x]+delta[start+x_int]
                x_int = x_int+1
            tie_int = tie_int+1
        else:
            exit("ERROR: Point does not exist!")
    
    return delta,data_ext_adj,data_tie_adj,data_con_adj,v_obs,A,P,n,no,uo,ue,norm,gcp_ids,Po

#A function for postprocessing and network assessment after converging
#Returns the following:
#     -   df: degrees of freedom
#     -   data_pho_adj: adjusted x and y observations, standard deviations of adjusted
#     -   data_tie_adj: adjusted tie X,Y,Z, standard deviation of adjusted
#     -   data_con_adj: adjusted con X,Y,Z, standard deviation of adjusted
#     -   data_ext_adj: adjusted EOPs and their corresponding standard deviation
#     -   data_pho_res: photo observation residuals, redundancy, standard deviation, residuals
#     -   data_con_res: photo observation residuals, redundancy, standard deviation, residuals
#     -   apost: A posteriori variance factor
#     -   r: total redundancy
def postprocess(N,A,P,v_obs,data_pho,data_ext_adj,data_tie_adj,data_con_adj,n,no,uo,ue,gcp_ids,Po,confidence,pho_std,con_std):
    # Calcuating total network redundancy
    #   n include observed photo points and control points (for datum definition)
    #   u include unknown tie points and unknown EOPs
    df = (n+no)-(uo+ue)

    # Organizing residuals by photo and control
    v_obs_pho=v_obs[:n]
    v_obs_pho_reshp=np.reshape(v_obs_pho,(int(n/2),2))
    v_obs_con=v_obs[n:]
    gcps_extend=np.zeros((len(gcp_ids)*3,1))
    coords=np.empty((no,1),dtype=str)
    obs_gcps=np.zeros((no,1))
    for i in range(len(gcp_ids)):
        extend_idx=i*3
        gcps_extend[extend_idx]=gcp_ids[i]
        gcps_extend[extend_idx+1]=gcp_ids[i]
        gcps_extend[extend_idx+2]=gcp_ids[i]
    
    for x in range(int(len(coords)/3)):
        current_con=data_con_adj.iloc[x,:]
        curr_point=current_con['Point']
        idx=x*3
        coords[idx]='X'
        coords[idx+1]='Y'
        coords[idx+2]='Z'
        obs_gcps[idx]=curr_point
        obs_gcps[idx+1]=curr_point
        obs_gcps[idx+2]=curr_point

    
    #Adjust photo observations using v
    data_pho_adj=pd.DataFrame(data_pho)
    data_pho_adj['x']=data_pho_adj['x']+v_obs_pho_reshp[:,0]
    data_pho_adj['y']=data_pho_adj['y']+v_obs_pho_reshp[:,1]

    # Forming full P matrix (photo obs and control point obs)
    P_topright=np.zeros((len(P),len(Po[0])))
    P_bottomleft=np.zeros((len(Po),len(P[0])))
    P_top=np.concatenate((P,P_topright),axis = 1)
    P_bottom=np.concatenate((P_bottomleft,Po),axis = 1)
    P_full=np.concatenate((P_top,P_bottom),axis = 0)

    # Forming full Cl matrix (photo obs and control point obs)
    Cl=((pho_std*pho_std)*(pho_std*pho_std))*P
    Clo=((con_std*con_std)*(con_std*con_std))*Po
    Cl_topright=np.zeros((len(Cl),len(Clo[0])))
    Cl_bottomleft=np.zeros((len(Clo),len(Cl[0])))
    Cl_top=np.concatenate((Cl,Cl_topright),axis = 1)
    Cl_bottom=np.concatenate((Cl_bottomleft,Clo),axis = 1)
    Cl_full=np.concatenate((Cl_top,Cl_bottom),axis = 0)

    # Calculating Cx and standard deviations of unknowns
    Cx=np.linalg.inv(N)
    var_x=np.diag(Cx)
    std_x=np.sqrt(var_x)
    std_x_eops=std_x[:ue]
    std_x_obs=std_x[ue:]
    std_x_eops=np.reshape(std_x_eops,(int(ue/6),6))
    std_x_obs=np.reshape(std_x_obs,(int(uo/3),3))

    std_x_obs_df=pd.DataFrame(std_x_obs)
    gcp_ids_df=pd.DataFrame(gcp_ids)
    std_x_obs_df=[gcp_ids_df,std_x_obs_df]
    std_x_obs_df = pd.concat(std_x_obs_df,axis=1)
    std_x_obs_df.columns=["Point", "sd X", "sd Y", "sd Z"]

    std_x_eops[:,3]=std_x_eops[:,3]*(180.0/math.pi)
    std_x_eops[:,4]=std_x_eops[:,4]*(180.0/math.pi)
    std_x_eops[:,5]=std_x_eops[:,5]*(180.0/math.pi)
    std_x_eops_df=pd.DataFrame(std_x_eops)
    std_x_eops_df.columns=["sd Xc", "sd Yc", "sd Zc", "sd omega","sd phi","sd kappa"]

    data_ext_adj=[data_ext_adj,std_x_eops_df.reset_index(drop=True)]
    data_ext_adj=pd.concat(data_ext_adj,axis=1)

    Cx_eops=Cx[:ue,:ue]

    # Adding precisions to data_con_adj and data_tie_adj
    con_ids=data_con_adj['Point']
    tie_ids=data_tie_adj['Point']
    stds_con = std_x_obs_df[std_x_obs_df['Point'].isin(con_ids)].reset_index()
    stds_tie = std_x_obs_df[std_x_obs_df['Point'].isin(tie_ids)].reset_index()
  
    data_con_adj=[data_con_adj,stds_con['sd X'],stds_con['sd Y'],stds_con['sd Z']] 
    data_con_adj=pd.concat(data_con_adj,axis=1)

    data_tie_adj=[data_tie_adj,stds_tie['sd X'],stds_tie['sd Y'],stds_tie['sd Z']] 
    data_tie_adj=pd.concat(data_tie_adj,axis=1)


    # Calculating Cl and standard deviations of adjusted observations
    C_lhat=np.matmul(np.matmul(A,Cx),np.transpose(A))
    var_lhat=np.diag(C_lhat)
    std_lhat=np.sqrt(var_lhat)
    std_lhat_pho=std_lhat[:n]
    std_lhat_pho_reshp=np.reshape(std_lhat_pho,(int(n/2),2))

    #Adding standard deviations of adjusted values to datafram
    data_pho_adj.insert(loc=4, column='sd x',value=std_lhat_pho_reshp[:,0])
    data_pho_adj.insert(loc=5, column='sd y',value=std_lhat_pho_reshp[:,1])


    # Calculating Cv and standard deviations of residuals
    Cv=Cl_full-C_lhat
    var_v=np.diag(Cv)
    std_v=np.sqrt(var_v)
    std_v_pho=std_v[:n]
    std_v_pho_reshp=np.reshape(std_v_pho,(int(n/2),2))
    std_v_con=std_v[n:]

    # Calculating redundancy matrix
    R=np.matmul(Cv,P_full)
    red=np.diag(R)
    r=np.sum(red)
    red_pho=red[:n]
    red_con=red[n:]
    red_pho_reshp=np.reshape(red_pho,(int(n/2),2))
 

    # Building data_pho_res
    data_pho_res=pd.DataFrame(v_obs_pho_reshp)
    data_pho_res.columns=['v x','v y']
    data_pho_res.insert(loc=0,column='point',value=data_pho_adj['point'].values)
    data_pho_res.insert(loc=1,column='image',value=data_pho_adj['image'].values)
    data_pho_res.insert(loc=4,column='r x',value=red_pho_reshp[:,0])
    data_pho_res.insert(loc=5,column='r y',value=red_pho_reshp[:,1])
    data_pho_res.insert(loc=6,column='sd x',value=std_v_pho_reshp[:,0])
    data_pho_res.insert(loc=7,column='sd y',value=std_v_pho_reshp[:,1])
    stand_vx=v_obs_pho_reshp[:,0]/std_v_pho_reshp[:,0]
    stand_vy=v_obs_pho_reshp[:,1]/std_v_pho_reshp[:,1]
    data_pho_res.insert(loc=8,column='w x',value=stand_vx)
    data_pho_res.insert(loc=9,column='w y',value=stand_vy)

    # Building data_con_res
    v_obs_con_filt=[1]
    red_con_filt=[1]
    std_v_con_filt=[1]
    con_ids=data_con_adj['Point']
    for x in range(len(gcps_extend)):
        current_gcp=gcps_extend[x]
        for y in con_ids:
            if int(current_gcp) == y:
                v_obs_con_filt=np.vstack([v_obs_con_filt,v_obs_con[x]])
                red_con_filt=np.vstack([red_con_filt,red_con[x]])
                std_v_con_filt=np.vstack([std_v_con_filt,std_v_con[x]])
    v_obs_con_filt=np.delete(v_obs_con_filt,0)
    red_con_filt=np.delete(red_con_filt,0)
    std_v_con_filt=np.delete(std_v_con_filt,0)
    stand_v_con=v_obs_con_filt/std_v_con_filt
    data_con_res=pd.DataFrame(v_obs_con_filt)
    data_con_res.columns=['v']
    data_con_res.insert(loc=0,column='Point',value=obs_gcps)
    data_con_res.insert(loc=1,column='Param',value=coords)
    data_con_res.insert(loc=3,column='r',value=red_con_filt)
    data_con_res.insert(loc=4,column='sd',value=std_v_con_filt)
    data_con_res.insert(loc=5,column='w',value=stand_v_con)

    # determining confidence level and testing photo observations and control for outliers using standardized residuals
    onetail=confidence/2
    ttest=s.t.ppf((1-onetail), df)

    outlier_pho=np.empty(len(data_pho_res),dtype=str)
    for i in range(len(outlier_pho)):
        current_pho=data_pho_res.iloc[i,:]
        if (abs(current_pho['w x']) > ttest) | (abs(current_pho['w y']) > ttest):
            outlier_pho[i]='Y'
        else:
            outlier_pho[i]='N'

    outlier_con=np.empty(len(data_con_res),dtype=str)
    for i in range(len(outlier_con)):
        current_con=data_con_res.iloc[i,:]
        if abs(current_con['w']) > ttest:
            outlier_con[i]='Y'
        else:
            outlier_con[i]='N'
    
    data_pho_res.insert(loc=10,column='outlier?',value=outlier_pho)
    data_con_res.insert(loc=6,column='outlier?',value=outlier_con)


    # Calculating aposteriori variance factor
    apost=(1/df)*np.matmul(np.matmul(np.transpose(v_obs),P_full),v_obs)
    apost=apost[0][0]

    return df,data_pho_adj, data_con_adj, data_tie_adj, data_ext_adj, data_pho_res, data_con_res, apost, r, ttest, Cx_eops

def output_file(outfile,num_iter,tolerance,df,tred,n,no,uo,ue,conf,ttest,apost,data_pho,data_con,data_tie,data_ext,data_int,data_pho_adj, data_con_adj, data_tie_adj, data_ext_adj, data_pho_res, data_con_res,Cx_eops):

    unk_info = [['Number of images', len(data_ext)], ['Number of EOP unknowns', ue], ['Number of cameras', len(data_int)], ['Number of IOP unknowns', 0], ['Number of tie points', len(data_tie)],['Number of tie point unknowns', (len(data_tie)*3)],['Number of control points', len(data_con)],['Number of control point unknowns', (len(data_con)*3)],['Number of ue', ue],['Number of uo', uo]]
    unk_total = [['Total number of unknowns', (uo+ue)]]

    unk_info_df = pd.DataFrame(unk_info)
    unk_info_df=tabulate(unk_info_df,showindex=False)
    unk_total_df = pd.DataFrame(unk_total)

    obs_info = [['Number of observed image points',len(data_pho)], ['Number of observed image point coords',n],['Number of control param obs',no]]
    obs_total = [['Total number of observations', (n+no)]]
    total_dof=[['Degrees of freedom',df]]

    obs_info_df = pd.DataFrame(obs_info)
    obs_info_df=tabulate(obs_info_df,showindex=False)
    obs_total_df = pd.DataFrame(obs_total)
    total_dof_df=pd.DataFrame(total_dof)
    total_dof_df=tabulate(total_dof_df,showindex=False)

    img_ids=data_ext['image'].unique()
    img_ids.sort()
    con_ids=data_con['Point'].unique()
    con_ids.sort()
    tie_ids=data_tie['Point'].unique()
    tie_ids.sort()

    with open(outfile, 'w') as f:
        f.write("ENGO 500: Bundle Adjustment Results \n")
        f.write("By: Claire Mah, Hannah Poon and Mabel Heffring \n")
        f.write(" \n")
        f.write("*************************************************************************************************************\n")
        f.write("OBSERVATIONS/UNKNOWNS SUMMARY\n")
        f.write(" \n")
        #f.write(obs_info_df.to_string(index= False,header=False,float_format='%0.3f',col_space=10))
        f.write("UNKNOWNS\n")
        f.write(unk_info_df)
        f.write("\n")
        f.write(unk_total_df.to_string(index= False,header=False,float_format='%0.3f',col_space=11))
        f.write("\n")
        f.write("\n")
        f.write("OBSERVATIONS\n")
        f.write(obs_info_df)
        f.write("\n")
        f.write(obs_total_df.to_string(index= False,header=False,float_format='%0.3f',col_space=12))
        f.write("\n")
        f.write("\n")
        f.write(total_dof_df)
        f.write("\n")
        f.write("\n")
        f.write("*************************************************************************************************************\n")
        f.write("EXTERIOR ORIENTATION INPUT DATA\n")
        f.write("\n")
        for i in range(len(data_ext_adj)):
            current_ext=data_ext.iloc[i,:]
            pho_filtered=data_pho[(data_pho.image == current_ext['image'])]
            metadata=[['Image',current_ext['image']],['Camera',current_ext['camera']]]
            metadata_df = pd.DataFrame(metadata)
            eop_xyz_info = [['Xc', current_ext['Xc']],['Yc', current_ext['Yc']],['Zc', current_ext['Zc']]]
            eop_opk_info=[['omega', current_ext['omega']],['phi', current_ext['phi']],['kappa', current_ext['kappa'],]]
            eop_xyz_info_df = pd.DataFrame(eop_xyz_info)
            eop_opk_info_df = pd.DataFrame(eop_opk_info)
            eop_xyz_info_df=tabulate(eop_xyz_info_df,showindex=False,floatfmt=(None,".3f"))
            eop_opk_info_df=tabulate(eop_opk_info_df,showindex=False,floatfmt=(None,".5f"))
            f.write(metadata_df.to_string(index= False,header=False,float_format='%0.0f',col_space=5))
            f.write("\n")
            f.write("Number of image point observations:  "+str(len(pho_filtered))+"\n")
            f.write("COORDINATES\n")
            f.write(eop_xyz_info_df)
            f.write("\n")
            f.write("ANGLES\n")
            f.write(eop_opk_info_df)
            f.write("\n")
            f.write("\n")
        f.write("*************************************************************************************************************\n")
        f.write("INTERIOR ORIENTATION INPUT DATA\n")
        f.write("\n")
        for i in range(len(data_int)):
            current_int=data_int.iloc[i,:]
            metadata=[['Camera',current_int['camera']]]
            metadata_df = pd.DataFrame(metadata)
            iop_in_info = [['xp', current_int['xp']],['yp', current_int['yp']],['c', current_int['c']]]
            iop_in_info_df = pd.DataFrame(iop_in_info)
            iop_in_info_df=tabulate(iop_in_info_df,showindex=False,floatfmt=".3f")
            f.write(metadata_df.to_string(index= False,header=False,float_format='%0.0f',col_space=5))
            f.write("\n")
            f.write(iop_in_info_df)
            f.write("\n")
            f.write("\n")
        f.write("*************************************************************************************************************\n")
        f.write("OBSERVED PHOTO COORDINATE DATA\n")
        f.write("\n")
        for i in img_ids:
            pho_filtered=data_pho[(data_pho.image == i)]
            pho_filtered=pho_filtered.drop('image',axis=1)
            type_array=np.empty((len(pho_filtered),1),dtype=str)
            for x in range(len(pho_filtered)):
                current_pho=pho_filtered.iloc[x,:]
                p=current_pho['point']
                if p in con_ids:
                    type_array[x]='C'
                elif p in tie_ids:
                    type_array[x]='T'
            pho_filtered.insert(loc=1,column='type',value=type_array)
            metadata=[['Image',i]]
            metadata_df = pd.DataFrame(metadata)
            pho_filtered=tabulate(pho_filtered,showindex=False,headers=pho_filtered.columns,floatfmt=(".0f",None,".3f",".3f",".3f",".3f"),tablefmt="simple")
            f.write(metadata_df.to_string(index= False,header=False,float_format='%0.0f',col_space=5))
            f.write("\n")
            f.write("=============\n")
            f.write(pho_filtered)
            f.write("\n")
            f.write("\n")
        f.write("*************************************************************************************************************\n")
        f.write("CONTROL POINT INPUT DATA\n")
        f.write("\n")
        num_img_con=np.zeros((len(data_con),1))
        for i in range(len(data_con)):
            current_con=data_con.iloc[i,:]
            P=current_con['Point']
            num_img_filt=data_pho[(data_pho.point == P)]
            num_img_con[i]=len(num_img_filt)
        data_con.insert(loc=1,column='# img',value=num_img_con)
        data_con_df=tabulate(data_con,showindex=False,headers=data_con.columns,floatfmt=(".0f",".0f",".3f",".3f",".3f",".3f",".3f",".3f"),tablefmt="simple")
        f.write(data_con_df)
        f.write("\n")
        f.write("\n")
        f.write("*************************************************************************************************************\n")
        f.write("TIE POINT INPUT DATA\n")
        f.write("\n")
        num_img_tie=np.zeros((len(data_tie),1))
        for i in range(len(data_tie)):
            current_tie=data_tie.iloc[i,:]
            P=current_tie['Point']
            num_img_filt=data_pho[(data_pho.point == P)]
            num_img_tie[i]=len(num_img_filt)
        data_tie.insert(loc=1,column='# img',value=num_img_tie)
        data_tie_df=tabulate(data_tie,showindex=False,headers=data_tie.columns,floatfmt=(".0f",".0f",".3f",".3f",".3f"),tablefmt="simple")
        f.write(data_tie_df)
        f.write("\n")
        f.write("\n")
        f.write("*************************************************************************************************************\n")
        f.write("ADJUSTMENT SUCCESSFUL!\n")
        f.write("\n")
        f.write("Number of iteration(s):  "+str(num_iter)+"\n")
        f.write("\n")
        f.write("Convergence tolerance:   "+str(tolerance)+"\n")
        f.write("\n")
        f.write("*************************************************************************************************************\n")
        f.write("IMAGE POINT RESIDUALS, REDUNDANCY NUMBERS AND STANDARDISED RESIDUALS\n")
        f.write("\n")
        initial_info = [['Significance of test (two-tail)', conf], ['Critical t-test value', ttest]]

        initial_info = pd.DataFrame(initial_info)
        initial_info=tabulate(initial_info,showindex=False)
        f.write(initial_info)
        f.write("\n")
        f.write("\n")

        for i in img_ids:
            pho_res_filt=data_pho_res[(data_pho_res.image == i)]
            pho_res_filt=pho_res_filt.drop('image',axis=1)
            metadata=[['Image',i]]
            metadata_df = pd.DataFrame(metadata)
            pho_res_filt_df=tabulate(pho_res_filt,showindex=False,headers=pho_res_filt.columns,floatfmt=(".0f",".3f",".3f",".2f",".2f",".3f",".3f",".2f",".2f",None),tablefmt="simple")
            f.write(metadata_df.to_string(index= False,header=False,float_format='%0.0f',col_space=5))
            f.write("\n")
            f.write("=============\n")
            f.write(pho_res_filt_df)
            RMS_now=[['RMS',calc_RMS(pho_res_filt.iloc[:,1]),calc_RMS(pho_res_filt.iloc[:,2])]]
            RMS_now=pd.DataFrame(RMS_now)
            f.write("\n")
            f.write("    -------------------\n")
            f.write(RMS_now.to_string(index= False,header=False,float_format='%0.3f',col_space=7))
            f.write("\n")
            f.write("\n")
        f.write("=======================================\n")
        over_mean=[['MEAN   ',round(calc_mean(data_pho_res.iloc[:,2]),3),round(calc_mean(data_pho_res.iloc[:,3]),3),round(calc_mean(data_pho_res.iloc[:,4]),2),round(calc_mean(data_pho_res.iloc[:,5]),2)]]
        rms_mean=[['RMS    ',calc_RMS(data_pho_res.iloc[:,2]),calc_RMS(data_pho_res.iloc[:,3])]]
        over_mean=pd.DataFrame(over_mean)
        over_mean.columns=['A','B','C','D','E']
        rms_mean=pd.DataFrame(rms_mean)
        f.write("OVERALL\n")
        f.write(over_mean.to_string(index= False,header=False,formatters={"B": "{: .3f}".format, "C": "{: .3f}".format, "D": "{: .2f}".format,"E": "{: .2f}".format},col_space=7))
        f.write("\n")
        f.write(rms_mean.to_string(index= False,header=False,float_format='%0.3f',col_space=7))
        f.write("\n")

        flagged_points=data_pho_res[(data_pho_res.iloc[:,9] == 'Y')]
        f.write("\n")
        f.write("Number of outliers     "+str(len(flagged_points))+"\n")
        f.write("\n")
        x_res=np.array(data_pho_res.iloc[:,2])
        y_res=np.array(data_pho_res.iloc[:,3])
        max_in_x=data_pho_res[(data_pho_res.iloc[:,2] == np.max(x_res))]
        max_in_y=data_pho_res[(data_pho_res.iloc[:,3] == np.max(y_res))]
        min_in_x=data_pho_res[(data_pho_res.iloc[:,2] == np.min(x_res))]
        min_in_y=data_pho_res[(data_pho_res.iloc[:,3] == np.min(y_res))]
        f.write("Maximum x residual:  "+'{:.3f}'.format(round(max_in_x.iloc[0,2],3))+"\n")
        f.write("Point   "+str(max_in_x.iloc[0,0])+"\n")
        f.write("Image   "+str(max_in_x.iloc[0,1])+"\n")
        f.write("Maximum y residual:  "+'{:.3f}'.format(round(max_in_y.iloc[0,3], 3))+"\n")
        f.write("Point   "+str(max_in_y.iloc[0,0])+"\n")
        f.write("Image   "+str(max_in_y.iloc[0,1])+"\n")
        f.write("Minimum x residual: "+'{:.3f}'.format(round(min_in_x.iloc[0,2],3))+"\n")
        f.write("Point   "+str(min_in_x.iloc[0,0])+"\n")
        f.write("Image   "+str(min_in_x.iloc[0,1])+"\n")
        f.write("Minimum y residual: "+'{:.3f}'.format(round(min_in_y.iloc[0,3],3))+"\n")
        f.write("Point   "+str(min_in_y.iloc[0,0])+"\n")
        f.write("Image   "+str(min_in_y.iloc[0,1])+"\n")
        f.write("\n")
        x_red=np.array(data_pho_res.iloc[:,4])
        y_red=np.array(data_pho_res.iloc[:,5])
        f.write("Redundancy in x:   "+'{:.2f}'.format(round(np.sum(x_red),2))+"\n")
        f.write("Redundancy in y:   "+'{:.2f}'.format(round(np.sum(y_red),2))+"\n")
        f.write("\n")
        f.write("*************************************************************************************************************\n")
        f.write("PARAMETER RESIDUALS\n")
        f.write("\n")
        f.write("CONTROL POINTS\n")
        f.write("===============\n")
        con_res_df=tabulate(data_con_res,showindex=False,headers=data_con_res.columns,floatfmt=(".0f",None,".3f",".2f",".3f",".2f",None),tablefmt="simple")
        f.write(con_res_df)
        f.write("\n")

        X_res=data_con_res[(data_con_res.iloc[:,1] == 'X')]
        Y_res=data_con_res[(data_con_res.iloc[:,1] == 'Y')]
        Z_res=data_con_res[(data_con_res.iloc[:,1] == 'Z')]
        All_red=np.array(data_con_res['r'])
        RMS_con=[['RMS','X',calc_RMS(X_res.iloc[:,2])],['RMS','Y',calc_RMS(Y_res.iloc[:,2])],['RMS','Z',calc_RMS(Z_res.iloc[:,2])]]
        RMS_con=tabulate(pd.DataFrame(RMS_con),showindex=False,floatfmt=(None,None,".3f"))
        f.write("\n")
        f.write(RMS_con+"\n")
        f.write("\n")
        f.write("Redundancy:  "+'{:.2f}'.format(round(np.sum(All_red),2))+"\n")
        f.write("\n")
        f.write("*************************************************************************************************************\n")
        f.write("ESTIMATED VARIANCE FACTOR SUMMARY\n")
        f.write("\n")
        vfactor=[['Total Redundancy',tred],['Estimated variance factor',apost]]
        vfactor=tabulate(pd.DataFrame(vfactor),showindex=False,floatfmt=(None,".3f"))
        f.write(vfactor+"\n")
        f.write("\n")
        f.write("*************************************************************************************************************\n")
        f.write("ESTIMATED EXTERIOR ORIENTATION PARAMETERS AND STANDARD ERRORS\n")
        f.write("\n")
        for i in range(len(data_ext_adj)):
            current_ext=data_ext_adj.iloc[i,:]
            pho_filtered=data_pho[(data_pho.image == current_ext['image'])]
            metadata=[['Image',current_ext['image']],['Camera',current_ext['camera']]]
            metadata_df = pd.DataFrame(metadata)
            eop_xyz_info = [['Xc', current_ext['Xc'],current_ext.iloc[8]],['Yc', current_ext['Yc'],current_ext.iloc[9]],['Zc', current_ext['Zc'],current_ext.iloc[10]]]
            eop_opk_info=[['omega', current_ext['omega'],current_ext.iloc[11]],['phi', current_ext['phi'],current_ext.iloc[12]],['kappa', current_ext['kappa'],current_ext.iloc[13]]]
            eop_xyz_info_df = pd.DataFrame(eop_xyz_info)
            eop_opk_info_df = pd.DataFrame(eop_opk_info)
            eop_xyz_info_df=tabulate(eop_xyz_info_df,showindex=False,floatfmt=(None,".3f",".3f"))
            eop_opk_info_df=tabulate(eop_opk_info_df,showindex=False,floatfmt=(None,".5f",".5f"))
            f.write(metadata_df.to_string(index= False,header=False,float_format='%0.0f',col_space=5))
            f.write("\n")
            f.write("Number of image point observations:  "+str(len(pho_filtered))+"\n")
            f.write("COORDINATES\n")
            f.write(eop_xyz_info_df)
            f.write("\n")
            f.write("ANGLES\n")
            f.write(eop_opk_info_df)
            f.write("\n")
            f.write("\n")
        f.write("MEAN PRECISION\n")
        eop_xyz_prec=[['Xc',calc_Prec(data_ext_adj.iloc[:,8])],['Yc',calc_Prec(data_ext_adj.iloc[:,9])],['Zc',calc_Prec(data_ext_adj.iloc[:,10])]]
        eop_opk_prec=[['omega',calc_Prec(data_ext_adj.iloc[:,11])],['phi',calc_Prec(data_ext_adj.iloc[:,12])],['kappa',calc_Prec(data_ext_adj.iloc[:,13])]]
        eop_xyz_prec_df=tabulate(pd.DataFrame(eop_xyz_prec),showindex=False,floatfmt=(None,".3f"))
        eop_opk_prec_df=tabulate(pd.DataFrame(eop_opk_prec),showindex=False,floatfmt=(None,".5f"))
        f.write("COORDINATES\n")
        f.write(eop_xyz_prec_df)
        f.write("\n")
        f.write("ANGLES\n")
        f.write(eop_opk_prec_df)
        f.write("\n")
        f.write("\n")
        f.write("*************************************************************************************************************\n")
        f.write("ESTIMATED CONTROL POINT COORDINATES AND STANDARD ERRORS\n")
        f.write("\n")
        data_con_adj.insert(loc=1,column='# img',value=num_img_con)
        data_con_adj_tbl=tabulate(data_con_adj,showindex=False,headers=data_con_adj.columns,floatfmt=(".0f",".0f",".3f",".3f",".3f",".3f",".3f",".3f"),tablefmt="simple")
        f.write(data_con_adj_tbl+"\n")
        prec_con=[[calc_Prec(data_con_adj.iloc[:,5]),calc_Prec(data_con_adj.iloc[:,6]),calc_Prec(data_con_adj.iloc[:,7])]]
        prec_con_tbl=tabulate(pd.DataFrame(prec_con),showindex=False,floatfmt=(".3f",".3f",".3f"),tablefmt="plain")
        f.write("                                               ----------------------\n")
        f.write("MEAN PRECISION                                   "+prec_con_tbl+"\n")
        f.write("\n")
        f.write("*************************************************************************************************************\n")
        f.write("ESTIMATED TIE POINT COORDINATES AND STANDARD ERRORS\n")
        f.write("\n")
        data_tie_adj.insert(loc=1,column='# img',value=num_img_tie)
        data_tie_adj_tbl=tabulate(data_tie_adj,showindex=False,headers=data_tie_adj.columns,floatfmt=(".0f",".0f",".3f",".3f",".3f",".3f",".3f",".3f"),tablefmt="simple")
        f.write(data_tie_adj_tbl+"\n")
        prec_tie=[[calc_Prec(data_tie_adj.iloc[:,5]),calc_Prec(data_tie_adj.iloc[:,6]),calc_Prec(data_tie_adj.iloc[:,7])]]
        prec_tie_tbl=tabulate(pd.DataFrame(prec_tie),showindex=False,floatfmt=(".3f",".3f",".3f"),tablefmt="plain")
        f.write("                                                ----------------------\n")
        f.write("MEAN PRECISION                                  "+prec_tie_tbl+"\n")
        f.write("\n")
        f.write("*************************************************************************************************************\n")
        f.write("ADJUSTED PHOTO OBSERVATIONS AND STANDARD ERRORS\n")
        f.write("\n")
        for i in img_ids:
            pho_filtered=data_pho_adj[(data_pho_adj.image == i)]
            pho_filtered=pho_filtered.drop('image',axis=1)
            type_array=np.empty((len(pho_filtered),1),dtype=str)
            for x in range(len(pho_filtered)):
                current_pho=pho_filtered.iloc[x,:]
                p=current_pho['point']
                if p in con_ids:
                    type_array[x]='C'
                elif p in tie_ids:
                    type_array[x]='T'
            pho_filtered.insert(loc=1,column='type',value=type_array)
            metadata=[['Image',i]]
            metadata_df = pd.DataFrame(metadata)
            pho_filtered=tabulate(pho_filtered,showindex=False,headers=pho_filtered.columns,floatfmt=(".0f",None,".3f",".3f",".3f",".3f"),tablefmt="simple")
            f.write(metadata_df.to_string(index= False,header=False,float_format='%0.0f',col_space=5))
            f.write("\n")
            f.write("=============\n")
            f.write(pho_filtered+"\n")
            prec_pho=[[calc_Prec(data_pho_adj.iloc[:,4]),calc_Prec(data_pho_adj.iloc[:,5])]]
            prec_pho_tbl=tabulate(pd.DataFrame(prec_pho),showindex=False,floatfmt=(".3f",".3f"),tablefmt="plain")
            f.write("                                   ----------------\n")
            f.write("MEAN PRECISION                       "+prec_pho_tbl+"\n")
            f.write("\n")
            f.write("\n")
        f.write("*************************************************************************************************************\n")
        f.write("CORRELATION COEFFICIENT SUB-MATRICIES\n")
        f.write("\n")
        Corr_columns=['Xc','Yc','Zc','omega','phi','kappa']
        for i in range(len(img_ids)):
            current_ext=data_ext_adj.iloc[i,:]
            img_idx=i*6
            sub_Cx=Cx_eops[img_idx:img_idx+6,img_idx:img_idx+6]
            sub_Corr=calc_Corr(sub_Cx)
            sub_Corr_df=pd.DataFrame(sub_Corr)
            sub_Corr_df.columns=Corr_columns
            sub_Corr_df.insert(loc=0,column='',value=Corr_columns)
            sub_Corr_tbl=tabulate(sub_Corr_df,showindex=False,headers=sub_Corr_df.columns,floatfmt=(None,".2f",".2f",".2f",".2f",".2f",".2f"),tablefmt="plain")
            metadata=[['Image',current_ext['image']],['Camera',current_ext['camera']]]
            metadata_df = pd.DataFrame(metadata)
            f.write(metadata_df.to_string(index= False,header=False,float_format='%0.0f',col_space=5))
            f.write("\n")
            f.write("=============\n")
            f.write(sub_Corr_tbl)
            f.write("\n")
            f.write("\n")
        f.write("*************************************************************************************************************\n")
        f.write("Program ended successfully - no errors.\n")
        f.write("*******END OF FILE*******\n")
        f.write("\n")
        

def calc_RMS(residuals):
    squared_res=np.zeros((len(residuals),1))
    for r in range(len(residuals)):
        squared_res[r]=math.pow(residuals.iloc[r],2)
    sum_res=np.sum(squared_res)
    RMS=math.sqrt(sum_res/len(residuals))
    return RMS

def calc_Prec(std):
    squared_std=np.zeros((len(std),1))
    for r in range(len(std)):
        squared_std[r]=math.pow(std.iloc[r],2)
    sum_std=np.sum(squared_std)
    Prec=math.sqrt(sum_std/len(std))
    return Prec

def calc_Corr(Cx):
    Cor_mat=np.zeros((len(Cx),len(Cx[0])))
    for i in range(len(Cx)):
        for j in range(len(Cx[0])):
            Cor_mat[i][j]=Cx[i][j]/(math.sqrt(Cx[i][i])*math.sqrt(Cx[j][j]))
    return Cor_mat

def calc_mean(array):
    array_sum=0
    for a in range(len(array)):
        array_sum=array_sum+array.iloc[a]
    mean=array_sum/len(array)
    return mean
    





  



