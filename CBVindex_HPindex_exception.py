#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 14:35:35 2018

@author: icasdb
"""

import SimpleITK as sitk
import numpy as np
#import dicom2nifti
import glob, os
import dicom
import shutil
import imageutils
import scipy
#import dicomutils
import matplotlib.pyplot as plt
import rapid47
import re

from PIL import Image, ImageDraw, ImageFont
import xlsxwriter


def txt2vol(location,txt,matrix,fontsize):
    #location is valued 1-8 where 1-4 is left side of matrix top to bottom in 4 sections and 5-8 is corresponding right sided sections    
    
    matshape=matrix.shape
    xy=location
    mymat=np.zeros(matshape,np.int16)
    font = ImageFont.truetype('Arial.ttf', fontsize) 
    # starting position of the message
    image = Image.new("I", (matshape[1], matshape[0])) #create an image background
    draw = ImageDraw.Draw(image)          #create a draw object on this image

    (x, y) = (xy[0], xy[1])
 
    draw.text((x, y), txt , fill=1, font=font) #draw txt on image
    textarr=np.array(image)        
    textarr=np.stack( (textarr,textarr,textarr),2)                                      #make image a numpy array
    mymat=matrix 
    mymat[textarr.astype(np.int16)>0]=textarr[textarr.astype(np.int16)>0]                     #insert it fully into another numpy array - you should just overwrite a section of the image here Amarnath
    return mymat
  

def rewrite_dim(arr1):
    temparrshape=arr1.shape
    if temparrshape[1]<temparrshape[2]:
        arr1=arr1[:,:,0:temparrshape[1]]
    else:
        arr1=arr1[:,0:temparrshape[2],:]
        
    return arr1

def logread(location):
    fid=open(location,'r')      
    logtxt=fid.read()
    fid.close()  
    return logtxt

def create_tmax_PNGs(tmaxgray_image,tmaxmask_image):
    
    tmaxgray = tmaxgray_image
    tmaxmask = tmaxmask_image  
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
    green=np.stack( (mymontage2*0,np.logical_or(mymontage2==2,mymontage2==3),mymontage2*0 ),2)
    red=np.stack( (mymontage2==4,mymontage2*0,mymontage2*0 ),2)
    
    composite_rgb_mask=green+red
    
    final_tmax_rgb=  imageutils.rgbmaskonrgb(rgbmont,composite_rgb_mask.astype(np.float))
    
#    imageutils.imsave(outputpng_full_path,final_tmax_rgb)
#    
    return final_tmax_rgb


if __name__=="__main__":
     IDs=open('/Users/amar/registered_maps2/' + 'IDS_test.txt').read().split("\n")
     cid_list=[]
     BL_core_vol_list=[]
     BL_Tmax6_vol_list=[]
     BL_Tmax10_vol_list=[]
     BL_CBVindex_list=[]
     BL_HPindex_list=[]
#     FU_core_vol_list=[]
#     FU_Tmax6_vol_list=[]
#     FU_Tmax10_vol_list=[]
#     FU_CBVindex_basedon_BLtmax6_list=[]
#     FU_HPindex_list=[]
#     FU_HPindex_basedon_BLtmax6_list=[]
     reperfusionpercent_list=[]   

         
     
     for cid in IDs:  #IDs:
         print cid
         
#         input_folder='/Users/amar/D3_R47_RANDOMIZED_FINAL'
         input_folder='/Users/amar/registered_maps2/'  
     
         if not (os.path.exists(input_folder + cid)):
             cid_list.append(cid)
             BL_core_vol_list.append("")
             BL_Tmax6_vol_list.append("")
             BL_Tmax10_vol_list.append("")
             BL_CBVindex_list.append("")
             BL_HPindex_list.append("")
#             FU_core_vol_list.append("")
#             FU_Tmax6_vol_list.append("")
#             FU_Tmax10_vol_list.append("")
#             FU_CBVindex_basedon_BLtmax6_list.append("")
#             FU_HPindex_list.append("")
#             reperfusionpercent_list.append("")
#             FU_HPindex_basedon_BLtmax6_list.append("")
             print(cid+ "doesn't exist")
             continue
          
         
         BL_flag=""
         if os.path.exists(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_rcbv_slice_merged.nii'):            
             BL_rcbv_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_rcbv_slice_merged.nii') 
             BL_tmaxgray_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_tmax_slice_merged.nii')
             BL_tmax_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_tmax_mask_merged.nii')
             BL_tmax6_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_tmax6_mask_merged.nii')
             BL_core_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_core_mask_merged.nii')
             BL_rcbv_mask_outside_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_rcbv_mask_outside_merged.nii')
             BL_tissue_mask_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_tissue_mask_merged.nii')
             BL_tissue_mask0_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_tissue_mask_slab0.nii')
             BL_tissue_mask1_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_tissue_mask_slab1.nii')
             BL_rcbv0_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_rcbv_slice_slab0.nii')
             BL_rcbv1_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_rcbv_slice_slab1.nii')
             BL_rcbv_outside_mask0_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_rcbv_mask_outside_slab0.nii')
             BL_rcbv_outside_mask1_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_rcbv_mask_outside_slab1.nii')
             BL_flag=2
             BL_fontsize=50
             BL_indent=70
         elif os.path.exists(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_rcbv_slice_slab0.nii'):
             BL_rcbv_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_rcbv_slice_slab0.nii')  
             BL_tmaxgray_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_tmax_slice_slab0.nii') 
             BL_tmax_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_segm_mask_view1_Thresholded_Tmax_Parameter_View_slab0.nii')             
             BL_tmax6_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_segm_mask_view0_Thresholded_Tmax_Parameter_View_slab0.nii')
             BL_core_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_segm_mask_view0_Thresholded_core_Parameter_View_slab0.nii')
             BL_rcbv_mask_outside_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_rcbv_mask_outside_slab0.nii')
             BL_tissue_mask_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL2NCCT_coregistration_tissue_mask_slab0.nii')
             BL_fontsize=50
             BL_indent=70
             BL_flag=1
         elif os.path.exists(input_folder + cid + '/' + cid +'_' +'BL_rcbv_slice_slab0.nii'):
             BL_rcbv_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL_rcbv_slice_slab0.nii')   
             BL_tmaxgray_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL_tmax_slice_slab0.nii') 
             BL_tmax_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL_segm_mask_view1_Thresholded_Tmax_Parameter_View_slab0.nii')      
             BL_tmax6_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL_segm_mask_view0_Thresholded_Tmax_Parameter_View_slab0.nii')
             BL_core_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL_segm_mask_view0_Thresholded_core_Parameter_View_slab0.nii')
             BL_rcbv_mask_outside_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL_rcbv_mask_outside_slab0.nii')
             BL_tissue_mask_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'BL_tissue_mask_slab0.nii')
             BL_fontsize=13
             BL_indent=40
             BL_flag=0
         BL_rcbv_arr=sitk.GetArrayFromImage(BL_rcbv_image)
         BL_rcbv_arr=rewrite_dim(BL_rcbv_arr)
         BL_tmax_arr=sitk.GetArrayFromImage(BL_tmax_image)
         BL_tmax_arr=rewrite_dim(BL_tmax_arr) 
         BL_tmax6_arr=sitk.GetArrayFromImage(BL_tmax6_image)
         BL_tmax6_arr=rewrite_dim(BL_tmax6_arr) 
         BL_core_arr=sitk.GetArrayFromImage(BL_core_image)
         BL_core_arr=rewrite_dim(BL_core_arr) 
         BL_rcbv_mask_outside_arr=sitk.GetArrayFromImage(BL_rcbv_mask_outside_image)
         BL_rcbv_mask_outside_arr=rewrite_dim(BL_rcbv_mask_outside_arr) 
         BL_tissue_arr=sitk.GetArrayFromImage(BL_tissue_mask_image)
         BL_tissue_arr=rewrite_dim(BL_tissue_arr) 
         
         if BL_flag==2:
             print('BL2slabs')
             BL_tissue0_arr=sitk.GetArrayFromImage(BL_tissue_mask0_image)
             BL_tissue0_arr=rewrite_dim(BL_tissue0_arr) 
             BL_tissue1_arr=sitk.GetArrayFromImage(BL_tissue_mask1_image)
             BL_tissue1_arr=rewrite_dim(BL_tissue1_arr) 
             
             BL_rcbv0_arr=sitk.GetArrayFromImage(BL_rcbv0_image)
             BL_rcbv0_arr=rewrite_dim(BL_rcbv0_arr) 
             BL_rcbv1_arr=sitk.GetArrayFromImage(BL_rcbv1_image)
             BL_rcbv1_arr=rewrite_dim(BL_rcbv1_arr) 
             
             BL_rcbv_outside_mask0_arr=sitk.GetArrayFromImage(BL_rcbv_outside_mask0_image)
             BL_rcbv_outside_mask0_arr=rewrite_dim(BL_rcbv_outside_mask0_arr) 
             BL_rcbv_outside_mask1_arr=sitk.GetArrayFromImage(BL_rcbv_outside_mask1_image)
             BL_rcbv_outside_mask1_arr=rewrite_dim(BL_rcbv_outside_mask1_arr) 
             
             mean_outside_slab0=np.mean(BL_rcbv0_arr[BL_rcbv_outside_mask0_arr>0])
             BL_rcbv0_arr=BL_rcbv0_arr/mean_outside_slab0
             mean_outside_slab1=np.mean(BL_rcbv1_arr[BL_rcbv_outside_mask1_arr>0])
             BL_rcbv1_arr=BL_rcbv1_arr/mean_outside_slab1
             BL_rcbv_arr_norm=BL_rcbv1_arr
             BL_rcbv_arr_norm[BL_tissue0_arr>0]=BL_rcbv0_arr[BL_tissue0_arr>0]
             BL_CBVindex=np.mean(BL_rcbv_arr_norm[np.logical_and(BL_tmax6_arr>0,BL_tissue_arr>0)])
             BL_CBVindex0=np.mean(BL_rcbv0_arr[np.logical_and(BL_tmax6_arr>0,BL_tissue0_arr>0)])
             BL_CBVindex1=np.mean(BL_rcbv1_arr[np.logical_and(BL_tmax6_arr>0,BL_tissue1_arr>0)])
             BL_CBVindex0= round(BL_CBVindex0, 2)
             BL_CBVindex1=round(BL_CBVindex1, 2)

         elif BL_flag==1 or BL_flag==0:
             print('BL1slab')
             mean_outside=np.mean(BL_rcbv_arr[np.logical_and(BL_rcbv_mask_outside_arr>0,BL_tissue_arr>0)])
             BL_rcbv_arr_norm=BL_rcbv_arr/mean_outside
             BL_CBVindex=np.mean(BL_rcbv_arr_norm[np.logical_and(BL_tmax6_arr>0,BL_tissue_arr>0)])
             BL_CBVindex0=""
             BL_CBVindex1=""

         BL_HPindex=np.sum((BL_tmax_arr==4).astype(float))/np.sum((BL_tmax6_arr>0).astype(float))
         BL_core_spacing=BL_core_image.GetSpacing()
         BL_tmax6_spacing=BL_tmax6_image.GetSpacing()
         BL_spacing=BL_rcbv_image.GetSpacing()
         BL_Tmax6_vol=(np.sum((BL_tmax6_arr>0).astype(float))*BL_spacing[0]*BL_spacing[1]*BL_spacing[2])/1000
         BL_Tmax10_vol=(np.sum((BL_tmax_arr==4).astype(float))*BL_spacing[0]*BL_spacing[1]*BL_spacing[2])/1000
         BL_core_vol=(np.sum((BL_core_arr>0).astype(float))*BL_spacing[0]*BL_spacing[1]*BL_spacing[2])/1000
         
         BL_Tmax6_vol=round(BL_Tmax6_vol,2)
         BL_Tmax10_vol=round(BL_Tmax10_vol,2)
         BL_core_vol=round(BL_core_vol,2)
    
         print("BL_Tmax6_vol is " + str(BL_Tmax6_vol))
         print("BL_Tmax10_vol is " + str(BL_Tmax10_vol))
         print("BL_core_vol is " + str(BL_core_vol))
         
         try:
             BL_HPindex= round(BL_HPindex, 2)
         except: 
             BL_HPindex=str(BL_HPindex)
             
         try:   
             BL_CBVindex= round(BL_CBVindex, 2)
         except:
             BL_CBVindex= str(BL_CBVindex)
         BL_tmax6_mask=np.transpose(BL_tmax6_arr.astype(int),(1,2,0))   
         BL_tmax6_edges=imageutils.get_edges(BL_tmax6_mask)
         BL_tmax6_mymontage=imageutils.montage(BL_tmax6_edges)
         BL_tmax6_rescale_edges=imageutils.imrescale(BL_tmax6_mymontage,[np.min(BL_tmax6_mymontage),np.max(BL_tmax6_mymontage)],[0,1])
         imageutils.imsave(input_folder + cid + '/' + cid +'_' +'BL_tmax6_edges.png' ,BL_tmax6_rescale_edges)
         print('BL_HPindex is '+ str(BL_HPindex))
         print('BL_CBVindex is '+ str(BL_CBVindex))
         

         
         BL_rcbv_arr_norm=np.transpose(BL_rcbv_arr_norm,(1,2,0))   
         BL_rcbv_mymontage=imageutils.montage(BL_rcbv_arr_norm)
         BL_rescale_rcbv_arr=imageutils.imrescale(BL_rcbv_mymontage,[0,3],[0,1])
         BL_rcbv_rgbmont=np.stack( (BL_rescale_rcbv_arr,BL_rescale_rcbv_arr,BL_rescale_rcbv_arr),2)        
         
         yellow=np.stack((BL_tmax6_mymontage==1,BL_tmax6_mymontage==1,BL_tmax6_mymontage*0 ),2)        
         final_img=imageutils.rgbmaskonrgb(BL_rcbv_rgbmont,yellow.astype(np.float))
         imageutils.imsave(input_folder + cid + '/' + cid +'_' +'BL_tmax6_edges_on_rcbv.png',final_img)         
           
         
         input_folder2='/Users/amar/D3_R47_RANDOMIZED_FINAL/'
         
         if os.path.isdir(input_folder2 +'/'+str(cid)+'/'+'BL/Results_PWI_DWI_R47/'):
            op_BL=rapid47.RAPID46OP(input_folder2 +'/'+str(cid)+'/'+'BL/Results_PWI_DWI_R47/')
            
            
            BL_slicethickness=float(op_BL.slicethickness_slab1)
            diff_slicethickness=BL_slicethickness-BL_spacing[2]            
            print(str(cid)+"  BL diff slicethickness" + str(diff_slicethickness))
            file = open("/Users/amar/registered_maps2/BL_diff slicethickness.txt","a") 
            file.write(str(cid)+"  BL diff slicethickness" + str(diff_slicethickness)+"\n")
            
#            BL_log_location=glob.glob(input_folder2 +'/'+str(cid)+'/'+'BL/Results_PWI_DWI_R47/'+'*processing.log.txt')
#            logtxt=logread(BL_log_location[0])
#            opt=re.search("Reconstructed slice thickness: (.*) mm",logtxt)
#            if not opt==None:
#                slicethickness=float(opt.group(1))
#                diff_slicethickness=slicethickness-BL_spacing[2]
#                print("BL diff slicethickness" + str(diff_slicethickness))
            
         elif os.path.isdir(input_folder2 +'/'+str(cid)+'/'+'BL/Results_CTP_R47/'):
            op_BL=rapid47.RAPID46OP(input_folder2 +'/'+str(cid)+'/'+'BL/Results_CTP_R47/')
         elif os.path.isdir(input_folder2 +'/'+str(cid)+'/'+'BL/Results_CTP_2SLABS_R47/'):
            op_BL=rapid47.RAPID46OP(input_folder2 +'/'+str(cid)+'/'+'BL/Results_CTP_2SLABS_R47/')
            
            
        
            
         if BL_flag==0:
             try:
                 BL_HPindex_orig=op_BL.HypoperfusionIndex_slab1[0]
                 BL_CBVindex_orig=op_BL.CBVIndex_slab1[0]
             except: 
                 BL_HPindex_orig=op_BL.HypoperfusionIndex_slab1
                 BL_CBVindex_orig=op_BL.CBVIndex_slab1
             BL_HPindex0_orig=""
             BL_HPindex1_orig=""
             BL_CBVindex0_orig=""
             BL_CBVindex1_orig=""

             try:
                 BL_CBVindex_orig=round(BL_CBVindex_orig, 2)
                 print("original BL_CBVindex is " + BL_CBVindex_orig)                 
             except:
                 print("original BL_CBVindex is " + str(BL_CBVindex_orig))
             try:
                 BL_HPindex_orig=round(BL_HPindex_orig, 2)
                 print("original BL_HPindex is " + BL_HPindex_orig)
             except:
                 print("original BL_HPindex is " + str(BL_HPindex_orig))
                 


                 
         elif BL_flag==1:  
             try:
                 BL_HPindex_orig=op_BL.HypoperfusionIndex_slab1[0]
                 BL_CBVindex_orig=op_BL.CBVIndex_slab1[0]
             except: 
                 BL_HPindex_orig=op_BL.HypoperfusionIndex_slab1
                 BL_CBVindex_orig=op_BL.CBVIndex_slab1        
             BL_HPindex0_orig=""
             BL_HPindex1_orig=""
             BL_CBVindex0_orig=""
             BL_CBVindex1_orig=""

             try:
                 BL_CBVindex_orig=round(BL_CBVindex_orig, 2)
                 print("original BL_CBVindex is " + BL_CBVindex_orig)                 
             except:
                 print("original BL_CBVindex is " + str(BL_CBVindex_orig))
             try:
                 BL_HPindex_orig=round(BL_HPindex_orig, 2)
                 print("original BL_HPindex is " + BL_HPindex_orig)
             except:
                 print("original BL_HPindex is " + str(BL_HPindex_orig))
                 
         elif BL_flag==2:
             BL_HPindex_orig=""
             BL_CBVindex_orig=""        
             BL_HPindex0_orig=op_BL.HypoperfusionIndex_slab1
             BL_HPindex1_orig=op_BL.HypoperfusionIndex_slab2
             BL_CBVindex0_orig=op_BL.CBVIndex_slab1 
             BL_CBVindex1_orig=op_BL.CBVIndex_slab2 
             
             try:
                 BL_CBVindex0_orig=round(BL_CBVindex0_orig, 2)
                 print("original BL_CBVindex slab0 is " + BL_CBVindex0_orig)
             except:
                 print("original BL_CBVindex slab0 is " + str(BL_CBVindex0_orig))
             try:
                 BL_HPindex0_orig=round(BL_HPindex0_orig, 2)
                 print("original BL_HPindex slab0 is " + BL_HPindex0_orig)
             except:
                 print("original BL_HPindex slab0 is " + str(BL_HPindex0_orig))
                 
             try:
                 BL_CBVindex1_orig=round(BL_CBVindex1_orig, 2)
                 print("original BL_CBVindex slab1 is " + BL_CBVindex1_orig)
             except:
                 print("original BL_CBVindex slab1 is " + str(BL_CBVindex1_orig))
             try:
                 BL_HPindex1_orig=round(BL_HPindex1_orig, 2)
                 print("original BL_HPindex slab1 is " + BL_HPindex1_orig)
             except:
                 print("original BL_HPindex slab1 is " + str(BL_HPindex1_orig))

                 

             
             
         temp=txt2vol([20,20],"CBV index: "+str(BL_CBVindex)+"   Slab0 CBV index: "+str(BL_CBVindex0)+"   Slab1 CBV index: "+str(BL_CBVindex1),final_img,BL_fontsize)
         temp=txt2vol([20,BL_indent],"CBV index orig: "+str(BL_CBVindex_orig)+"   Slab0 CBV index orig : "+str(BL_CBVindex0_orig)+"   Slab1 CBV index orig: "+str(BL_CBVindex1_orig),temp,BL_fontsize)
         imageutils.imsave(input_folder + cid + '/' + cid +'_' +'BL_CBVindex.png',temp)     
          
         
         BL_tmaxoverlayed_png=create_tmax_PNGs(BL_tmaxgray_image,BL_tmax_image)
         temp1=txt2vol([20,20],"Tmax6 vol(green): "+str(BL_Tmax6_vol)+"   Tmax10 vol(red): "+str(BL_Tmax10_vol)+"   Core vol: "+str(BL_core_vol)+"   HP index: "+str(BL_HPindex),BL_tmaxoverlayed_png,BL_fontsize)
         imageutils.imsave(input_folder + cid + '/' + cid +'_' +'BL_HPindex.png',temp1) 
         
         
         
#         FU_flag=""
#         if os.path.exists(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_rcbv_slice_merged.nii'):
#             FU_rcbv_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_rcbv_slice_merged.nii')  
#             FU_tmaxgray_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_tmax_slice_merged.nii')  
#             FU_tmax_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_tmax_mask_merged.nii')
#             FU_tmax6_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_tmax6_mask_merged.nii')
#             FU_core_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_core_mask_merged.nii')
#             FU_rcbv_mask_outside_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_rcbv_mask_outside_merged.nii')
#             FU_tissue_mask_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_tissue_mask_merged.nii')
#             FU_tissue_mask0_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_tissue_mask_slab0.nii')
#             FU_tissue_mask1_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_tissue_mask_slab1.nii')
#             FU_rcbv0_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_rcbv_slice_slab0.nii')
#             FU_rcbv1_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_rcbv_slice_slab1.nii')
#             FU_flag=2
#             FU_fontsize=50
#             FU_indent=70
#         elif os.path.exists(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_rcbv_slice_slab0.nii'):
#             FU_rcbv_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_rcbv_slice_slab0.nii')   
#             FU_tmaxgray_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_tmax_slice_slab0.nii') 
#             FU_tmax_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_segm_mask_view1_Thresholded_Tmax_Parameter_View_slab0.nii')             
#             FU_tmax6_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_segm_mask_view0_Thresholded_Tmax_Parameter_View_slab0.nii')
#             FU_core_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_segm_mask_view0_Thresholded_core_Parameter_View_slab0.nii')
#             FU_rcbv_mask_outside_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_rcbv_mask_outside_slab0.nii')
#             FU_tissue_mask_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2NCCT_coregistration_tissue_mask_slab0.nii')
#             FU_fontsize=50
#             FU_indent=70
#             FU_flag=1
#         elif os.path.exists(input_folder + cid + '/' + cid +'_' +'FU2BL_coregistration_rcbv_slice_slab0.nii'):
#             FU_rcbv_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2BL_coregistration_rcbv_slice_slab0.nii')  
#             FU_tmaxgray_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2BL_coregistration_tmax_slice_slab0.nii') 
#             FU_tmax_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2BL_coregistration_tmax_mask_slab0.nii')     
#             FU_tmax6_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2BL_coregistration_tmax6_mask_slab0.nii')
#             FU_core_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2BL_coregistration_core_mask_slab0.nii')
#             FU_rcbv_mask_outside_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2BL_coregistration_rcbv_mask_outside_slab0.nii')
#             FU_tissue_mask_image=sitk.ReadImage(input_folder + cid + '/' + cid +'_' +'FU2BL_coregistration_tissue_mask_slab0.nii')             
#             FU_fontsize=13
#             FU_indent=40
#             FU_flag=0
#         FU_rcbv_arr=sitk.GetArrayFromImage(FU_rcbv_image)
#         FU_rcbv_arr=rewrite_dim(FU_rcbv_arr)
#         FU_tmax_arr=sitk.GetArrayFromImage(FU_tmax_image)
#         FU_tmax_arr=rewrite_dim(FU_tmax_arr)
#         FU_tmax6_arr=sitk.GetArrayFromImage(FU_tmax6_image)
#         FU_tmax6_arr=rewrite_dim(FU_tmax6_arr) 
#         FU_core_arr=sitk.GetArrayFromImage(FU_core_image)
#         FU_core_arr=rewrite_dim(FU_core_arr) 
#         FU_rcbv_mask_outside_arr=sitk.GetArrayFromImage(FU_rcbv_mask_outside_image)
#         FU_rcbv_mask_outside_arr=rewrite_dim(FU_rcbv_mask_outside_arr) 
#         FU_tissue_arr=sitk.GetArrayFromImage(FU_tissue_mask_image)
#         FU_tissue_arr=rewrite_dim(FU_tissue_arr) 
#         
#         if FU_flag==2:
#             print('FU2slabs')
#             FU_tissue0_arr=sitk.GetArrayFromImage(FU_tissue_mask0_image)
#             FU_tissue0_arr=rewrite_dim(FU_tissue0_arr) 
#             FU_tissue1_arr=sitk.GetArrayFromImage(FU_tissue_mask1_image)
#             FU_tissue1_arr=rewrite_dim(FU_tissue1_arr) 
#             
#             FU_rcbv0_arr=sitk.GetArrayFromImage(FU_rcbv0_image)
#             FU_rcbv0_arr=rewrite_dim(FU_rcbv0_arr) 
#             FU_rcbv1_arr=sitk.GetArrayFromImage(FU_rcbv1_image)
#             FU_rcbv1_arr=rewrite_dim(FU_rcbv1_arr) 
#             
#             mean_outside_slab0=np.mean(FU_rcbv0_arr[np.logical_and(BL_rcbv_mask_outside_arr>0,FU_tissue0_arr>0)])
#             FU_rcbv0_arr=FU_rcbv0_arr/mean_outside_slab0
#             mean_outside_slab1=np.mean(FU_rcbv1_arr[np.logical_and(BL_rcbv_mask_outside_arr>0,FU_tissue1_arr>0)])
#             FU_rcbv1_arr=FU_rcbv1_arr/mean_outside_slab1
#             FU_rcbv_arr_norm=FU_rcbv1_arr
#             FU_rcbv_arr_norm[FU_tissue0_arr>0]=FU_rcbv0_arr[FU_tissue0_arr>0]
#             FU_CBVindex=np.mean(FU_rcbv_arr_norm[np.logical_and(BL_tmax6_arr>0,FU_tissue_arr>0)])
#             
#             FU_CBVindex0=np.mean(FU_rcbv0_arr[np.logical_and(BL_tmax6_arr>0,FU_tissue0_arr>0)])
#             FU_CBVindex1=np.mean(FU_rcbv1_arr[np.logical_and(BL_tmax6_arr>0,FU_tissue1_arr>0)])
#             FU_CBVindex0= round(FU_CBVindex0, 2)
#             FU_CBVindex1= round(FU_CBVindex1, 2)
#
#         elif FU_flag==1 or FU_flag==0:
#             print('FU1slab')
#             FU_rcbv_arr_norm=FU_rcbv_arr/np.mean(FU_rcbv_arr[np.logical_and(BL_rcbv_mask_outside_arr>0,FU_tissue_arr>0)])
#             FU_CBVindex=np.mean(FU_rcbv_arr_norm[np.logical_and(BL_tmax6_arr>0,FU_tissue_arr>0)])
#             FU_CBVindex0=""
#             FU_CBVindex1=""
#         try:
#             FU_CBVindex= round(FU_CBVindex, 2)
#         except:
#             FU_CBVindex= str(FU_CBVindex)
#             
#         FU_HPindex_basedon_BLtmax6=np.sum(np.logical_and(FU_tmax_arr==4,BL_tmax6_arr>0).astype(float))/np.sum((BL_tmax6_arr>0).astype(float))
#         
#         try:
#             FU_HPindex_basedon_BLtmax6= round(FU_HPindex_basedon_BLtmax6, 2)
#         except:
#             FU_HPindex_basedon_BLtmax6= str(FU_HPindex_basedon_BLtmax6)
#         
#         FU_tmax6_mask=np.transpose((FU_tmax6_arr>0).astype(int),(1,2,0))   
#         FU_tmax6_edges=imageutils.get_edges(FU_tmax6_mask)
#         FU_tmax6_mymontage=imageutils.montage(FU_tmax6_edges)
#         FU_tmax6_rescale_edges=imageutils.imrescale(FU_tmax6_mymontage,[np.min(FU_tmax6_mymontage),np.max(FU_tmax6_mymontage)],[0,1])
#         imageutils.imsave(input_folder + cid + '/' + cid +'_' +'FU_tmax6_edges.png' ,FU_tmax6_rescale_edges)
#             
#         FU_HPindex=np.sum((FU_tmax_arr==4).astype(float))/np.sum((FU_tmax6_arr>0).astype(float))  
#         FU_spacing=FU_rcbv_image.GetSpacing()
#         FU_Tmax6_vol=(np.sum((FU_tmax6_arr>0).astype(float))*FU_spacing[0]*FU_spacing[1]*FU_spacing[2])/1000
#         FU_Tmax10_vol=(np.sum((FU_tmax_arr==4).astype(float))*FU_spacing[0]*FU_spacing[1]*FU_spacing[2])/1000
#         FU_core_vol=(np.sum((FU_core_arr>0).astype(float))*FU_spacing[0]*FU_spacing[1]*FU_spacing[2])/1000
#         
#
#         FU_Tmax6_vol=round(FU_Tmax6_vol,2)
#         FU_Tmax10_vol=round(FU_Tmax10_vol,2)
#         FU_core_vol=round(FU_core_vol,2)
#    
#         print("FU_Tmax6_vol is " + str(FU_Tmax6_vol))
#         print("FU_Tmax10_vol is " + str(FU_Tmax10_vol))
#         print("FU_core_vol is " + str(FU_core_vol))
#         
#         try:
#             FU_HPindex= round(FU_HPindex, 2)
#         except:
#             FU_HPindex= str(FU_HPindex)
#             
#         print('FU_HPindex is '+str(FU_HPindex))
#         print('FU_CBVindex is '+str(FU_CBVindex))
#         
#
#         FU_rcbv_arr_norm=np.transpose(FU_rcbv_arr_norm,(1,2,0))   
#         FU_rcbv_mymontage=imageutils.montage(FU_rcbv_arr_norm)
#         FU_rescale_rcbv_arr=imageutils.imrescale(FU_rcbv_mymontage,[0,3],[0,1])
#         FU_rcbv_rgbmont=np.stack( (FU_rescale_rcbv_arr,FU_rescale_rcbv_arr,FU_rescale_rcbv_arr),2)        
#        
##         green=np.stack((FU_tmax6_mymontage*0,FU_tmax6_mymontage==1,FU_tmax6_mymontage*0 ),2) 
#         
#         FU_tissue=np.transpose((FU_tissue_arr>0).astype(int),(1,2,0)) 
#         FU_tissue_mymontage=imageutils.montage(FU_tissue)
#         
#         BL_tmax6_mymontage=np.logical_and(BL_tmax6_mymontage>0,FU_tissue_mymontage>0)
#         BL_tmax6_mymontage=BL_tmax6_mymontage.astype(int)
#         yellow=np.stack((BL_tmax6_mymontage==1,BL_tmax6_mymontage==1,BL_tmax6_mymontage*0 ),2)  
##         compositemask=yellow+green
##         compositemask[compositemask==2]=1
#         final_img=imageutils.rgbmaskonrgb(FU_rcbv_rgbmont,yellow.astype(np.float))
#         imageutils.imsave(input_folder + cid + '/' + cid +'_' +'FU_tmax6_edges_on_rcbv.png',final_img)   
#        
#
#         input_folder2='/Users/amar/D3_R47_RANDOMIZED_FINAL/'
#         
#         if os.path.isdir(input_folder2 +'/'+str(cid)+'/'+'FU/Results_PWI_DWI_R47/'):
#            op_FU=rapid47.RAPID46OP(input_folder2 +'/'+str(cid)+'/'+'FU/Results_PWI_DWI_R47/')
#            
#            FU_slicethickness=float(op_FU.slicethickness_slab1)
#            diff_slicethickness=FU_slicethickness-FU_spacing[2]
#            print(str(cid)+"  FU diff slicethickness" + str(diff_slicethickness))
#            file = open("/Users/amar/registered_maps2/FU_diff slicethickness.txt","a") 
#            file.write(str(cid)+"  FU diff slicethickness" + str(diff_slicethickness)+"\n")
#            
#            
##            FU_log_location=glob.glob(input_folder2 +'/'+str(cid)+'/'+'FU/Results_PWI_DWI_R47/'+'*processing.log.txt')
##            logtxt=logread(FU_log_location[0])
##            opt=re.search("Reconstructed slice thickness: (.*) mm",logtxt)
##            if not opt==None:
##                slicethickness=float(opt.group(1))
##                diff_slicethickness=slicethickness-FU_spacing[2]
##                print("FU diff slicethickness" + str(diff_slicethickness))
#         elif os.path.isdir(input_folder2 +'/'+str(cid)+'/'+'FU/Results_CTP_R47/'):
#            op_FU=rapid47.RAPID46OP(input_folder2 +'/'+str(cid)+'/'+'FU/Results_CTP_R47/')
#         elif os.path.isdir(input_folder2 +'/'+str(cid)+'/'+'FU/Results_CTP_2SLABS_R47/'):
#            op_FU=rapid47.RAPID46OP(input_folder2 +'/'+str(cid)+'/'+'FU/Results_CTP_2SLABS_R47/')
#            
#         if FU_flag==0:  
#             try:
#                 FU_HPindex_orig=op_FU.HypoperfusionIndex_slab1[0]
#                 FU_CBVindex_orig=op_FU.CBVIndex_slab1[0]   
#             except:
#                 FU_HPindex_orig=op_FU.HypoperfusionIndex_slab1
#                 FU_CBVindex_orig=op_FU.CBVIndex_slab1
#                 
#             FU_HPindex0_orig=""
#             FU_HPindex1_orig=""
#             FU_CBVindex0_orig=""
#             FU_CBVindex1_orig=""
#             try:
#                 FU_CBVindex_orig=round(FU_CBVindex_orig, 2)
#                 print("original FU_CBVindex is " + FU_CBVindex_orig)                 
#             except:
#                 print("original FU_CBVindex is " + str(FU_CBVindex_orig))
#             try:
#                 FU_HPindex_orig=round(FU_HPindex_orig, 2)
#                 print("original FU_HPindex is " + FU_HPindex_orig)
#             except:
#                 print("original FU_HPindex is " + str(FU_HPindex_orig))
#                 
#                 
#         if FU_flag==1:  
#
#             try:
#                 FU_HPindex_orig=op_FU.HypoperfusionIndex_slab1[0]
#                 FU_CBVindex_orig=op_FU.CBVIndex_slab1[0]   
#             except:
#                 FU_HPindex_orig=op_FU.HypoperfusionIndex_slab1
#                 FU_CBVindex_orig=op_FU.CBVIndex_slab1                 
#             FU_HPindex0_orig=""
#             FU_HPindex1_orig=""
#             FU_CBVindex0_orig=""
#             FU_CBVindex1_orig=""
#             
#             try:
#                 FU_CBVindex_orig=round(FU_CBVindex_orig, 2)
#                 print("original FU_CBVindex is " + FU_CBVindex_orig)                 
#             except:
#                 print("original FU_CBVindex is " + str(FU_CBVindex_orig))
#             try:
#                 FU_HPindex_orig=round(FU_HPindex_orig, 2)
#                 print("original FU_HPindex is " + FU_HPindex_orig)
#             except:
#                 print("original FU_HPindex is " + str(FU_HPindex_orig))
#                 
#             
#         elif FU_flag==2:
#             FU_HPindex_orig=""
#             FU_CBVindex_orig=""        
#             FU_HPindex0_orig=op_FU.HypoperfusionIndex_slab1
#             FU_HPindex1_orig=op_FU.HypoperfusionIndex_slab2
#             FU_CBVindex0_orig=op_FU.CBVIndex_slab1
#             FU_CBVindex1_orig=op_FU.CBVIndex_slab2 
#             
#             try:
#                 FU_CBVindex0_orig=round(FU_CBVindex0_orig, 2)
#                 print("original FU_CBVindex slab0 is " + FU_CBVindex0_orig)
#             except:
#                 print("original FU_CBVindex slab0 is " + str(FU_CBVindex0_orig))
#             try:
#                 FU_HPindex0_orig=round(FU_HPindex0_orig, 2)
#                 print("original FU_HPindex slab0 is " + FU_HPindex0_orig)
#             except:
#                 print("original FU_HPindex slab0 is " + str(FU_HPindex0_orig))
#                 
#             try:
#                 FU_CBVindex1_orig=round(FU_CBVindex1_orig, 2)
#                 print("original FU_CBVindex slab1 is " + FU_CBVindex1_orig)
#             except:
#                 print("original FU_CBVindex slab1 is " + str(FU_CBVindex1_orig))
#             try:
#                 FU_HPindex1_orig=round(FU_HPindex1_orig, 2)
#                 print("original FU_HPindex slab1 is " + FU_HPindex1_orig)
#             except:
#                 print("original FU_HPindex slab1 is " + str(FU_HPindex1_orig))
#             
#         temp=txt2vol([20,20],"CBV index: "+str(FU_CBVindex)+"   Slab0 CBV index: "+str(FU_CBVindex0)+"   Slab1 CBV index: "+str(FU_CBVindex1),final_img,FU_fontsize)
##         temp=txt2vol([20,50],"CBV index orig: "+str(FU_CBVindex_orig)+"   Slab0 CBV index orig : "+str(FU_CBVindex0_orig)+"   Slab1 CBV index orig: "+str(FU_CBVindex1_orig),temp,FU_fontsize)
#         imageutils.imsave(input_folder + cid + '/' + cid +'_' +'FU_CBVindex.png',temp)     
#         
#         FU_tmaxoverlayed_png=create_tmax_PNGs(FU_tmaxgray_image,FU_tmax_image)
#         temp1=txt2vol([20,20],"Tmax6 vol(green): "+str(FU_Tmax6_vol)+"   Tmax10 vol(red): "+str(FU_Tmax10_vol)+"   Core vol: "+str(FU_core_vol)+"   HP index: "+str(FU_HPindex),FU_tmaxoverlayed_png,FU_fontsize)
#         imageutils.imsave(input_folder + cid + '/' + cid +'_' +'FU_HPindex.png',temp1) 
#         
#                  
#         reperfusionpercent=round(((BL_Tmax6_vol-FU_Tmax6_vol)/BL_Tmax6_vol)*100,2)   
#         print("reperfusionpercent is" + str(reperfusionpercent))
         
         cid_list.append(cid)
         BL_core_vol_list.append(BL_core_vol)
         BL_Tmax6_vol_list.append(BL_Tmax6_vol)
         BL_Tmax10_vol_list.append(BL_Tmax10_vol)
         BL_CBVindex_list.append(BL_CBVindex)
         BL_HPindex_list.append(BL_HPindex)
#         FU_core_vol_list.append(FU_core_vol)
#         FU_Tmax6_vol_list.append(FU_Tmax6_vol)
#         FU_Tmax10_vol_list.append(FU_Tmax10_vol)
#         FU_CBVindex_basedon_BLtmax6_list.append(FU_CBVindex)
#         FU_HPindex_list.append(FU_HPindex)
#         reperfusionpercent_list.append(reperfusionpercent)
#         FU_HPindex_basedon_BLtmax6_list.append(FU_HPindex_basedon_BLtmax6)
         
    
names_list=["cid","BL_core_vol","BL_Tmax6_vol","BL_Tmax10_vol","BL_CBVindex","BL_HPindex","FU_core_vol","FU_Tmax6_vol","FU_Tmax10_vol","FU_CBVindex_basedon_BLtmax6","FU_HPindex","FU_HPindex_basedon_BLtmax6","reperfusionpercent"]
workbook = xlsxwriter.Workbook("/Users/amar/registered_maps2/"+'D3_registered_volumes_missingcases.xlsx')
worksheet = workbook.add_worksheet()

# Start from the first cell. Rows and columns are zero indexed.
col = 0

# Iterate over the data and write it out row by row.
for col in range(len(names_list)):    
    worksheet.write(0, col, names_list[col]) 
    col += 1
    
for row in range(len(cid_list)):
    worksheet.write(row+1, 0,cid_list[row])
    worksheet.write(row+1, 1,BL_core_vol_list[row])
    worksheet.write(row+1, 2,BL_Tmax6_vol_list[row])
    worksheet.write(row+1, 3,BL_Tmax10_vol_list[row])
    worksheet.write(row+1, 4,BL_CBVindex_list[row])
    worksheet.write(row+1, 5,BL_HPindex_list[row])
#    worksheet.write(row+1, 6,FU_core_vol_list[row])
#    worksheet.write(row+1, 7,FU_Tmax6_vol_list[row])
#    worksheet.write(row+1, 8,FU_Tmax10_vol_list[row])
#    worksheet.write(row+1, 9,FU_CBVindex_basedon_BLtmax6_list[row])
#    worksheet.write(row+1, 10,str(FU_HPindex_list[row]))
#    worksheet.write(row+1, 11,FU_HPindex_basedon_BLtmax6_list[row]) 
#    worksheet.write(row+1, 12,reperfusionpercent_list[row]) 

    row += 1


workbook.close()












             