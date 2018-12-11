
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

     for cid in IDs:  #IDs:
         print cid

         if os.path.exists(output_folder+str(cid)+'_b1000_registered_to_template.nii'):

             dwi_reg2template_img=sitk.ReadImage(output_folder+str(cid)+'_b1000_registered_to_template.nii')             
             dwi_reg2template_arr=sitk.GetArrayFromImage(dwi_reg2template_img)
             dwi_reg2template_arr=rewrite_dim(dwi_reg2template_arr)
             dwi_reg2template_arr=np.transpose(dwi_reg2template_arr.astype(int),(1,2,0))
             dwi_reg2template_arr_mymontage=imageutils.montage(dwi_reg2template_arr)
             dwi_reg2template_arr_mymontage_rescale=imageutils.imrescale(dwi_reg2template_arr_mymontage,[np.min(dwi_reg2template_arr_mymontage),np.max(dwi_reg2template_arr_mymontage)],[0,1])
             imageutils.imsave(output_folder+'pngs/'+str(cid)+'_B_b1000_registered_to_template.png' ,dwi_reg2template_arr_mymontage_rescale)
             
             mask_reg2template_img=sitk.ReadImage(output_folder+str(cid)+'_mask_registered_to_template.nii')             
             mask_reg2template_arr=sitk.GetArrayFromImage(mask_reg2template_img)
             mask_reg2template_arr=rewrite_dim(mask_reg2template_arr)
             mask_reg2template_arr=np.transpose(mask_reg2template_arr.astype(int),(1,2,0))
             mask_reg2template_arr_mymontage=imageutils.montage(mask_reg2template_arr)
             mask_reg2template_arr_mymontage_rescale=imageutils.imrescale(mask_reg2template_arr_mymontage,[np.min(mask_reg2template_arr_mymontage),np.max(mask_reg2template_arr_mymontage)],[0,1])
             imageutils.imsave(output_folder+'pngs/'+str(cid)+'_C_mask_registered_to_template.png' ,mask_reg2template_arr_mymontage_rescale)
             
             template_img=sitk.ReadImage(output_folder+'T1_template_5mm_thickness.nii')             
             template_arr=sitk.GetArrayFromImage(template_img)
             template_arr=rewrite_dim(template_arr)
             template_arr=np.transpose(template_arr.astype(int),(1,2,0))
             template_arr_mymontage=imageutils.montage(template_arr)
             template_arr_mymontage_rescale=imageutils.imrescale(template_arr_mymontage,[np.min(template_arr_mymontage),np.max(template_arr_mymontage)],[0,1])
             imageutils.imsave(output_folder+'pngs/'+str(cid)+'_A_T1_template_5mm_thickness.png' ,template_arr_mymontage_rescale)
             
             
             
             
             
