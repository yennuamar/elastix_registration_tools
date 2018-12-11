#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 10:39:17 2017

@author: icasdb
"""

import SimpleITK as sitk
import numpy as np
import glob, os
import dicom
import shutil
import imageutils
#import dicomutils
import matplotlib.pyplot as plt

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

def dcms_to_nifti_converter(dicom_folder_path, nifti_filename , pattern):
    os.chdir(dicom_folder_path)
    dcm_list=[]
    for file in glob.glob(pattern):
        dcm_list.append(dicom_folder_path + '/' + file)
#    if not os.path.exists(nifti_folder_path):
#        os.makedirs(nifti_folder_path)
    nifti_full_path= nifti_filename  
#    dcm_list.sort()
    dcm_sorted_list,_,_= dicom_sorter_thickness_splitter(dcm_list)
    reader = sitk.ImageSeriesReader()
    reader.SetFileNames(dcm_sorted_list)
    image = reader.Execute()
    sitk.WriteImage( image, nifti_full_path )  
    return nifti_full_path, dcm_sorted_list 

def mhd_to_nifti_converter(mhd_folder_path, nifti_filename, mhd_name):
    nifti_full_path= nifti_filename  + '.nii' 
    image = sitk.ReadImage(mhd_folder_path+mhd_name)
    sitk.WriteImage( image, nifti_full_path )  
    return


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

def registerFU2BL_singleslab_sufficient_zcoverage(FU_LOC,BL_LOC,output_folder,cid,BL_numofslabs,FU_numofslabs,bl_modality,fu_modality):
    if not os.path.exists(output_folder+str(cid)):
        os.makedirs(output_folder+str(cid))
    FU_LOC_2=FU_LOC+'/Results'
    BL_LOC_2=BL_LOC+'/Results'

    BL_baseline_slice_loc=output_folder+str(cid)+'/'+str(cid)+'_BL_baseline_slice_slab0.nii'
    BL_tmax_slice_loc=output_folder+str(cid)+'/'+str(cid)+'_BL_tmax_slice_slab0.nii'
    BL_rcbv_slice_loc=output_folder+str(cid)+'/'+str(cid)+'_BL_rcbv_slice_slab0.nii'
    BL_tmax_mask_loc=output_folder+str(cid)+'/'+str(cid)+'_BL_segm_mask_view1_Thresholded_Tmax_Parameter_View_slab0.nii'
    BL_tmax6_mask_loc=output_folder+str(cid)+'/'+str(cid)+'_BL_segm_mask_view0_Thresholded_Tmax_Parameter_View_slab0.nii'
    BL_nonCsf_mask_loc=output_folder+str(cid)+'/'+str(cid)+'_BL_perf_nonCsfMask_slab0.nii'

    
    
    _,BL_baseline_slice_list=dcms_to_nifti_converter(BL_LOC_2,BL_baseline_slice_loc, '*baseline_slab0_slice*' )
    _,BL_tmax_slice_list=dcms_to_nifti_converter(BL_LOC_2,BL_tmax_slice_loc, '*tmax_slab0_slice*' )
    _,BL_rcbv_slice_list=dcms_to_nifti_converter(BL_LOC_2,BL_rcbv_slice_loc, '*rcbv_slab0_slice*' )
    mhd_to_nifti_converter(BL_LOC,BL_tmax_mask_loc,'/segm_mask_view1_Thresholded_Tmax_Parameter_View_slab0.mhd')
    mhd_to_nifti_converter(BL_LOC,BL_tmax6_mask_loc,'/segm_mask_view0_Thresholded_Tmax_Parameter_View_slab0.mhd')
    mhd_to_nifti_converter(BL_LOC,BL_nonCsf_mask_loc,'/perf_nonCsfMask_slab0.mhd')
    
    rewrite_nifti(BL_baseline_slice_loc,BL_tmax_slice_loc)
    rewrite_nifti(BL_baseline_slice_loc,BL_rcbv_slice_loc)
    rewrite_nifti(BL_baseline_slice_loc,BL_tmax_mask_loc)  
    rewrite_nifti(BL_baseline_slice_loc,BL_tmax6_mask_loc)
    rewrite_nifti(BL_baseline_slice_loc,BL_nonCsf_mask_loc) 
    
    z0=dicom.read_file(BL_baseline_slice_list[0])
    zcoverage=float(z0.SliceThickness)*len(BL_baseline_slice_list)
    print zcoverage
    if cid=="113":
        zcoverage=999999 #exception
        
    
        
    if (bl_modality=='CT' and zcoverage<120) or cid=="197" or cid=="247":
        registerFUBL2NCCT_insufficient_zcoverage(FU_LOC,BL_LOC,output_folder,cid,BL_numofslabs,FU_numofslabs,bl_modality,fu_modality)
        return
    FU_baseline_slice_loc=output_folder+str(cid)+'/'+str(cid)+'_FU_baseline_slice_slab0.nii'
    FU_tmax_slice_loc=output_folder+str(cid)+'/'+str(cid)+'_FU_tmax_slice_slab0.nii'
    FU_rcbv_slice_loc=output_folder+str(cid)+'/'+str(cid)+'_FU_rcbv_slice_slab0.nii'
    FU_tmax_mask_loc=output_folder+str(cid)+'/'+str(cid)+'_FU_segm_mask_view1_Thresholded_Tmax_Parameter_View_slab0.nii'
    FU_tmax6_mask_loc=output_folder+str(cid)+'/'+str(cid)+'_FU_segm_mask_view0_Thresholded_Tmax_Parameter_View_slab0.nii'
    FU_nonCsf_mask_loc=output_folder+str(cid)+'/'+str(cid)+'_FU_perf_nonCsfMask_slab0.nii'
    
    dcms_to_nifti_converter(FU_LOC_2,FU_baseline_slice_loc, '*baseline_slab0_slice*' )
    dcms_to_nifti_converter(FU_LOC_2,FU_tmax_slice_loc, '*tmax_slab0_slice*' )
    dcms_to_nifti_converter(FU_LOC_2,FU_rcbv_slice_loc, '*rcbv_slab0_slice*' )
    mhd_to_nifti_converter(FU_LOC,FU_tmax_mask_loc,'/segm_mask_view1_Thresholded_Tmax_Parameter_View_slab0.mhd')
    mhd_to_nifti_converter(FU_LOC,FU_tmax6_mask_loc,'/segm_mask_view0_Thresholded_Tmax_Parameter_View_slab0.mhd')
    mhd_to_nifti_converter(FU_LOC,FU_nonCsf_mask_loc,'/perf_nonCsfMask_slab0.mhd')
    
    rewrite_nifti(FU_baseline_slice_loc,FU_tmax_slice_loc)
    rewrite_nifti(FU_baseline_slice_loc,FU_rcbv_slice_loc)
    rewrite_nifti(FU_baseline_slice_loc,FU_tmax_mask_loc)
    rewrite_nifti(FU_baseline_slice_loc,FU_tmax6_mask_loc)
    rewrite_nifti(FU_baseline_slice_loc,FU_nonCsf_mask_loc) 
        
    SimpleElastix = sitk.ElastixImageFilter() 
    FU_baseline_slice_img=sitk.ReadImage(FU_baseline_slice_loc)
    BL_baseline_slice_img=sitk.ReadImage(BL_baseline_slice_loc)
    
    if bl_modality=='CT' and fu_modality=='MR':
        blarr=sitk.GetArrayFromImage(sitk.ReadImage(BL_baseline_slice_loc))
        blarr[blarr>100]=0
        tempimg=sitk.GetImageFromArray(blarr)
        tempimg.CopyInformation(BL_baseline_slice_img)
        BL_baseline_slice_img=tempimg
#        
    SimpleElastix.SetFixedImage(BL_baseline_slice_img) 
    SimpleElastix.SetMovingImage(FU_baseline_slice_img)  
#    parameterMap = SimpleElastix.ReadParameterFile('/Users/icasdb/Desktop/DWINCCT/CODE/affine_mutualinformation.txt')
#    parameterMap = SimpleElastix.ReadParameterFile('/Users/icasdb/Desktop/DWINCCT/CODE/affine_crosscorelation.txt')
    parameterMap = SimpleElastix.ReadParameterFile(output_folder+str(cid)+'/'+str(cid)+'_FU2BL_rigid_D3.txt')
#    parameterMap = SimpleElastix.ReadParameterFile(output_folder+'Parameter_files'+'/'+str(cid)+'_FU2BL_rigid_D3.txt')
#    shutil.copy2('/Users/icasdb/Desktop/DWINCCT/CODE/rigid_D3.txt',output_folder+str(cid)+'/'+str(cid)+'_FU2BL_rigid_D3.txt')
    SimpleElastix.SetParameterMap(parameterMap)
    SimpleElastix.Execute()
    FU2BL_baseline_slice_img=SimpleElastix.GetResultImage()  
    FU2BL_baseline_slice_img_loc=output_folder+str(cid)+'/'+str(cid)+'_FU2BL_coregistration_baseline_slice_slab0.nii'
    sitk.WriteImage(FU2BL_baseline_slice_img,FU2BL_baseline_slice_img_loc)
    
    transformParameterMap = SimpleElastix.GetTransformParameterMap()
    tranform_parameter_loc=output_folder+str(cid)+'/'+str(cid)+'_FU2BL_coregistration_transform_baseline_slice_slab0.xfm.txt'
    sitk.WriteParameterFile(transformParameterMap[0],tranform_parameter_loc)
    transformParameterMap[0]["FinalBSplineInterpolationOrder"]=('0')
    nn_transform_parameter_loc=output_folder+str(cid)+'/'+str(cid)+'_FU2BL_coregistration_transform_baseline_slice_nearestneighborinterpolation_slab0.xfm.txt'
    sitk.WriteParameterFile(transformParameterMap[0],nn_transform_parameter_loc)
    
#transformix _FU2BL_tmax_slice
    transformixImageFilter = sitk.TransformixImageFilter()
    transformParameterMap=sitk.ReadParameterFile(tranform_parameter_loc)
    transformixImageFilter.SetTransformParameterMap(transformParameterMap)
    transformixImageFilter.SetMovingImage(sitk.ReadImage(FU_tmax_slice_loc))
    transformixImageFilter.Execute()
    
    FU2BL_tmax_slice_img=transformixImageFilter.GetResultImage()
    FU2BL_tmax_slice_img_loc=output_folder+str(cid)+'/'+str(cid)+'_FU2BL_coregistration_tmax_slice_slab0.nii'
    sitk.WriteImage(FU2BL_tmax_slice_img,FU2BL_tmax_slice_img_loc) 
    
#transformix _FU2BL_rcbv_slice
    transformixImageFilter = sitk.TransformixImageFilter()
    transformParameterMap=sitk.ReadParameterFile(tranform_parameter_loc)
    transformixImageFilter.SetTransformParameterMap(transformParameterMap)
    transformixImageFilter.SetMovingImage(sitk.ReadImage(FU_rcbv_slice_loc))
    transformixImageFilter.Execute()
    
    FU2BL_rcbv_slice_img=transformixImageFilter.GetResultImage()
    FU2BL_rcbv_slice_img_loc=output_folder+str(cid)+'/'+str(cid)+'_FU2BL_coregistration_rcbv_slice_slab0.nii'
    sitk.WriteImage(FU2BL_rcbv_slice_img,FU2BL_rcbv_slice_img_loc) 

#transformix segm_mask_view1_Thresholded_Tmax_Parameter_View_slab0
    transformixImageFilter = sitk.TransformixImageFilter()
    transformParameterMap=sitk.ReadParameterFile(nn_transform_parameter_loc)
    transformixImageFilter.SetTransformParameterMap(transformParameterMap)
    transformixImageFilter.SetMovingImage(sitk.ReadImage(FU_tmax_mask_loc))
    transformixImageFilter.Execute()    
    FU2BL_tmax_mask_img=transformixImageFilter.GetResultImage()
    FU2BL_tmax_mask_img_loc=output_folder+str(cid)+'/'+str(cid)+'_FU2BL_coregistration_tmax_mask_slab0.nii'
    sitk.WriteImage(FU2BL_tmax_mask_img,FU2BL_tmax_mask_img_loc)   
    
#transformix segm_mask_view0_Thresholded_Tmax_Parameter_View_slab0
    transformixImageFilter = sitk.TransformixImageFilter()
    transformParameterMap=sitk.ReadParameterFile(nn_transform_parameter_loc)
    transformixImageFilter.SetTransformParameterMap(transformParameterMap)
    transformixImageFilter.SetMovingImage(sitk.ReadImage(FU_tmax6_mask_loc))
    transformixImageFilter.Execute()    
    FU2BL_tmax6_mask_img=transformixImageFilter.GetResultImage()
    FU2BL_tmax6_mask_img_loc=output_folder+str(cid)+'/'+str(cid)+'_FU2BL_coregistration_tmax6_mask_slab0.nii'
    sitk.WriteImage(FU2BL_tmax6_mask_img,FU2BL_tmax6_mask_img_loc)   
    
#transformix perf_nonCsfMask_slab0
    transformixImageFilter = sitk.TransformixImageFilter()
    transformParameterMap=sitk.ReadParameterFile(nn_transform_parameter_loc)
    transformixImageFilter.SetTransformParameterMap(transformParameterMap)
    transformixImageFilter.SetMovingImage(sitk.ReadImage(FU_nonCsf_mask_loc))
    transformixImageFilter.Execute()    
    FU2BL_nonCsf_mask_img=transformixImageFilter.GetResultImage()
    FU2BL_nonCsf_mask_img_loc=output_folder+str(cid)+'/'+str(cid)+'_FU2BL_coregistration_nonCsf_mask_slab0.nii'
    sitk.WriteImage(FU2BL_nonCsf_mask_img,FU2BL_nonCsf_mask_img_loc)   
    
#creating tmaxmasks overlayed on tmax gray pngs
    createPNGs(FU2BL_tmax_slice_img_loc,FU2BL_tmax_mask_img_loc,output_folder+str(cid)+'/'+str(cid)+'_FU2BL_coregistration_tmaxmask_overlayed_on_tmaxgray_slab0.png')
    createPNGs(BL_tmax_slice_loc,BL_tmax_mask_loc,output_folder+str(cid)+'/'+str(cid)+'_BL_tmaxmask_overlayed_on_tmaxgray_slab0.png')

#creating baseline pngs 
    arr1 = sitk.GetArrayFromImage(sitk.ReadImage(FU2BL_baseline_slice_img_loc))
    baselinearray=np.transpose(arr1,(1,2,0))   
    mymontage=imageutils.montage(baselinearray)
    if fu_modality=='MR':
        clim=[np.min(mymontage),np.max(mymontage)]
    else:
        clim=[0,100]
    rescale_baseline=imageutils.imrescale(mymontage,clim,[0,1])
    imageutils.imsave(output_folder+str(cid)+'/'+str(cid)+'_'+ 'FU2BL_coregistration_baseline_slice_slab0.png' ,rescale_baseline)
    
    arr2 = sitk.GetArrayFromImage(sitk.ReadImage(BL_baseline_slice_loc))
    baselinearray=np.transpose(arr2,(1,2,0))   
    mymontage=imageutils.montage(baselinearray)
    if bl_modality=='MR':
        clim=[np.min(mymontage),np.max(mymontage)]
    else:
        clim=[0,100]
    rescale_baseline=imageutils.imrescale(mymontage,clim,[0,1])
    imageutils.imsave(output_folder+str(cid)+'/'+str(cid)+'_'+ 'BL_baseline_slice_slab0.png' ,rescale_baseline)
    
#creating rcbv pngs 
    
    arr1 = sitk.GetArrayFromImage(sitk.ReadImage(FU2BL_rcbv_slice_img_loc))
    rcbvarray=np.transpose(arr1,(1,2,0))   
    mymontage=imageutils.montage(rcbvarray)
    clim=[np.min(mymontage),50]
    rescale_rcbv=imageutils.imrescale(mymontage,clim,[0,1])
    imageutils.imsave(output_folder+str(cid)+'/'+str(cid)+'_'+ 'FU2BL_coregistration_rcbv_slice_slab0.png' ,rescale_rcbv)
    
    arr2 = sitk.GetArrayFromImage(sitk.ReadImage(BL_rcbv_slice_loc))
    rcbvarray=np.transpose(arr2,(1,2,0))   
    mymontage=imageutils.montage(rcbvarray)
    clim=[np.min(mymontage),50]
    rescale_rcbv=imageutils.imrescale(mymontage,clim,[0,1])
    imageutils.imsave(output_folder+str(cid)+'/'+str(cid)+'_'+ 'BL_rcbv_slice_slab0.png' ,rescale_rcbv)
    
    
   
    return


def slab2NCCT(IMG_LOC,Ioutput_folder,cid,slab,BLorFU,modality):
    baseline_slice_loc=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'_baseline_slice_'+ slab +'.nii'
    tmax_slice_loc=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'_tmax_slice_'+ slab +'.nii'
    rcbv_slice_loc=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'_rcbv_slice_'+ slab +'.nii'
    tmax_mask1_loc=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'_segm_mask_view1_Thresholded_Tmax_Parameter_View_'+ slab +'.nii'
    tmax6_mask1_loc=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'_segm_mask_view0_Thresholded_Tmax_Parameter_View_'+ slab +'.nii'
    nonCsf_mask1_loc=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'_perf_nonCsfMask_'+ slab +'.nii'


    ncct_skullstripped_loc=output_folder+str(cid)+'/'+str(cid)+'_NCCT_corrected_baseline_skullstripped.nii'
    ncct_loc=output_folder+str(cid)+'/'+str(cid)+'_NCCT_corrected_baseline.nii' 
    
    IMG_LOC_2=IMG_LOC+'/Results'
    dcms_to_nifti_converter(IMG_LOC_2,baseline_slice_loc , '*baseline_'+ slab +'_slice*' )
    dcms_to_nifti_converter(IMG_LOC_2,tmax_slice_loc , '*tmax_'+ slab +'_slice*' )
    dcms_to_nifti_converter(IMG_LOC_2,rcbv_slice_loc , '*rcbv_'+ slab +'_slice*' )
    mhd_to_nifti_converter(IMG_LOC,tmax_mask1_loc , '/segm_mask_view1_Thresholded_Tmax_Parameter_View_'+ slab +'.mhd')
    mhd_to_nifti_converter(IMG_LOC,tmax6_mask1_loc , '/segm_mask_view0_Thresholded_Tmax_Parameter_View_'+ slab +'.mhd')
    mhd_to_nifti_converter(IMG_LOC,nonCsf_mask1_loc , '/perf_nonCsfMask_'+ slab +'.mhd')    
    
    
    rewrite_nifti(baseline_slice_loc,tmax_slice_loc)
    rewrite_nifti(baseline_slice_loc,rcbv_slice_loc)
    rewrite_nifti(baseline_slice_loc,tmax_mask1_loc)
    rewrite_nifti(baseline_slice_loc,tmax6_mask1_loc)
    rewrite_nifti(baseline_slice_loc,nonCsf_mask1_loc)
    
    if modality=='MR':
        non_con_loc=ncct_skullstripped_loc
    else:
        non_con_loc=ncct_loc
        
    
    non_con_img=sitk.ReadImage(non_con_loc)  
#    non_con_arr=sitk.GetArrayFromImage(non_con_img)
#    masked_non_con_arr=np.zeros(non_con_arr.shape,np.uint8)
#    masked_non_con_arr[10:40,:,:]=1
#    masked_non_con_img=sitk.GetImageFromArray(masked_non_con_arr)
#    masked_non_con_img.CopyInformation(non_con_img)
#    
    
    
    temp_bl_img=sitk.ReadImage(baseline_slice_loc)
    temp_bl_img.SetDirection(non_con_img.GetDirection())
    sitk.WriteImage(temp_bl_img,baseline_slice_loc)
    
    temp_tmax_img=sitk.ReadImage(tmax_slice_loc)
    temp_tmax_img.SetDirection(non_con_img.GetDirection())
    sitk.WriteImage(temp_tmax_img,tmax_slice_loc)
    
    temp_rcbv_img=sitk.ReadImage(rcbv_slice_loc)
    temp_rcbv_img.SetDirection(non_con_img.GetDirection())
    sitk.WriteImage(temp_rcbv_img,rcbv_slice_loc)
    
    temp_tmaxmask_img=sitk.ReadImage(tmax_mask1_loc)
    temp_tmaxmask_img.SetDirection(non_con_img.GetDirection())
    sitk.WriteImage(temp_tmaxmask_img,tmax_mask1_loc)
    
    temp_tmax6mask_img=sitk.ReadImage(tmax6_mask1_loc)
    temp_tmax6mask_img.SetDirection(non_con_img.GetDirection())
    sitk.WriteImage(temp_tmax6mask_img,tmax6_mask1_loc)
    
    temp_nonCsfmask_img=sitk.ReadImage(nonCsf_mask1_loc)
    temp_nonCsfmask_img.SetDirection(non_con_img.GetDirection())
    sitk.WriteImage(temp_nonCsfmask_img,nonCsf_mask1_loc)

    SimpleElastix = sitk.ElastixImageFilter() 
    baseline_slice_img=sitk.ReadImage(baseline_slice_loc)
    non_con_img=sitk.ReadImage(non_con_loc) 
    
    
    SimpleElastix.SetFixedImage(non_con_img) 
#    SimpleElastix.SetFixedMask(masked_non_con_img)
    SimpleElastix.SetMovingImage(baseline_slice_img)
    parameterMap = SimpleElastix.ReadParameterFile(output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU + '_rigid_D3.txt')
#    parameterMap = SimpleElastix.ReadParameterFile(output_folder+'Parameter_files'+'/'+str(cid)+'_'+ BLorFU + '_rigid_D3.txt')
#    shutil.copy2('/Users/icasdb/Desktop/DWINCCT/CODE/rigid_D3.txt',output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU + '_rigid_D3.txt')
    SimpleElastix.SetParameterMap(parameterMap)
    SimpleElastix.Execute()
    baseline_slice2ncct=SimpleElastix.GetResultImage() 
    baseline_slice2ncct_loc=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'2NCCT_coregistration_baseline_slice_'+ slab +'.nii'
    sitk.WriteImage(baseline_slice2ncct,baseline_slice2ncct_loc)

    transformParameterMap = SimpleElastix.GetTransformParameterMap()
    tranform_parameter_loc=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'2NCCT_coregistration_transform_baseline_slice_'+ slab +'.xfm.txt'
    nn_tranform_parameter_loc=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'2NCCT_coregistration_transform_baseline_slice_nearestneighborinterpolation_'+ slab +'.xfm.txt'
    sitk.WriteParameterFile(transformParameterMap[0],tranform_parameter_loc)
    transformParameterMap[0]["FinalBSplineInterpolationOrder"]=('0')
    sitk.WriteParameterFile(transformParameterMap[0],nn_tranform_parameter_loc)
    
    
#transformix_tmax_slice
    transformixImageFilter = sitk.TransformixImageFilter()
    ParameterMap=sitk.ReadParameterFile(tranform_parameter_loc)
    transformixImageFilter.SetTransformParameterMap(ParameterMap)
    transformixImageFilter.SetMovingImage(sitk.ReadImage(tmax_slice_loc))
    transformixImageFilter.Execute()   
    tmax_slice2ncct=transformixImageFilter.GetResultImage()
    tmax_slice2ncct_loc=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'2NCCT_coregistration_tmax_slice_'+ slab +'.nii'
    sitk.WriteImage(tmax_slice2ncct,tmax_slice2ncct_loc) 
   
#transformix_tmax_slice_ones
    temparr=sitk.GetArrayFromImage(sitk.ReadImage(tmax_slice_loc))
    ones_arr=np.ones(temparr.shape)
    ones_img=sitk.GetImageFromArray(ones_arr)
    ones_img.CopyInformation(sitk.ReadImage(tmax_slice_loc))
    transformixImageFilter = sitk.TransformixImageFilter()
    nn_ParameterMap=sitk.ReadParameterFile(nn_tranform_parameter_loc)
    transformixImageFilter.SetTransformParameterMap(nn_ParameterMap)
    transformixImageFilter.SetMovingImage(ones_img)
    transformixImageFilter.Execute()
    RI1=transformixImageFilter.GetResultImage()
    sitk.WriteImage(RI1,output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'2NCCT_coregistration_tmax_slice_ones_'+ slab +'.nii') 
    
#transformix_rcbv_slice
    transformixImageFilter = sitk.TransformixImageFilter()
    transformixImageFilter.SetTransformParameterMap(ParameterMap)
    transformixImageFilter.SetMovingImage(sitk.ReadImage(rcbv_slice_loc))
    transformixImageFilter.Execute()   
    rcbv_slice2ncct=transformixImageFilter.GetResultImage()
    rcbv_slice2ncct_loc=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'2NCCT_coregistration_rcbv_slice_'+ slab +'.nii'
    sitk.WriteImage(rcbv_slice2ncct,rcbv_slice2ncct_loc) 
   
          
#transformix segm_mask_view1_Thresholded_Tmax_Parameter_View_slab0
    transformixImageFilter = sitk.TransformixImageFilter()
    nn_ParameterMap=sitk.ReadParameterFile(nn_tranform_parameter_loc)
    transformixImageFilter.SetTransformParameterMap(nn_ParameterMap)
    transformixImageFilter.SetMovingImage(sitk.ReadImage(tmax_mask1_loc))
    transformixImageFilter.Execute()   
    tmax_mask2ncct=transformixImageFilter.GetResultImage()
    tmax_mask2ncct_loc=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'2NCCT_coregistration_segm_mask_view1_Thresholded_Tmax_Parameter_View_'+ slab +'.nii'
    sitk.WriteImage(tmax_mask2ncct,tmax_mask2ncct_loc) 
    
    tmaxmask_overlayedon_tmaxgray_loc=output_folder+str(cid)+'/'+str(cid)+'_'+BLorFU +'2NCCT_tmaxmask_overlayed_on_tmaxgray_'+ slab +'.png'
    createPNGs(tmax_slice2ncct_loc,tmax_mask2ncct_loc,tmaxmask_overlayedon_tmaxgray_loc)

#transformix segm_mask_view0_Thresholded_Tmax_Parameter_View_slab0
    transformixImageFilter = sitk.TransformixImageFilter()
    nn_ParameterMap=sitk.ReadParameterFile(nn_tranform_parameter_loc)
    transformixImageFilter.SetTransformParameterMap(nn_ParameterMap)
    transformixImageFilter.SetMovingImage(sitk.ReadImage(tmax6_mask1_loc))
    transformixImageFilter.Execute()   
    tmax6_mask2ncct=transformixImageFilter.GetResultImage()
    tmax6_mask2ncct_loc=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'2NCCT_coregistration_segm_mask_view0_Thresholded_Tmax_Parameter_View_'+ slab +'.nii'
    sitk.WriteImage(tmax6_mask2ncct,tmax6_mask2ncct_loc) 
    
#transformix perf_nonCsfMask_slab0
    transformixImageFilter = sitk.TransformixImageFilter()
    nn_ParameterMap=sitk.ReadParameterFile(nn_tranform_parameter_loc)
    transformixImageFilter.SetTransformParameterMap(nn_ParameterMap)
    transformixImageFilter.SetMovingImage(sitk.ReadImage(nonCsf_mask1_loc))
    transformixImageFilter.Execute()   
    nonCsf_mask2ncct=transformixImageFilter.GetResultImage()
    nonCsf_mask2ncct_loc=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'2NCCT_coregistration_nonCsfMask_'+ slab +'.nii'
    sitk.WriteImage(nonCsf_mask2ncct,nonCsf_mask2ncct_loc) 
    
# creating baseline slice pngs
    arr1 = sitk.GetArrayFromImage(sitk.ReadImage(baseline_slice2ncct_loc))
    arr1= rewrite_dim(arr1)
    baselinearray=np.transpose(arr1,(1,2,0))   
    mymontage=imageutils.montage(baselinearray)
    if modality=='MR':
        clim=[np.min(mymontage),np.max(mymontage)]
    else:
        clim=[0,100]
    rescale_baseline=imageutils.imrescale(mymontage,clim,[0,1])
    imageutils.imsave(output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'2NCCT_coregistration_baseline_slice_'+ slab + '.png' ,rescale_baseline)

# creating rcbv slice pngs
    arr1 = sitk.GetArrayFromImage(sitk.ReadImage(rcbv_slice2ncct_loc))
    arr1= rewrite_dim(arr1)
    rcbvarray=np.transpose(arr1,(1,2,0))   
    mymontage=imageutils.montage(rcbvarray)
    clim=[np.min(mymontage),50]
    rescale_rcbv=imageutils.imrescale(mymontage,clim,[0,1])
    imageutils.imsave(output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'2NCCT_coregistration_rcbv_slice_'+ slab + '.png' ,rescale_rcbv)

def merge2slabs(output_folder,BLorFU,cid):
    
    tmaxgrayslab0_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_tmax_slice_slab0.nii'
    tmaxgrayslab1_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_tmax_slice_slab1.nii'
    tmaxmaskslab0_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_segm_mask_view1_Thresholded_Tmax_Parameter_View_slab0.nii'
    tmaxmaskslab1_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_segm_mask_view1_Thresholded_Tmax_Parameter_View_slab1.nii'
    tmax6maskslab0_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_segm_mask_view0_Thresholded_Tmax_Parameter_View_slab0.nii'
    tmax6maskslab1_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_segm_mask_view0_Thresholded_Tmax_Parameter_View_slab1.nii'
    nonCsfmaskslab0_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_nonCsfMask_slab0.nii'
    nonCsfmaskslab1_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_nonCsfMask_slab1.nii'
    rcbvslab0_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_rcbv_slice_slab0.nii'
    rcbvslab1_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_rcbv_slice_slab1.nii'
    baselinegrayslab0_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_baseline_slice_slab0.nii'
    baselinegrayslab1_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_baseline_slice_slab1.nii'   
    
    
    tmaxgrayslab0img=sitk.ReadImage(tmaxgrayslab0_loc)
    tmaxgrayslab0arr=sitk.GetArrayFromImage(tmaxgrayslab0img)
    tmaxgrayslab1img=sitk.ReadImage(tmaxgrayslab1_loc)
    tmaxgrayslab1arr=sitk.GetArrayFromImage(tmaxgrayslab1img)

    tmaxmaskslab0img=sitk.ReadImage(tmaxmaskslab0_loc)
    tmaxmaskslab0arr=sitk.GetArrayFromImage(tmaxmaskslab0img)
    tmaxmaskslab1img=sitk.ReadImage(tmaxmaskslab1_loc)
    tmaxmaskslab1arr=sitk.GetArrayFromImage(tmaxmaskslab1img)
    
    tmax6maskslab0img=sitk.ReadImage(tmax6maskslab0_loc)
    tmax6maskslab0arr=sitk.GetArrayFromImage(tmax6maskslab0img)
    tmax6maskslab1img=sitk.ReadImage(tmax6maskslab1_loc)
    tmax6maskslab1arr=sitk.GetArrayFromImage(tmax6maskslab1img)
    
    nonCsfmaskslab0img=sitk.ReadImage(nonCsfmaskslab0_loc)
    nonCsfmaskslab0arr=sitk.GetArrayFromImage(nonCsfmaskslab0img)
    nonCsfmaskslab1img=sitk.ReadImage(nonCsfmaskslab1_loc)
    nonCsfmaskslab1arr=sitk.GetArrayFromImage(nonCsfmaskslab1img)
    
    rcbvslab0img=sitk.ReadImage(rcbvslab0_loc)
    rcbvslab0arr=sitk.GetArrayFromImage(rcbvslab0img)
    rcbvslab1img=sitk.ReadImage(rcbvslab1_loc)
    rcbvslab1arr=sitk.GetArrayFromImage(rcbvslab1img)
    
    baselinegrayslab0img=sitk.ReadImage(baselinegrayslab0_loc)
    baselinegrayslab0arr=sitk.GetArrayFromImage(baselinegrayslab0img)
    baselinegrayslab1img=sitk.ReadImage(baselinegrayslab1_loc)
    baselinegrayslab1arr=sitk.GetArrayFromImage(baselinegrayslab1img)
    
#merging and creating tmax niis and pngs
    onesslab0img=sitk.ReadImage(output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'2NCCT_coregistration_tmax_slice_ones_slab0.nii')
    onesslab0arr=sitk.GetArrayFromImage(onesslab0img)
      
    tmaxgrayslab0arr[onesslab0arr<1]=tmaxgrayslab1arr[onesslab0arr<1]
    tmaxgraymergedimg=sitk.GetImageFromArray(tmaxgrayslab0arr)
    tmaxgraymergedimg.CopyInformation(tmaxgrayslab0img) 
    
    tmaxmaskslab0arr[onesslab0arr<1]=tmaxmaskslab1arr[onesslab0arr<1]
    tmaxmaskmergedimg=sitk.GetImageFromArray(tmaxmaskslab0arr)
    tmaxmaskmergedimg.CopyInformation(tmaxmaskslab0img)
    
    tmax6maskslab0arr[onesslab0arr<1]=tmax6maskslab1arr[onesslab0arr<1]
    tmax6maskmergedimg=sitk.GetImageFromArray(tmax6maskslab0arr)
    tmax6maskmergedimg.CopyInformation(tmax6maskslab0img)
    
    nonCsfmaskslab0arr[onesslab0arr<1]=nonCsfmaskslab1arr[onesslab0arr<1]
    nonCsfmaskmergedimg=sitk.GetImageFromArray(nonCsfmaskslab0arr)
    nonCsfmaskmergedimg.CopyInformation(nonCsfmaskslab0img)
    
    rcbvslab0arr[onesslab0arr<1]=rcbvslab1arr[onesslab0arr<1]
    rcbvmergedimg=sitk.GetImageFromArray(rcbvslab0arr)
    rcbvmergedimg.CopyInformation(rcbvslab0img) 
    
    baselinegrayslab0arr[onesslab0arr<1]=baselinegrayslab1arr[onesslab0arr<1]
    baselinegraymergedimg=sitk.GetImageFromArray(baselinegrayslab0arr)
    baselinegraymergedimg.CopyInformation(baselinegrayslab0img) 

    tmaxgraymergedimg_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_tmax_slice_merged.nii'
    tmaxmaskmergedimg_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_tmax_mask_merged.nii'
    tmax6maskmergedimg_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_tmax6_mask_merged.nii'
    nonCsfmaskmergedimg_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_nonCsf_mask_merged.nii'
    rcbvmergedimg_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_rcbv_slice_merged.nii'
    baselinegraymergedimg_loc=output_folder+str(cid)+'/'+str(cid)+ '_'+ BLorFU +'2NCCT_coregistration_baseline_slice_merged.nii'  
 
    sitk.WriteImage(tmaxgraymergedimg,tmaxgraymergedimg_loc) 
    sitk.WriteImage(tmaxmaskmergedimg,tmaxmaskmergedimg_loc) 
    sitk.WriteImage(tmax6maskmergedimg,tmax6maskmergedimg_loc) 
    sitk.WriteImage(nonCsfmaskmergedimg,nonCsfmaskmergedimg_loc) 
    sitk.WriteImage(rcbvmergedimg,rcbvmergedimg_loc) 
    sitk.WriteImage(baselinegraymergedimg,baselinegraymergedimg_loc)  

    tmaxmaskmergedimg_overlayedon_tmaxgraymergedimg_loc=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'2NCCT_tmaxmask_overlayed_on_tmaxgray_merged.png'
    createPNGs(tmaxgraymergedimg_loc,tmaxmaskmergedimg_loc,tmaxmaskmergedimg_overlayedon_tmaxgraymergedimg_loc)

#creating merged pngs
    
    arr1 = sitk.GetArrayFromImage(baselinegraymergedimg)
    baselinegraymergedarray=np.transpose(arr1,(1,2,0))   
    mymontage=imageutils.montage(baselinegraymergedarray)
    rescale_baselinegraymergedarray=imageutils.imrescale(mymontage,[0,50],[0,1])
    
    baselinegraymergedimg_loc_png=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'2NCCT_coregistration_baseline_slice_merged.png'
    imageutils.imsave(baselinegraymergedimg_loc_png ,rescale_baselinegraymergedarray)
    
    arr1 = sitk.GetArrayFromImage(rcbvmergedimg)
    rcbvarray=np.transpose(arr1,(1,2,0))   
    mymontage=imageutils.montage(rcbvarray)
    rescale_rcbv=imageutils.imrescale(mymontage,[0,50],[0,1])
    
    rcbvmergedimg_loc_png=output_folder+str(cid)+'/'+str(cid)+'_'+ BLorFU +'2NCCT_coregistration_rcbv_slice_merged.png'
    imageutils.imsave(rcbvmergedimg_loc_png ,rescale_rcbv)


    return
    
def registerFUBL2NCCT_insufficient_zcoverage(FU_LOC,BL_LOC,output_folder,cid,BL_numofslabs,FU_numofslabs,baseline_mod,followup_mod):
    if not os.path.exists(output_folder+str(cid)):
        os.makedirs(output_folder+str(cid))
         
#    nifti_path, dcm_list = dcms_to_nifti_converter(input_folder +'/'+str(cid)+'/'+'NCCT',output_folder+str(cid)+'/',str(cid)+'_NCCT_baseline', '*.dcm')
    if os.path.exists('/Users/amar/Reference_nccts_new/'+cid+'_ncct.nii'):
        ncctimg_bl=sitk.ReadImage('/Users/amar/Reference_nccts_new/'+cid+'_ncct.nii')
    else:
        print str(cid)+'not processed'
        return
    ncctarr_bl=sitk.GetArrayFromImage(ncctimg_bl)
    ncct_dcm_list=[]
#    for file in glob.glob('/Users/icasdb/Desktop/Reference_nccts_new/'+cid+'/*/*/*dcm'):
#        ncct_dcm_list.append(file)
#    ncct_dcm_list.sort()
#    dcminfo1 = dicom.read_file(ncct_dcm_list[len(ncct_dcm_list)-2])
#    dcminfo2 = dicom.read_file(ncct_dcm_list[len(ncct_dcm_list)-1])
##    intercept=dcminfo.RescaleIntercept    
##    ncctarr_bl=ncctarr_bl+intercept
    shapebl=ncctimg_bl.GetSize()
    if ncctarr_bl[shapebl[2]/2,shapebl[1]/2,shapebl[0]/2]>1000:
        ncctarr_bl=ncctarr_bl-1024
    ncctarr_bl[ncctarr_bl<0]=0
    newncctimg_bl=sitk.GetImageFromArray(ncctarr_bl)
    newncctimg_bl.CopyInformation(ncctimg_bl)
#    newncctimg_bl.SetDirection((1,0,0,0,1,0,0,0,1))
#    temp_spacing=newncctimg_bl.GetSpacing()
#    if temp_spacing[2]<=2:
#        zspace=float(dcminfo2.SliceLocation-dcminfo1.SliceLocation)
#        xspace=float(dcminfo1.PixelSpacing[0])
#        yspace=float(dcminfo1.PixelSpacing[1])
#        print zspace
#        newncctimg_bl.SetSpacing((xspace,yspace,zspace))
    sitk.WriteImage(newncctimg_bl,output_folder+str(cid)+'/'+str(cid)+'_NCCT_corrected_baseline.nii')

    ncctarr_bl_skullstripped=ncctarr_bl
    ncctarr_bl_skullstripped[ncctarr_bl_skullstripped>100]=0
    newncctimg_bl_SS=sitk.GetImageFromArray(ncctarr_bl_skullstripped)
    newncctimg_bl_SS.CopyInformation(newncctimg_bl)
    sitk.WriteImage(newncctimg_bl_SS,output_folder+str(cid)+'/'+str(cid)+'_NCCT_corrected_baseline_skullstripped.nii')
    
 
    arr1 = sitk.GetArrayFromImage(newncctimg_bl)
    arr1= rewrite_dim(arr1)
    nonconarray=np.transpose(arr1,(1,2,0))   
    mymontage=imageutils.montage(nonconarray)
    rescale_noncon=imageutils.imrescale(mymontage,[np.min(mymontage),100],[0,1])
    imageutils.imsave(output_folder + cid + '/' + cid +'_' +'noncon.png' ,rescale_noncon)
    
    arr2 = sitk.GetArrayFromImage(newncctimg_bl_SS)
    arr2= rewrite_dim(arr2)
    nonconarray=np.transpose(arr2,(1,2,0))   
    mymontage=imageutils.montage(nonconarray)
    rescale_noncon=imageutils.imrescale(mymontage,[np.min(mymontage),100],[0,1])
    imageutils.imsave(output_folder + cid + '/' + cid +'_' +'noncon_skullstripped.png' ,rescale_noncon)
    
    if BL_numofslabs==1 and FU_numofslabs==1:   
        slab2NCCT(FU_LOC,output_folder,cid,'slab0','FU',followup_mod)
        slab2NCCT(BL_LOC,output_folder,cid,'slab0','BL',baseline_mod)
        
    elif BL_numofslabs==2 and FU_numofslabs==1: 
        slab2NCCT(FU_LOC,output_folder,cid,'slab0','FU',followup_mod)
        slab2NCCT(BL_LOC,output_folder,cid,'slab1','BL',baseline_mod)
        slab2NCCT(BL_LOC,output_folder,cid,'slab0','BL',baseline_mod)
        merge2slabs(output_folder,'BL',cid)
        
        
    elif BL_numofslabs==2 and FU_numofslabs==2: 
        slab2NCCT(FU_LOC,output_folder,cid,'slab0','FU',followup_mod)
        slab2NCCT(FU_LOC,output_folder,cid,'slab1','FU',followup_mod)
        slab2NCCT(BL_LOC,output_folder,cid,'slab0','BL',baseline_mod)
        slab2NCCT(BL_LOC,output_folder,cid,'slab1','BL',baseline_mod)
        merge2slabs(output_folder,'BL',cid)
        merge2slabs(output_folder,'FU',cid)
        
    elif BL_numofslabs==2 and FU_numofslabs==0:
        slab2NCCT(BL_LOC,output_folder,cid,'slab0','BL',baseline_mod)
        slab2NCCT(BL_LOC,output_folder,cid,'slab1','BL',baseline_mod)
        merge2slabs(output_folder,'BL',cid)
        
    return


def registerFU2BL(cid,input_folder,output_folder):

    caseflag1="BL_MR_FU_MR"
    caseflag2="BL_CT_FU_MR"
    caseflag3="BL_CT_FU_CT"
    caseflag4="BL_2CT_FU_2CT"
    caseflag5="BL_2CT_FU_MR"
    caseflag6="BL_2CT_FU_CT"
    caseflag7="BL_2CT_FU_NA"
    
    flag=''
    if os.path.isdir(input_folder +'/'+str(cid)+'/'+'BL/Results_PWI_DWI_R47/') and os.path.isdir(input_folder +'/'+str(cid)+'/'+'FU/Results_PWI_DWI_R47/'):
        flag=caseflag1
        print flag
        FU_LOC=input_folder +'/'+str(cid)+'/'+'FU/Results_PWI_DWI_R47'
        BL_LOC=input_folder +'/'+str(cid)+'/'+'BL/Results_PWI_DWI_R47'
        baseline_mod='MR'
        followup_mod='MR'
        BL_numofslabs=1;
        FU_numofslabs=1;
    elif os.path.isdir(input_folder +'/'+str(cid)+'/'+'BL/Results_CTP_R47/') and os.path.isdir(input_folder +'/'+str(cid)+'/'+'FU/Results_PWI_DWI_R47/'):
        flag=caseflag2
        print flag
        FU_LOC=input_folder +'/'+str(cid)+'/'+'FU/Results_PWI_DWI_R47'
        BL_LOC=input_folder +'/'+str(cid)+'/'+'BL/Results_CTP_R47'
        baseline_mod='CT'
        followup_mod='MR'
        BL_numofslabs=1;
        FU_numofslabs=1;
    elif os.path.isdir(input_folder +'/'+str(cid)+'/'+'BL/Results_CTP_R47/') and os.path.isdir(input_folder +'/'+str(cid)+'/'+'FU/Results_CTP_R47/'):
        flag=caseflag3
        print flag
        FU_LOC=input_folder +'/'+str(cid)+'/'+'FU/Results_CTP_R47'
        BL_LOC=input_folder +'/'+str(cid)+'/'+'BL/Results_CTP_R47'
        baseline_mod='CT'
        followup_mod='CT'
        BL_numofslabs=1;
        FU_numofslabs=1;        
    elif os.path.isdir(input_folder +'/'+str(cid)+'/'+'BL/Results_CTP_2SLABS_R47/') and os.path.isdir(input_folder +'/'+str(cid)+'/'+'FU/Results_CTP_2SLABS_R47/'):
        flag=caseflag4
        print flag
        FU_LOC=input_folder +'/'+str(cid)+'/'+'FU/Results_CTP_2SLABS_R47'
        BL_LOC=input_folder +'/'+str(cid)+'/'+'BL/Results_CTP_2SLABS_R47'
        baseline_mod='CT'
        followup_mod='CT'
        BL_numofslabs=2;
        FU_numofslabs=2;        
    elif os.path.isdir(input_folder +'/'+str(cid)+'/'+'BL/Results_CTP_2SLABS_R47/') and os.path.isdir(input_folder +'/'+str(cid)+'/'+'FU/Results_PWI_DWI_R47/'):
        flag=caseflag5
        print flag
        FU_LOC=input_folder +'/'+str(cid)+'/'+'FU/Results_PWI_DWI_R47'
        BL_LOC=input_folder +'/'+str(cid)+'/'+'BL/Results_CTP_2SLABS_R47'
        baseline_mod='CT'
        followup_mod='MR'
        BL_numofslabs=2;
        FU_numofslabs=1;  
    elif os.path.isdir(input_folder +'/'+str(cid)+'/'+'BL/Results_CTP_2SLABS_R47/') and os.path.isdir(input_folder +'/'+str(cid)+'/'+'FU/Results_CTP_R47/'):
        flag=caseflag6
        print flag
        FU_LOC=input_folder +'/'+str(cid)+'/'+'FU/Results_CTP_R47'
        BL_LOC=input_folder +'/'+str(cid)+'/'+'BL/Results_CTP_2SLABS_R47'
        baseline_mod='CT'
        followup_mod='CT'
        BL_numofslabs=2;
        FU_numofslabs=1;  
        
    elif os.path.isdir(input_folder +'/'+str(cid)+'/'+'BL/Results_CTP_2SLABS_R47/') and not os.path.isdir(input_folder +'/'+str(cid)+'/'+'FU/'):
        flag=caseflag7
        print flag
        FU_LOC='NA'
        BL_LOC=input_folder +'/'+str(cid)+'/'+'BL/Results_CTP_2SLABS_R47'
        baseline_mod='CT'
        followup_mod='NA'
        BL_numofslabs=2;
        FU_numofslabs=0; 
        
    if flag==caseflag1 or flag==caseflag2 or flag==caseflag3:
        registerFU2BL_singleslab_sufficient_zcoverage(FU_LOC,BL_LOC,output_folder,cid,BL_numofslabs,FU_numofslabs,baseline_mod,followup_mod)
    elif flag==caseflag4 or flag==caseflag5 or flag==caseflag6: 
        registerFUBL2NCCT_insufficient_zcoverage(FU_LOC,BL_LOC,output_folder,cid,BL_numofslabs,FU_numofslabs,baseline_mod,followup_mod)
    elif flag==caseflag7:
        registerFUBL2NCCT_insufficient_zcoverage(FU_LOC,BL_LOC,output_folder,cid,BL_numofslabs,FU_numofslabs,baseline_mod,followup_mod)
    return

def createPNGs(tmaxgray_full_path,tmaxmask_full_path,outputfile_full_path):
    
    tmaxgray = sitk.ReadImage(tmaxgray_full_path)
    tmaxmask = sitk.ReadImage(tmaxmask_full_path)  
    arr1 = sitk.GetArrayFromImage(tmaxgray)
    arr1= rewrite_dim(arr1)
    tmaxgrayarray=np.transpose(arr1,(1,2,0))   
    mymontage=imageutils.montage(tmaxgrayarray)
    rescale_tmaxgray=imageutils.imrescale(mymontage,[np.min(mymontage),20],[0,1])
    rgbmont=np.stack( (rescale_tmaxgray,rescale_tmaxgray,rescale_tmaxgray),2)
    
    arr2 = sitk.GetArrayFromImage(tmaxmask)
    arr2= rewrite_dim(arr2)
    tmaxmaskarray=np.transpose(arr2,(1,2,0))   
    mymontage2=imageutils.montage(tmaxmaskarray)
    blue=np.stack( (mymontage2*0,mymontage2*0,mymontage2==1 ),2)
    green=np.stack( (mymontage2*0,mymontage2==2,mymontage2*0 ),2)
    yellow=np.stack( (mymontage2==3,mymontage2==3,mymontage2*0 ),2)
    red=np.stack( (mymontage2==4,mymontage2*0,mymontage2*0 ),2)
    
    composite_rgb_mask=blue+green+yellow+red
    
    final_tmax_rgb=  imageutils.rgbmaskonrgb(rgbmont,composite_rgb_mask.astype(np.float))
    imageutils.imsave(outputfile_full_path,final_tmax_rgb)
    
    return





#for cid in IDs:  #IDs:
#    print cid
if __name__=="__main__":
#     IDs=open('/Users/icasdb/Desktop/D3_R47_RANDOMIZED_FINAL/' + 'IDS.txt').read().split("\n")
     IDs=open('/Users/amar/registered_maps2/' + 'IDS_test.txt').read().split("\n")
#     IDs=open('/Users/icasdb/Desktop/nccts_for_registration_new/' + 'IDS.txt').read().split("\n")
     for cid in IDs:  #IDs:
         print cid

         input_folder='/Users/amar/D3_R47_RANDOMIZED_FINAL'
         output_folder='/Users/amar/registered_maps2/'
         registerFU2BL(cid,input_folder,output_folder)   

         
         
         

             

             
         
         


