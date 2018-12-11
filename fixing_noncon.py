#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 13:14:12 2018

@author: icasdb
"""


import SimpleITK as sitk
import glob
import numpy as np
import dicom
import math


def dicom_sorter_thickness_splitter(dcm_unsorted_list):
    thickness_list=[]
    slicelocation_list=[]
    unique_sorted_thickness_list=[]
    sorted_slicelocation_list=[]
    dcm_sorted_list=[]
    dcm_sorted_thickness_list=[]
    dcm_lists=[]
    for i in range(len(dcm_unsorted_list)):
        x=dicom.read_file(dcm_unsorted_list[i])
        thickness_list.append(float(x.SliceThickness))
        slicelocation_list.append(float(x.SliceLocation))

    unique_sorted_thickness_list=sorted(set(thickness_list))
    sorted_slicelocation_list=sorted(slicelocation_list)
    
    for i in range(len(sorted_slicelocation_list)):   
        for j in range(len(slicelocation_list)):
            if slicelocation_list[j]==sorted_slicelocation_list[i]:
                dcm_sorted_list.append(dcm_unsorted_list[j])
#        if i>0:
#            print sorted_slicelocation_list[i]-sorted_slicelocation_list[i-1]
            
    for i in range(len(unique_sorted_thickness_list)):   
        for j in range(len(dcm_sorted_list)):
            x1=dicom.read_file(dcm_sorted_list[j])
            if float(x1.SliceThickness)==unique_sorted_thickness_list[i]:
                dcm_sorted_thickness_list.append(dcm_sorted_list[j])
                
        dcm_lists.append(dcm_sorted_thickness_list) 
        dcm_sorted_thickness_list=[]

    return dcm_sorted_list, dcm_lists,unique_sorted_thickness_list
        
if __name__=="__main__":
    cid=101
    input_folder='/Users/icasdb/Desktop/'+str(cid)+'/'
    output_folder='/Users/icasdb/Desktop/'+str(cid)+'/'

    x1=sitk.ReadImage(input_folder+'NCCT_FIX_tiltcorrected.nii')
    y1=sitk.ReadImage(input_folder+'NCCT_TOPOK_tiltcorrected.nii')
    x1arr=sitk.GetArrayFromImage(x1)
    x1arr[x1arr<0]=0
    x1new=sitk.GetImageFromArray(x1arr)
    x1new.CopyInformation(x1)
    y1arr=sitk.GetArrayFromImage(y1)
    y1arr[y1arr<0]=0
    y1new=sitk.GetImageFromArray(y1arr)
    y1new.CopyInformation(y1)
    
    y1new.SetDirection(x1new.GetDirection())
    SimpleElastix=sitk.ElastixImageFilter()
    parameterMap = SimpleElastix.ReadParameterFile('/Users/icasdb/Desktop/DWINCCT/CODE/rigid_D3.txt')
    
    SimpleElastix.SetFixedImage(x1new)
    SimpleElastix.SetMovingImage(y1new)
    SimpleElastix.SetParameterMap(parameterMap)
    RI=SimpleElastix.Execute()
    transformParameterMap =SimpleElastix.GetTransformParameterMap()
    sitk.WriteParameterFile(transformParameterMap[0],output_folder+'tranform_param.xfm.txt')
    sitk.WriteImage(RI,output_folder+'image2_registeredto_image1.nii')
    RIarr=sitk.GetArrayFromImage(RI)
    
    x1arr[RIarr>0]=RIarr[RIarr>0]
    
    FIimage=sitk.GetImageFromArray(x1arr)
    FIimage.CopyInformation(x1new)
    sitk.WriteImage(FIimage,output_folder+'corrected_noncon.nii')
    

    
    
    
    
    