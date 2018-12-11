#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 13:23:23 2018

@author: icasdb
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 12:31:00 2018

@author: icasdb
"""


import SimpleITK as sitk
import glob
import numpy as np
import dicom

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
    
    for i in range(len(unique_sorted_thickness_list)):   
        for j in range(len(dcm_sorted_list)):
            x1=dicom.read_file(dcm_sorted_list[j])
            if float(x1.SliceThickness)==unique_sorted_thickness_list[i]:
                dcm_sorted_thickness_list.append(dcm_sorted_list[j])
                
        dcm_lists.append(dcm_sorted_thickness_list) 
        dcm_sorted_thickness_list=[]

    return dcm_sorted_list, dcm_lists
        
if __name__=="__main__":
    cid=295
    input_folder='/Users/icasdb/Desktop/NCCTS/'+str(cid)+'/'
    dcm_list=glob.glob(input_folder+'*dcm')
    full_sorted_dcm_list, dcm_thickness_lists=dicom_sorter_thickness_splitter(dcm_list)
    
    z1=dicom.read_file(full_sorted_dcm_list[0])
    zn=dicom.read_file(full_sorted_dcm_list[len(full_sorted_dcm_list)-1])
    zcoverage=float(zn.SliceLocation)-float(z1.SliceLocation)
    
    lower_dcm_list=dcm_thickness_lists[0]
    upper_dcm_list=dcm_thickness_lists[1]
    
    x1=dicom.read_file(lower_dcm_list[0])
    y1=dicom.read_file(lower_dcm_list[1])
    A_zspacing =  float(y1.SliceLocation)-float(x1.SliceLocation)
    A_pixelspacing = float(x1.PixelSpacing[0])
    
    x2=dicom.read_file(upper_dcm_list[0])
    y2=dicom.read_file(upper_dcm_list[1])
    
    B_zspacing =  float(y2.SliceLocation)-float(x2.SliceLocation)
    B_pixelspacing = float(y2.PixelSpacing[0])
       
    A= sitk.ReadImage(lower_dcm_list)
#    A.SetSpacing((A_pixelspacing,A_pixelspacing,A_zspacing))
    A.SetDirection((1,0,0,0,1,0,0,0,1))
    
    B= sitk.ReadImage(upper_dcm_list)
#    B.SetSpacing((B_pixelspacing,B_pixelspacing,B_zspacing))
    B.SetDirection((1,0,0,0,1,0,0,0,1))
       
    sitk.WriteImage(A,input_folder+'lower_orig.nii')
    sitk.WriteImage(B,input_folder+'upper_orig.nii')
    
    SimpleElastix=sitk.ElastixImageFilter()
    parameterMap = SimpleElastix.ReadParameterFile('/Users/icasdb/Desktop/DWINCCT/CODE/rigid_D3.txt')
    
    SimpleElastix.SetFixedImage(A)
    SimpleElastix.SetMovingImage(A)
    SimpleElastix.SetParameterMap(parameterMap)
    SimpleElastix.Execute()
    
    transformParameterMap =SimpleElastix.GetTransformParameterMap()
    sitk.WriteParameterFile(transformParameterMap[0],input_folder+'tranform_param.xfm.txt')
    new_zcoverage=round(zcoverage/B_zspacing)
    transformParameterMap[0]["Spacing"]=(str(B_pixelspacing),str(B_pixelspacing),str(B_zspacing))
    transformParameterMap[0]["Size"]=('512','512',str(new_zcoverage))
    transformParameterMap[0]["FinalBSplineInterpolationOrder"]=('1')
    sitk.WriteParameterFile(transformParameterMap[0],input_folder+'tranform_param_new.xfm.txt')
    transformixImageFilter = sitk.TransformixImageFilter()
    transformixImageFilter.SetTransformParameterMap(transformParameterMap)
    transformixImageFilter.SetMovingImage(A)
    transformixImageFilter.Execute()
    
    FI1=transformixImageFilter.GetResultImage()

    sitk.WriteImage(FI1,input_folder+'lower.nii')
    
    transformixImageFilter = sitk.TransformixImageFilter()
    transformixImageFilter.SetTransformParameterMap(transformParameterMap)
    transformixImageFilter.SetMovingImage(B)
    transformixImageFilter.Execute()
    
    FI2=transformixImageFilter.GetResultImage()
    sitk.WriteImage(FI2,input_folder+'upper.nii')
    
    temparr1=sitk.GetArrayFromImage(A)
    ones_arr1=np.ones(temparr1.shape)
    ones_img1=sitk.GetImageFromArray(ones_arr1)
    ones_img1.CopyInformation(A)
    
    transformixImageFilter = sitk.TransformixImageFilter()
    transformixImageFilter.SetTransformParameterMap(transformParameterMap)
    transformixImageFilter.SetMovingImage(ones_img1)
    transformixImageFilter.Execute()
    
    onesFI1=transformixImageFilter.GetResultImage()
    
    onesFI1arr=sitk.GetArrayFromImage(onesFI1)
    
    FI1arr=sitk.GetArrayFromImage(FI1)
    FI2arr=sitk.GetArrayFromImage(FI2)
    
    FI1arr[onesFI1arr<1]=FI2arr[onesFI1arr<1]
    
    finalimage=sitk.GetImageFromArray(FI1arr)
    finalimage.CopyInformation(onesFI1)
    
    sitk.WriteImage(finalimage,input_folder+str(cid)+'.nii')
    
    
    














