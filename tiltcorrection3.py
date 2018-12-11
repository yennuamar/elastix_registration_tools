#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 22:47:07 2018

@author: amar
"""

import SimpleITK as sitk
import numpy as np

import glob, os
import dicom
import math

#if os.path.exists('/Users/amar/Desktop/nccts_for_registration/'+cid+'.nii'):
#    ncctimg_bl=sitk.ReadImage('/Users/amar/Desktop/nccts_for_registration/'+cid+'.nii')
#else:
#    return
#ncctarr_bl=sitk.GetArrayFromImage(ncctimg_bl)
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
    
    input_folder='/Users/icasdb/Desktop/nccts_for_registration_new/'
    IDs=open(input_folder + 'IDS_test.txt').read().split("\n")
    #     IDs=open('/Users/icasdb/Desktop/registered_maps2/' + 'IDS.txt').read().split("\n")
    for cid in IDs:  #IDs:
        print cid
        
            
        ncct_dcm_list=[]
        for file in glob.glob(input_folder+str(cid)+'/*/*/*dcm'):
            ncct_dcm_list.append(file)
#        ncct_dcm_list.sort()
        try:    
            ncct_dcm_list,_,_=dicom_sorter_thickness_splitter(ncct_dcm_list)
        except:
            print "missing info in dicom header"
            ncct_dcm_list.sort()
        reader = sitk.ImageSeriesReader()
        reader.SetFileNames(ncct_dcm_list)
        ncct_image = reader.Execute()
        ncct_image.SetDirection((1,0,0,0,1,0,0,0,1))
        if os.path.exists(input_folder+str(cid)+'_dual.nii'):
            ncct_image = sitk.ReadImage(input_folder+str(cid)+'_dual.nii')
            ncct_image.SetDirection((1,0,0,0,1,0,0,0,1))      
        else:
            sitk.WriteImage(ncct_image,input_folder+str(cid)+'.nii')
        
        spacing=ncct_image.GetSpacing()
        size=ncct_image.GetSize()
        ncct_arr=sitk.GetArrayFromImage(ncct_image)
        
        dcminfo = dicom.read_file(ncct_dcm_list[0])
        
        tilt=float(dcminfo.GantryDetectorTilt)
        tiltradians=math.radians(tilt)
        #thickness=float(dcminfo.SliceThickness)
        thickness=float(spacing[2])
        print thickness
        if tilt<0:
            ytranslation=thickness*math.sin(tiltradians)*-1
        else:
            ytranslation=thickness*math.sin(tiltradians)
        ncct_image_arr_in=np.zeros(ncct_arr.shape)
        ncct_out_arr=np.zeros(ncct_arr.shape)
        ncct_image_out_main=[]
        for i in range(size[2]):
            ncct_image_arr_in=np.zeros(ncct_arr.shape)
            ncct_image_arr_in[i,:,:]=ncct_arr[i,:,:]
            ncct_image_in=sitk.GetImageFromArray(ncct_image_arr_in)
            ncct_image_in.CopyInformation(ncct_image) 
            translate=(0,ytranslation*(i-size[2]/2),0)
            translation = sitk.TranslationTransform(3)
            translation.SetOffset(translate)
            interpolator = sitk.sitkNearestNeighbor
            temp_ncct_image_out=sitk.Resample(ncct_image_in,ncct_image.GetSize(),translation,interpolator,ncct_image.GetOrigin(),ncct_image.GetSpacing(),ncct_image.GetDirection())
            temp_ncct_out_arr=sitk.GetArrayViewFromImage(temp_ncct_image_out)
            ncct_out_arr=ncct_out_arr+temp_ncct_out_arr
        ncct_out_image=sitk.GetImageFromArray(ncct_out_arr)
        ncct_out_image.CopyInformation(ncct_image)
        sitk.WriteImage(ncct_out_image,input_folder+str(cid)+'_tiltcorrected.nii')
        
        