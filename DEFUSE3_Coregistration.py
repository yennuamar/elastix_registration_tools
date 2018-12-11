#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 10:39:17 2017

@author: icasdb
"""

import SimpleITK as sitk
import numpy as np
import dicom2nifti
import glob, os
import dicom
#


def dcms_to_nifti_converter(dicom_folder_path, nifti_folder_path, nifti_filename, pattern):
    os.chdir(dicom_folder_path)
    dcm_list=[]
    for file in glob.glob(pattern):
        dcm_list.append(dicom.read_file(dicom_folder_path + '/' + file))
    if not os.path.exists(nifti_folder_path):
        os.makedirs(nifti_folder_path)
    nifti_path=nifti_folder_path + nifti_filename  + '.nii'     
    dicom2nifti.convert_dicom.dicom_array_to_nifti(dcm_list,nifti_path)
      
    return nifti_path, dcm_list 

IDs=open('/Users/icasdb/Desktop/defuse3_test/' + 'IDS.txt').read().split("\n")
for cid in IDs[0:1]:  #IDs:
    print cid


    start_dir='/Users/icasdb/Desktop/defuse3_test'
    BL_IMG=start_dir +'/'+str(cid)+'/'+'BL/Results_PWI_DWI_use'
    FU_IMG=start_dir +'/'+str(cid)+'/'+'FU/Results_PWI_DWI_use'

    if not os.path.exists('/Users/icasdb/Desktop/nifti/'+str(cid)):
        os.makedirs('/Users/icasdb/Desktop/nifti/'+str(cid))
    
    dcms_to_nifti_converter(BL_IMG,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/',str(cid)+'_BL_baseline_slice', '*baseline_slice*' )
    dcms_to_nifti_converter(BL_IMG,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/',str(cid)+'_BL_tmax_slice', '*tmax_slice*' )
    dcms_to_nifti_converter(BL_IMG,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/',str(cid)+'_BL_DWI_lesion_mask', '*DWI_lesion_mask*' )
    dcms_to_nifti_converter(BL_IMG,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/',str(cid)+'_BL_rdwi_slice', '*rdwi_slice*' )
    dcms_to_nifti_converter(BL_IMG,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/',str(cid)+'_BL_TMax_lesion_mask1_slice', '*TMax_lesion_mask1_slice*' )
    dcms_to_nifti_converter(BL_IMG,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/',str(cid)+'_BL_TMax_lesion_mask2_slice', '*TMax_lesion_mask2_slice*' )
    dcms_to_nifti_converter(BL_IMG,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/',str(cid)+'_BL_TMax_lesion_mask3_slice', '*TMax_lesion_mask3_slice*' )
    dcms_to_nifti_converter(BL_IMG,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/',str(cid)+'_BL_TMax_lesion_mask4_slice', '*TMax_lesion_mask4_slice*' )

    dcms_to_nifti_converter(FU_IMG,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/',str(cid)+'_FU_baseline_slice', '*baseline_slice*' )
    dcms_to_nifti_converter(FU_IMG,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/',str(cid)+'_FU_tmax_slice', '*tmax_slice*' )
    dcms_to_nifti_converter(FU_IMG,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/',str(cid)+'_FU_DWI_lesion_mask', '*DWI_lesion_mask*' )
    dcms_to_nifti_converter(FU_IMG,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/',str(cid)+'_FU_rdwi_slice', '*rdwi_slice*' )
    dcms_to_nifti_converter(FU_IMG,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/',str(cid)+'_FU_TMax_lesion_mask1_slice', '*TMax_lesion_mask1_slice*' )
    dcms_to_nifti_converter(FU_IMG,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/',str(cid)+'_FU_TMax_lesion_mask2_slice', '*TMax_lesion_mask2_slice*' )
    dcms_to_nifti_converter(FU_IMG,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/',str(cid)+'_FU_TMax_lesion_mask3_slice', '*TMax_lesion_mask3_slice*' )
    dcms_to_nifti_converter(FU_IMG,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/',str(cid)+'_FU_TMax_lesion_mask4_slice', '*TMax_lesion_mask4_slice*' )

    BL_baselineslice_niiloc='/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL_baseline_slice.nii'
    FU_baselineslice_niiloc='/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_FU_baseline_slice.nii'

    SimpleElastix = sitk.ElastixImageFilter() 
    BL_baselineslice_img=sitk.ReadImage(BL_baselineslice_niiloc)
    FU_baselineslice_img=sitk.ReadImage(FU_baselineslice_niiloc)

    SimpleElastix.SetFixedImage(FU_baselineslice_img) 
    SimpleElastix.SetMovingImage(BL_baselineslice_img)  
    parameterMap = SimpleElastix.ReadParameterFile('/Users/icasdb/Desktop/DWINCCT/CODE/affine_crosscorelation.txt')

    SimpleElastix.SetParameterMap(parameterMap)
    SimpleElastix.Execute()
    FI=SimpleElastix.GetResultImage()   
    transformParameterMap = SimpleElastix.GetTransformParameterMap()

    sitk.WriteParameterFile(transformParameterMap[0],'/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL2FU_Coregistration_transform_baseline_slice.xfm.txt')
    sitk.WriteImage(FI,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL2FU_Coregistration_baseline_slice.nii')

    #transformix _BL_tmax_slice
    transformixImageFilter = sitk.TransformixImageFilter()
    transformParameterMap_BL_baseline_2_FU_baseline=sitk.ReadParameterFile('/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL2FU_Coregistration_transform_baseline_slice.xfm.txt')
    transformixImageFilter.SetTransformParameterMap(transformParameterMap_BL_baseline_2_FU_baseline)
    transformixImageFilter.SetMovingImage(sitk.ReadImage('/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL_tmax_slice.nii'))
    transformixImageFilter.Execute()
    
    RI=transformixImageFilter.GetResultImage()
    sitk.WriteImage(RI,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL2FU_coregistration_tmax_slice.nii') 
    #transformix _BL_rdwi_slice
    transformixImageFilter = sitk.TransformixImageFilter()
    transformParameterMap_BL_baseline_2_FU_baseline=sitk.ReadParameterFile('/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL2FU_Coregistration_transform_baseline_slice.xfm.txt')
    transformixImageFilter.SetTransformParameterMap(transformParameterMap_BL_baseline_2_FU_baseline)
    transformixImageFilter.SetMovingImage(sitk.ReadImage('/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL_rdwi_slice.nii'))
    transformixImageFilter.Execute()
    
    RI=transformixImageFilter.GetResultImage()
    sitk.WriteImage(RI,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL2FU_coregistration_rdwi_slice.nii') 
    #transformix _BL_DWI_lesion_mask
    transformixImageFilter = sitk.TransformixImageFilter()
    transformParameterMap_BL_baseline_2_FU_baseline=sitk.ReadParameterFile('/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL2FU_Coregistration_transform_baseline_slice.xfm.txt')
    transformixImageFilter.SetTransformParameterMap(transformParameterMap_BL_baseline_2_FU_baseline)
    transformixImageFilter.SetMovingImage(sitk.ReadImage('/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL_DWI_lesion_mask.nii'))
    transformixImageFilter.Execute()
    
    RI=transformixImageFilter.GetResultImage()
    sitk.WriteImage(RI,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL2FU_coregistration_DWI_lesion_mask.nii') 
    #transformix  _BL_TMax_lesion_mask1_slice
    transformixImageFilter = sitk.TransformixImageFilter()
    transformParameterMap_BL_baseline_2_FU_baseline=sitk.ReadParameterFile('/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL2FU_Coregistration_transform_baseline_slice.xfm.txt')
    transformixImageFilter.SetTransformParameterMap(transformParameterMap_BL_baseline_2_FU_baseline)
    transformixImageFilter.SetMovingImage(sitk.ReadImage('/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL_TMax_lesion_mask1_slice'))
    transformixImageFilter.Execute()
    
    RI=transformixImageFilter.GetResultImage()
    sitk.WriteImage(RI,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL2FU_coregistration_TMax_lesion_mask1_slice.nii') 
    #transformix _BL_TMax_lesion_mask2_slice
    transformixImageFilter = sitk.TransformixImageFilter()
    transformParameterMap_BL_baseline_2_FU_baseline=sitk.ReadParameterFile('/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL2FU_Coregistration_transform_baseline_slice.xfm.txt')
    transformixImageFilter.SetTransformParameterMap(transformParameterMap_BL_baseline_2_FU_baseline)
    transformixImageFilter.SetMovingImage(sitk.ReadImage('/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL_TMax_lesion_mask2_slice.nii'))
    transformixImageFilter.Execute()
    
    RI=transformixImageFilter.GetResultImage()
    sitk.WriteImage(RI,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL2FU_coregistration_TMax_lesion_mask2_slice.nii') 

    #transformix _BL_TMax_lesion_mask3_slice
    transformixImageFilter = sitk.TransformixImageFilter()
    transformParameterMap_BL_baseline_2_FU_baseline=sitk.ReadParameterFile('/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL2FU_Coregistration_transform_baseline_slice.xfm.txt')
    transformixImageFilter.SetTransformParameterMap(transformParameterMap_BL_baseline_2_FU_baseline)
    transformixImageFilter.SetMovingImage(sitk.ReadImage('/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL_TMax_lesion_mask3_slice.nii'))
    transformixImageFilter.Execute()
    
    RI=transformixImageFilter.GetResultImage()
    sitk.WriteImage(RI,'/Users/icasdb/Desktop/nifti/'+str(cid)+'/'+str(cid)+'_BL2FU_coregistration_TMax_lesion_mask3_slice.nii') 