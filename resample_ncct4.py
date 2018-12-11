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



input_folder='/Users/icasdb/Desktop/NCCTS/127_NCCT/'
#dcm_list=glob.glob('/Users/icasdb/Desktop/nccts_for_registration/295/20170321/HEAD_WO/*dcm')
dcm_list=glob.glob(input_folder+'*dcm')
dcm_list=sorted(dcm_list)


Fullimage= sitk.ReadImage(dcm_list)
sitk.WriteImage(Fullimage,input_folder+'Fullimage_orig.nii')


A= sitk.ReadImage(dcm_list[16:40])
#A.SetOrigin((0,0,2.65*16))
sitk.WriteImage(A,input_folder+'A_orig.nii')

B= sitk.ReadImage(dcm_list[0:16])
#B.SetOrigin((0,0,0))

sitk.WriteImage(B,input_folder+'B_orig.nii')
#B.SetOrigin((-125.0, -114.98999786376953, 18.5939998626709))

SimpleElastix=sitk.ElastixImageFilter()
parameterMap = SimpleElastix.ReadParameterFile('/Users/icasdb/Desktop/DWINCCT/CODE/rigid_D3.txt')
SimpleElastix.SetFixedImage(A)
SimpleElastix.SetMovingImage(A)
SimpleElastix.SetParameterMap(parameterMap)
SimpleElastix.Execute()

transformParameterMap =SimpleElastix.GetTransformParameterMap()
sitk.WriteParameterFile(transformParameterMap[0],input_folder+'Registerfull2full.xfm.txt')

transformParameterMap[0]["Spacing"]=('0.488281','0.488281','5.29')
transformParameterMap[0]["Size"]=('512','512','32')
transformParameterMap[0]["FinalBSplineInterpolationOrder"]=('1')
sitk.WriteParameterFile(transformParameterMap[0],input_folder+'Registerfull2full_NEW.xfm.txt')
transformixImageFilter = sitk.TransformixImageFilter()
transformixImageFilter.SetTransformParameterMap(transformParameterMap)
transformixImageFilter.SetMovingImage(A)
transformixImageFilter.Execute()

FI1=transformixImageFilter.GetResultImage()

sitk.WriteImage(FI1,input_folder+'A.nii')

SimpleElastix=sitk.ElastixImageFilter()
parameterMap = SimpleElastix.ReadParameterFile('/Users/icasdb/Desktop/DWINCCT/CODE/rigid_D3.txt')
SimpleElastix.SetFixedImage(B)
SimpleElastix.SetMovingImage(B)
SimpleElastix.SetParameterMap(parameterMap)
SimpleElastix.Execute()

transformParameterMap =SimpleElastix.GetTransformParameterMap()
sitk.WriteParameterFile(transformParameterMap[0],input_folder+'Registerfull2full.xfm.txt')

transformParameterMap[0]["Spacing"]=('0.488281','0.488281','5.29')
transformParameterMap[0]["Size"]=('512','512','32')
transformParameterMap[0]["FinalBSplineInterpolationOrder"]=('1')
sitk.WriteParameterFile(transformParameterMap[0],input_folder+'Registerfull2full_NEW.xfm.txt')
transformixImageFilter = sitk.TransformixImageFilter()
transformixImageFilter.SetTransformParameterMap(transformParameterMap)
transformixImageFilter.SetMovingImage(B)
transformixImageFilter.Execute()

FI2=transformixImageFilter.GetResultImage()

sitk.WriteImage(FI2,input_folder+'B.nii')

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

temparr2=sitk.GetArrayFromImage(B)
ones_arr2=np.ones(temparr2.shape)
ones_img2=sitk.GetImageFromArray(ones_arr2)
ones_img2.CopyInformation(B)

transformixImageFilter = sitk.TransformixImageFilter()
transformixImageFilter.SetTransformParameterMap(transformParameterMap)
transformixImageFilter.SetMovingImage(ones_img2)
transformixImageFilter.Execute()

onesFI2=transformixImageFilter.GetResultImage()
onesFI2arr=sitk.GetArrayFromImage(onesFI2)

FI1arr=sitk.GetArrayFromImage(FI1)
FI2arr=sitk.GetArrayFromImage(FI2)

FI1arr[onesFI1arr<1]=FI2arr[onesFI1arr<1]

finalimage=sitk.GetImageFromArray(FI1arr)
finalimage.CopyInformation(onesFI1)

sitk.WriteImage(finalimage,input_folder+'finalimage.nii')

















