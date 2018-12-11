#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 12:06:33 2018

@author: icasdb
"""

import SimpleITK as sitk
import numpy as np
import dicom2nifti
import glob, os
import dicom
import shutil
import imageutils
import scipy
#import dicomutils
import matplotlib.pyplot as plt

template_img=sitk.ReadImage('/Users/icasdb/Desktop/ICBMtemplate/icbm_avg_152_t1_tal_nlin_symmetric_VI.nii')
template_mask_img=sitk.ReadImage('/Users/icasdb/Desktop/ICBMtemplate/icbm_avg_152_t1_tal_nlin_symmetric_VI_mask.nii')
template_arr=sitk.GetArrayFromImage(template_img)
template_mask_arr=sitk.GetArrayFromImage(template_mask_img)

brain_template_arr=np.zeros(template_arr.shape)
brain_template_arr[template_mask_arr>0]=template_arr[template_mask_arr>0]
brain_template_image=sitk.GetImageFromArray(brain_template_arr)
brain_template_image.CopyInformation(template_img)

sitk.WriteImage(brain_template_image,'/Users/icasdb/Desktop/ICBMtemplate/braintemplate.nii')

if __name__=="__main__":

     IDs=open('/Users/icasdb/Desktop/D2_DWI/' + 'IDs.txt').read().split("\n")

     for cid in IDs:  #IDs:
         print cid

         input_folder='/Users/icasdb/Desktop/D2_DWI/'
         output_folder=input_folder+'Registered_images/'
         
         DWI_image=sitk.ReadImage(input_folder+cid+'_b1000_bl.nii')
         DWI_mask_image=sitk.ReadImage(input_folder+cid+'_mask.nii')
         
         
         
         
         SimpleElastix=sitk.ElastixImageFilter()
         parameterMap = SimpleElastix.ReadParameterFile(input_folder+'affine_mutualinformation.txt')
         SimpleElastix.SetFixedImage(A)
         SimpleElastix.SetMovingImage(A)
         SimpleElastix.SetParameterMap(parameterMap)
         SimpleElastix.Execute()
         
