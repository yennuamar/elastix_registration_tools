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

reader = sitk.ImageSeriesReader()

input_folder='/Users/icasdb/Desktop/NCCTS/127_NCCT/'
#dcm_list=glob.glob('/Users/icasdb/Desktop/nccts_for_registration/295/20170321/HEAD_WO/*dcm')
dcm_list=glob.glob(input_folder+'*dcm')
dcm_list=sorted(dcm_list)


reader.SetFileNames(dcm_list)
Fullimage= reader.Execute()
sitk.WriteImage(Fullimage,input_folder+'Fullimage_orig.nii')


pmap=sitk.GetDefaultParameterMap('rigid')
pmap["UseDirectionCosines"]=['true']
pmap["AutomaticTransformInitialization"]=['true']
pmap["Metric"]=['AdvancedNormalizedCorrelation']
elf=sitk.ElastixImageFilter()
elf.SetFixedImage(Fullimage)
elf.SetMovingImage(Fullimage)
elf.SetParameterMap(pmap)
elf.Execute()

transformParameterMap =elf.GetTransformParameterMap()
sitk.WriteParameterFile(transformParameterMap[0],input_folder+'Registerfull2full.xfm.txt')

transformParameterMap[0]["Spacing"]=('0.488281','0.488281','5')
transformParameterMap[0]["Size"]=('512','512','32')
transformParameterMap[0]["FinalBSplineInterpolationOrder"]=('1')

#transformParameterMap[0]["Origin"]=(str(Fullimage.GetOrigin()[0]),str(Fullimage.GetOrigin()[1]),str(Fullimage.GetOrigin()[2]))
#transformParameterMap[0]["Direction"]=(str(Fullimage.GetDirection()[0]),str(Fullimage.GetDirection()[1]),str(Fullimage.GetDirection()[2]),str(Fullimage.GetDirection()[3]),str(Fullimage.GetDirection()[4]),str(Fullimage.GetDirection()[5]),str(Fullimage.GetDirection()[6]),str(Fullimage.GetDirection()[7]),str(Fullimage.GetDirection()[8]))
sitk.WriteParameterFile(transformParameterMap[0],input_folder+'Registerfull2full_NEW.xfm.txt')
transformixImageFilter = sitk.TransformixImageFilter()
transformixImageFilter.SetTransformParameterMap(transformParameterMap)
transformixImageFilter.SetMovingImage(Fullimage)
transformixImageFilter.Execute()

FI=transformixImageFilter.GetResultImage()
#FI1.SetOrigin(Fullimage.GetOrigin())
#FI1.SetDirection(Fullimage.GetDirection())
sitk.WriteImage(FI,input_folder+'finalimage.nii')

