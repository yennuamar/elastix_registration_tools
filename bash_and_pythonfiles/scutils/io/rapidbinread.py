#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 14:28:02 2016

@author: sorenc
"""
import array
import numpy as np
 
def rapidbinread(fname):    
    f = open(fname, 'r',0)
    a1 = array.array('H')
    a1.fromfile(f,6)
    #a1.fromfile(f,(a1[0]-1))
    
    #dtype=a1[0]
    ndims=a1[1]
    dimlist=list(a1[2:(2+ndims)])

    #now let us read it
    myarr=np.fromfile(f,dtype=np.float32)
    f.close()
    dimlist.reverse()
    return np.transpose(np.ndarray(dimlist,np.float32,myarr),(2,1,0,3))

#==============================================================================
# plt.imshow(mymat[1,:,:,1],clim=(0, 150),interpolation='nearest')
# plt.set_cmap(cm.gray)
# plt.show()
# 
# 
# #now calculate the correlation to frame 2
# 
# mycorr=np.zeros((1,mymat.shape[3]),dtype=np.float32)
# img1=mymat[1,:,:,2]
# for k in range(mymat.shape[3]):
#     img2=mymat[1,:,:,k]
#     
#     
#     
#     print np.corrcoef(img1.flatten(),img2.flatten() )
# 
# 
# 
# #do the same for the new RAPID - lets build this using cython/c++ for full flexibility
# #wishlist
# 
# import myio
# my4Dmat=myio.itk2np("/home/sorenc/CODE/rapid_4_6/source/backend/build-perf_mismatch-Desktop_Qt_5_5_1_GCC_64bit-Default/post_volume_slab0_band0_timepoint*mhd")
# #and from there on we can repeat the above...
#==============================================================================












