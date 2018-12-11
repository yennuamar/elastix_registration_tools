# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 14:13:55 2016

@author: sorenc
"""

import numpy as np

def framecorr(mymat,compframe):
    mycorr=np.zeros((mymat.shape[3]),dtype=np.float32)
    img1=mymat[:,:,:,compframe]
    for k in range(mymat.shape[3]):
        img2=mymat[:,:,:,k]
        #print "calculating corrcoeff frame " + str(k)
        #print np.corrcoef(img1.flatten(),img2.flatten() )
        mycorr[k]= np.corrcoef(img1.flatten(),img2.flatten())[1][0]
    
    return mycorr
    
    #plt.figure
    #plt.plot(mycorr)
    
    
