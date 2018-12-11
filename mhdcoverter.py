#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 12:44:04 2018

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

def mhd_to_nifti_converter(mhd_folder_path, nifti_filename, mhd_name):
    nifti_full_path= nifti_filename  + '.nii' 
    image = sitk.ReadImage(mhd_folder_path+mhd_name)
    sitk.WriteImage( image, nifti_full_path )  
    return


if __name__=="__main__":
     IDs=open('/Users/icasdb/Desktop/registered_maps2/' + 'IDS_full.txt').read().split("\n")

     for cid in IDs:  #IDs:
         print cid
         
#         input_folder='/Users/icasdb/Desktop/D3_R47_RANDOMIZED_FINAL'
         input_folder='/Users/icasdb/Desktop/D2_DWI/D3_BL_only_DWI/' 
         output_folder='/Users/icasdb/Desktop/D2_DWI/'
         if os.path.exists(input_folder+cid+"/BL/Results_only_DWI_R47/segm_mask_view0_Thresholded_ADC_Parameter_View_slab0.mhd"):
             mhd_to_nifti_converter(input_folder+cid+"/BL/Results_only_DWI_R47/",output_folder+cid+"_b1000_bl","dwi_bNonZeroIso_biasFieldCorrected.mhd")
             mhd_to_nifti_converter(input_folder+cid+"/BL/Results_only_DWI_R47/",output_folder+cid+"_mask","segm_mask_view0_Thresholded_ADC_Parameter_View_slab0.mhd")
             