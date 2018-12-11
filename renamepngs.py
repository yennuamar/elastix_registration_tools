#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 12:49:58 2018

@author: icasdb
"""
import SimpleITK as sitk
import numpy as np
import dicom2nifti
import glob, os
import dicom
import shutil
import imageutils

if __name__=="__main__":
     IDs=open('/Users/icasdb/Desktop/registered_maps2/' + 'IDS.txt').read().split("\n")
     for cid in IDs:  #IDs:
         print cid

#         input_folder='/Users/icasdb/Desktop/D3_R47_RANDOMIZED_FINAL'
         input_folder='/Users/icasdb/Desktop/registered_maps2/'
         output_folder2='/Users/icasdb/Desktop/Coregistration_pngs/'
        
         if os.path.exists(input_folder + cid + '/' + cid +'_' +'noncon_cropped.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'noncon_cropped.png',output_folder2 + cid +'_A_' +'noncon_cropped.png')
         elif os.path.exists(input_folder + cid + '/' + cid +'_' +'noncon.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'noncon.png',output_folder2 + cid +'_A_' +'noncon.png')   
         
         if os.path.exists(input_folder + cid + '/' + cid +'_' +'BL_baseline_slice_slab0.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'BL_baseline_slice_slab0.png',output_folder2 + cid +'_B_' +'BL_baseline_slice_slab0.png')
        
         if os.path.exists(input_folder + cid + '/' + cid +'_' +'FU2BL_coregistration_baseline_slice_slab0.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'FU2BL_coregistration_baseline_slice_slab0.png',output_folder2 + cid +'_C_' +'FU2BL_coregistration_baseline_slice_slab0.png')    
            
         if os.path.exists(input_folder + cid + '/' + cid +'_' +'BL_tmaxmask_overlayed_on_tmaxgray_slab0.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'BL_tmaxmask_overlayed_on_tmaxgray_slab0.png',output_folder2 + cid +'_D_' +'BL_tmaxmask_overlayed_on_tmaxgray_slab0.png')
        
         if os.path.exists(input_folder + cid + '/' + cid +'_' +'FU2BL_coregistration_tmaxmask_overlayed_on_tmaxgray_slab0.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'FU2BL_coregistration_tmaxmask_overlayed_on_tmaxgray_slab0.png',output_folder2 + cid +'_E_' +'FU2BL_coregistration_tmaxmask_overlayed_on_tmaxgray_slab0.png')    
              
         if os.path.exists(input_folder + cid + '/' + cid +'_' +'BL_rcbv_slice_slab0.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'BL_rcbv_slice_slab0.png',output_folder2 + cid +'_F_' +'BL_rcbv_slice_slab0.png')
        
         if os.path.exists(input_folder + cid + '/' + cid +'_' +'FU2BL_coregistration_rcbv_slice_slab0.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'FU2BL_coregistration_rcbv_slice_slab0.png',output_folder2 + cid +'_G_' +'FU2BL_coregistration_rcbv_slice_slab0.png')                         
         
            
         if os.path.exists(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_baseline_slice_merged_.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_baseline_slice_merged_.png',output_folder2 + cid +'_B_' +'BL2NCCT_coregistration_baseline_slice_merged_.png')
         elif os.path.exists(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_baseline_slice_slab0_.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_baseline_slice_slab0_.png',output_folder2 + cid +'_B_' +'BL2NCCT_coregistration_baseline_slice_slab0_.png')
            
            
            
            
         if os.path.exists(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_baseline_slice_merged_.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_baseline_slice_merged_.png',output_folder2 + cid +'_C_' +'FU2NCCT_coregistration_baseline_slice_merged_.png')    
         elif os.path.exists(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_baseline_slice_slab0_.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_baseline_slice_slab0_.png',output_folder2 + cid +'_C_' +'FU2NCCT_coregistration_baseline_slice_slab0_.png')              
         
            

         if os.path.exists(input_folder + cid + '/' + cid +'_' +'BL2NCCT_tmaxmask_overlayed_on_tmaxgray_merged.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'BL2NCCT_tmaxmask_overlayed_on_tmaxgray_merged.png',output_folder2 + cid +'_D_' +'BL2NCCT_tmaxmask_overlayed_on_tmaxgray_merged.png')
         elif os.path.exists(input_folder + cid + '/' + cid +'_' +'BL2NCCT_tmaxmask_overlayed_on_tmaxgray_slab0.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'BL2NCCT_tmaxmask_overlayed_on_tmaxgray_slab0.png',output_folder2 + cid +'_D_' +'BL2NCCT_tmaxmask_overlayed_on_tmaxgray_slab0.png')        
         
            
         if os.path.exists(input_folder + cid + '/' + cid +'_' +'FU2NCCT_tmaxmask_overlayed_on_tmaxgray_merged.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'FU2NCCT_tmaxmask_overlayed_on_tmaxgray_merged.png',output_folder2 + cid +'_E_' +'FU2NCCT_tmaxmask_overlayed_on_tmaxgray_merged.png')   
         elif os.path.exists(input_folder + cid + '/' + cid +'_' +'FU2NCCT_tmaxmask_overlayed_on_tmaxgray_slab0.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'FU2NCCT_tmaxmask_overlayed_on_tmaxgray_slab0.png',output_folder2 + cid +'_E_' +'FU2NCCT_tmaxmask_overlayed_on_tmaxgray_slab0.png')    
            
         if os.path.exists(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_rcbv_slice_merged_.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_rcbv_slice_merged_.png',output_folder2 + cid +'_F_' +'BL2NCCT_coregistration_rcbv_slice_merged_.png')
         elif os.path.exists(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_rcbv_slice_slab0_.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_rcbv_slice_slab0_.png',output_folder2 + cid +'_F_' +'BL2NCCT_coregistration_rcbv_slice_slab0_.png')        
         
            
         if os.path.exists(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_rcbv_slice_merged_.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_rcbv_slice_merged_.png',output_folder2 + cid +'_G_' +'FU2NCCT_coregistration_rcbv_slice_merged_.png')   
         elif os.path.exists(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_rcbv_slice_slab0_.png'):
             shutil.copy2(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_rcbv_slice_slab0_.png',output_folder2 + cid +'_G_' +'FU2NCCT_coregistration_rcbv_slice_slab0_.png')                
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            