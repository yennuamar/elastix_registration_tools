#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 12:31:00 2018

@author: icasdb
"""


import SimpleITK as sitk
import glob


input_folder='/Users/icasdb/Desktop/NCCTS/127_NCCT/'
#dcm_list=glob.glob('/Users/icasdb/Desktop/nccts_for_registration/295/20170321/HEAD_WO/*dcm')
dcm_list=glob.glob(input_folder+'*dcm')
dcm_list=sorted(dcm_list)

Fullimage= sitk.ReadImage(dcm_list)
sitk.WriteImage(Fullimage,input_folder+'Fullimage_orig.nii')


A= sitk.ReadImage(dcm_list[16:40])
sitk.WriteImage(A,input_folder+'A_orig.nii')
#A.SetOrigin((-125.0, -114.98999786376953, 18.5939998626709+16*2.65))
B= sitk.ReadImage(dcm_list[0:16])
sitk.WriteImage(B,input_folder+'B_orig.nii')
#B.SetOrigin((-125.0, -114.98999786376953, 18.5939998626709))

affine=sitk.AffineTransform(3)
#outimage=sitk.Resample(B,(512,512,32),affine,sitk.sitkLinear,(0,0,0),(0.488281,0.488281,5),(1,0,0,0,1,0,0,0,1))
outimage_lowthickness=sitk.Resample(A,(512,512,32),affine,sitk.sitkLinear,Fullimage.GetOrigin(),(0.488281,0.488281,5),Fullimage.GetDirection())

sitk.WriteImage(outimage_lowthickness,input_folder+'A.nii')

outimage_highthickness=sitk.Resample(B,(512,512,32),affine,sitk.sitkLinear,Fullimage.GetOrigin(),(0.488281,0.488281,5),Fullimage.GetDirection())

sitk.WriteImage(outimage_highthickness,input_folder+'B.nii')

pmap=sitk.GetDefaultParameterMap('rigid')




