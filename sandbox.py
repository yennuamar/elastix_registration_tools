#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 12:31:00 2018

@author: icasdb
"""


import SimpleITK as sitk
import glob


reader = sitk.ImageSeriesReader()
dcm_list=glob.glob('/Users/icasdb/Desktop/defuse3_test3/289/BL/Results_CTP_2SLABS_R47/results/series241_baseline_slab0_slice*dcm')
reader.SetFileNames(sorted(dcm_list))
A = reader.Execute()
B=sitk.ReadImage('/Users/icasdb/Desktop/defuse3_test3/289/NCCT/289.nii')

pmap=sitk.GetDefaultParameterMap('rigid')

sitk.WriteImage(A,'/Users/icasdb/Desktop/baseline.nii')


clamper=sitk.ClampImageFilter()
B_clamped=clamper.Execute(B,sitk.sitkFloat32,0,6000)
sitk.WriteImage(B_clamped,'/Users/icasdb/Desktop/ncct.nii')

A.SetDirection((1,0,0,0,1,0,0,0,1))
B_clamped.SetDirection((1,0,0,0,1,0,0,0,1))
#B_clamped.SetDirection
#A.SetOrigin(B_clamped.GetOrigin())
elf=sitk.ElastixImageFilter()
elf.SetFixedImage(B_clamped)
elf.SetMovingImage(A)
pmap["UseDirectionCosines"]=['true']
pmap["AutomaticTransformInitialization"]=['true']
pmap["Metric"]=['AdvancedNormalizedCorrelation']

elf.SetParameterMap(pmap)

A.GetDirection()
B_clamped.GetDirection()


elf.Execute()


sitk.WriteImage(elf.GetResultImage(),'/Users/icasdb/Desktop/ncct2baseline.nii')
