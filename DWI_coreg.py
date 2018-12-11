#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 11:03:15 2018

@author: icasdb
"""

import SimpleITK as sitk
import numpy as np
import dicom2nifti
import glob, os
import dicom
import shutil
import imageutils
#import dicomutils
import matplotlib.pyplot as plt

def rewrite_nifti(baselinefile,targetfile):
   
    baseline_image=sitk.ReadImage(baselinefile)
    targetimage=sitk.ReadImage(targetfile)
    targetimage.CopyInformation(baseline_image)
    sitk.WriteImage( targetimage, targetfile)
    return

def rewrite_dim(arr1):
    temparrshape=arr1.shape
    if temparrshape[1]<temparrshape[2]:
        arr1=arr1[:,:,0:temparrshape[1]]
    else:
        arr1=arr1[:,0:temparrshape[2],:]
        
    return arr1



if __name__=="__main__":

     IDs=open('/Users/icasdb/Desktop/D2_DWI/' + 'IDs.txt').read().split("\n")
     input_folder='/Users/icasdb/Desktop/D2_DWI/'
     output_folder='/Users/icasdb/Desktop/D2_DWI/Registered_images/'
     template_img=sitk.ReadImage(input_folder+'scct_unsmooth_clamped.nii')
     template_arr=sitk.GetArrayFromImage(template_img)
     template_arr[template_arr>100]=0
     SS_template_img=sitk.GetImageFromArray(template_arr)
     SS_template_img.CopyInformation(template_img)
     sitk.WriteImage(SS_template_img,input_folder+'scct_unsmooth_clamped_skullstripped.nii')
     T1_img=sitk.ReadImage(input_folder+'icbm_avg_152_t1_tal_nlin_symmetric_VI.nii')
     T1_mask_img=sitk.ReadImage(input_folder+'icbm_avg_152_t1_tal_nlin_symmetric_VI_mask.nii')
     T1_arr=sitk.GetArrayFromImage(T1_img)
     T1_mask_arr=sitk.GetArrayFromImage(T1_mask_img)
     T1_arr_new=np.zeros(T1_arr.shape)
     T1_arr_new[np.logical_and(T1_arr>0,T1_mask_arr>0)]=T1_arr[np.logical_and(T1_arr>0,T1_mask_arr>0)]
     T1_img_new=sitk.GetImageFromArray(T1_arr_new)
     T1_img_new.CopyInformation(T1_img)
     sitk.WriteImage(T1_img_new,input_folder+'icbm_avg_152_t1_tal_nlin_symmetric_VI_SS.nii')
     for cid in IDs:  #IDs:
         print cid

         if os.path.exists(input_folder+str(cid)+'_b1000_bl.nii'):
             dwi_img=sitk.ReadImage(input_folder+str(cid)+'_b1000_bl.nii')
             mask_img=sitk.ReadImage(input_folder+str(cid)+'_mask.nii') 
             
             SimpleElastix = sitk.ElastixImageFilter() 
             SimpleElastix.SetFixedImage(T1_img_new) 
             SimpleElastix.SetMovingImage(dwi_img)  
             parameterMap = SimpleElastix.ReadParameterFile(input_folder+'affine_mutualinformation.txt')    
             SimpleElastix.SetParameterMap(parameterMap)
             SimpleElastix.Execute()
             transformParameterMap = SimpleElastix.GetTransformParameterMap()
             
             transformParameterMap[0]["FinalBSplineInterpolationOrder"]=('0')
             transformParameterMap[0]["Spacing"]=(transformParameterMap[0]["Spacing"][0],transformParameterMap[0]["Spacing"][1],str(float(transformParameterMap[0]["Spacing"][2])*5))
             transformParameterMap[0]["Size"]=(transformParameterMap[0]["Size"][0],transformParameterMap[0]["Size"][1],str(int(transformParameterMap[0]["Size"][2])/5))
             
             transformixImageFilter = sitk.TransformixImageFilter()
             transformixImageFilter.SetTransformParameterMap(transformParameterMap)
             transformixImageFilter.SetMovingImage(mask_img)
             transformixImageFilter.Execute()    
             mask_reg2template_img=transformixImageFilter.GetResultImage()
             mask_reg2template_img_loc=output_folder+str(cid)+'_mask_registered_to_template.nii'
             sitk.WriteImage(mask_reg2template_img,mask_reg2template_img_loc) 
             
             transformParameterMap[0]["FinalBSplineInterpolationOrder"]=('1')
             transformixImageFilter = sitk.TransformixImageFilter()
             transformixImageFilter.SetTransformParameterMap(transformParameterMap)
             transformixImageFilter.SetMovingImage(dwi_img)
             transformixImageFilter.Execute()    
             dwi_reg2template_img=transformixImageFilter.GetResultImage()
             dwi_reg2template_img_loc=output_folder+str(cid)+'_b1000_registered_to_template.nii'
             sitk.WriteImage(dwi_reg2template_img,dwi_reg2template_img_loc) 
                       
             
#     SimpleElastix = sitk.ElastixImageFilter() 
#     SimpleElastix.SetFixedImage(T1_img_new) 
#     SimpleElastix.SetMovingImage(T1_img_new)  
#     parameterMap = SimpleElastix.ReadParameterFile(input_folder+'affine_mutualinformation.txt')    
#     SimpleElastix.SetParameterMap(parameterMap)
#     SimpleElastix.Execute()
#     transformParameterMap = SimpleElastix.GetTransformParameterMap()
#     transform_parameter_loc=output_folder+ 'template2template.xfm.txt'
#     sitk.WriteParameterFile(transformParameterMap[0],transform_parameter_loc)
             
     transformixImageFilter = sitk.TransformixImageFilter()
     parameterMap=transformixImageFilter.ReadParameterFile(output_folder+ 'template2template.xfm.txt')
     transformixImageFilter.SetTransformParameterMap(parameterMap)
     transformixImageFilter.SetMovingImage(T1_img_new)
     transformixImageFilter.Execute()    
     T1_image_lowres_img=transformixImageFilter.GetResultImage()
     T1_image_lowres_img_loc=output_folder+'T1_template_5mm_thickness.nii'
     sitk.WriteImage(T1_image_lowres_img,T1_image_lowres_img_loc) 
             
         