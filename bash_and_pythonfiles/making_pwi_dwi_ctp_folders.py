#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 10:09:44 2017

@author: amar
"""



#
#from os import walk
#
#f = []
#mypath='/Users/amar/Desktop/test_send_to_rapid'
#for (dirpath, dirnames, filenames) in walk(mypath):
#    f.extend(filenames)
#    break


import os
import dicom
from glob import glob
import shutil
import re

files = []
start_dir = os.getcwd()
start_dir = '/Users/amar/Desktop/data_arrange3'
pattern   = "*.dcm"

for dir,_,_ in os.walk('/Users/amar/Desktop/Buffer'):
    files.extend(glob(os.path.join(dir,pattern))) 
#    
#for file in files:     
#    f=open(file, 'r')  
#    f.close() 
    
ds=[]
ds1=[]
dict = {}
ds_StudyComments=[]
ds_PatientID=[]
ds_SOPInstanceUID=[]
ds_SeriesInstanceUID=[]
ds_SeriesDescription=[]
ds_Modality=[]
for x in range(0,len(files)):
   
    dict[x]=dicom.read_file(files[x])
    ds.append(dict[x])
    try:
        ds_StudyComments.append(str(ds[x].StudyComments ))
    except:
        print(files[x])
#        ds_StudyComments.append('BL')
#        ds_StudyComments.append(str(ds[x].ImageComments ))

    ds_PatientID.append(str(ds[x].PatientID ))
    ds_SOPInstanceUID.append(str(ds[x].SOPInstanceUID  ))
    ds_SeriesInstanceUID.append(str(ds[x].SeriesInstanceUID ))
    ds_SeriesDescription.append(str(ds[x].SeriesDescription ))
    ds_Modality.append(str(ds[x].Modality ))
   
uniqueSID=list(set(ds_SeriesInstanceUID));
uniquePID=list(set(ds_PatientID));
uniqueSC=list(set( ds_StudyComments));
pwi1=['perf','pwi','dsc'];
dwi1=['diff','dwi','b1000','isoreg','b0', 'dti', 'CHERIEPI'];
ctp1=['axial','shuttle','brain','perf','ctp','pct','dyn','head','cine','diamox','SLAB','PCT'];

             
for i in range(0,len(uniquePID)):
    if not os.path.exists(start_dir + '/' + uniquePID[i]):
        os.makedirs(start_dir + '/' + uniquePID[i]);
    for j in range(len(uniqueSC)):
        flag_pwi=1
        flag_dwi=1
        flag_ctp=1
        for k in range(len(uniqueSID)):
            for h in range(0,len(files)):
                
                if (uniquePID[i]==ds_PatientID[h]) and (uniqueSC[j]==ds_StudyComments[h]) and (uniqueSID[k]==ds_SeriesInstanceUID[h]): 
                    if not os.path.exists(start_dir + '/' + uniquePID[i] + '/' + uniqueSC[j]):
                        os.makedirs(start_dir + '/' + uniquePID[i] + '/' + uniqueSC[j]);
                    
                    for a in range(0,len(pwi1)):
                        if re.search(pwi1[a],ds_SeriesDescription[h],re.I) and (ds_Modality[h] == 'MR'):
                            if not os.path.exists(start_dir + '/' + uniquePID[i] + '/' + uniqueSC[j] + '/' + 'PWI' + str(flag_pwi) ):
                                os.makedirs(start_dir + '/' + uniquePID[i] + '/' + uniqueSC[j] + '/' + 'PWI'  + str(flag_pwi));
                            shutil.copy2(files[h], start_dir + '/' + uniquePID[i] + '/' + uniqueSC[j] + '/' + 'PWI' + str(flag_pwi) + '/' + ds_SOPInstanceUID[h] + '.dcm')            
                    
                    
                    
                    for b in range(0,len(dwi1)):
                        if re.search(dwi1[b],ds_SeriesDescription[h],re.I) and (ds_Modality[h] == 'MR'):
                            if not os.path.exists(start_dir + '/' + uniquePID[i] + '/' + uniqueSC[j] + '/' + 'DWI' + str(flag_dwi)):
                                os.makedirs(start_dir + '/' + uniquePID[i] + '/' + uniqueSC[j] + '/' + 'DWI' + str(flag_dwi));
                            shutil.copy2(files[h], start_dir + '/' + uniquePID[i] + '/' + uniqueSC[j] + '/' + 'DWI' + str(flag_dwi) + '/' + ds_SOPInstanceUID[h] + '.dcm')   
             
             
                    for c in range(0,len(ctp1)):
                        if re.search(ctp1[c],ds_SeriesDescription[h],re.I) and (ds_Modality[h] == 'CT'):
                            if not os.path.exists(start_dir + '/' + uniquePID[i] + '/' + uniqueSC[j] + '/' + 'CTP' + str(flag_ctp)):
                                os.makedirs(start_dir + '/' + uniquePID[i] + '/' + uniqueSC[j] + '/' + 'CTP' + str(flag_ctp));
                            shutil.copy2(files[h], start_dir + '/' + uniquePID[i] + '/' + uniqueSC[j] + '/' + 'CTP' + str(flag_ctp) + '/' + ds_SOPInstanceUID[h] + '.dcm')         
        
        
            if os.path.exists(start_dir + '/' + uniquePID[i] + '/' + uniqueSC[j] + '/' + 'PWI'  + str(flag_pwi)):
                flag_pwi=flag_pwi+1;
            if os.path.exists(start_dir + '/' + uniquePID[i] + '/' + uniqueSC[j] + '/' + 'DWI'  + str(flag_dwi)):
                flag_dwi=flag_dwi+1;
            if os.path.exists(start_dir + '/' + uniquePID[i] + '/' + uniqueSC[j] + '/' + 'CTP'  + str(flag_ctp)):
                flag_ctp=flag_ctp+1;
        
      

  
    
        
                
        




