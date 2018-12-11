#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 11:18:41 2018

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

if __name__=="__main__":

     IDs=open('/Users/icasdb/Desktop/nccts_for_registration_new/' + 'IDS.txt').read().split("\n")
     for cid in IDs:  #IDs:
         print cid


         input_folder='/Users/icasdb/Desktop/nccts_for_registration_new/'
         ncct_img=sitk.ReadImage(input_folder+cid+'_tiltcorrected.nii')
         arr1 = sitk.GetArrayFromImage(ncct_img)
         temparrshape=arr1.shape
         spacing=ncct_img.GetSpacing()
         
         fig=plt.figure()
         ax=plt.gca()
         ax.imshow(arr1[:,:,256],cmap='Greys_r',vmin=0,vmax=50)
#         ax.set_aspect(temparrshape[2]/temparrshape[0])
         ax.set_aspect(spacing[2]/spacing[1])
         ax.invert_yaxis()
#         ax.axes.get_xaxis().set_visible(False)
#         ax.axes.get_yaxis().set_visible(False)
         fig.savefig(input_folder + cid +'_tiltcorrected_sag.png')
         plt.close(fig)
         