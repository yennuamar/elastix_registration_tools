#import threading

import cy
#import numpy as np
#import matplotlib.pyplot as plt
#plt.show()


def readmhd(fglob): 
    t=cy.pyShort()  #create loader instance
    t.readFiles(fglob)
        #set prefix and load
    return t  #grab the data 

#  mystr="/home/sorenc/CODE/rapid_4_6/source/backend/build-perf_mismatch-Desktop_Qt_5_5_1_GCC_64bit-Default/post_volume_slab0_band0_timepoint*mhd"

#now get the correlations
#==============================================================================
# mycorr=np.zeros((mymat.shape[3]),dtype=np.float32)
# img1=mymat[:,:,:,2]
# for k in range(mymat.shape[3]):
#     img2=mymat[:,:,:,k]
#     print np.corrcoef(img1.flatten(),img2.flatten() )
#     mycorr[k]= np.corrcoef(img1.flatten(),img2.flatten())[1][0]
# 
# plt.figure
# plt.plot(mycorr)
#==============================================================================


#
#import ctypes
#from ctypes import util
#ctypes.CDLL(util.find_library('GL'), ctypes.RTLD_GLOBAL)
#ctypes.CDLL(util.find_library('glib-2'), ctypes.RTLD_GLOBAL)
#ctypes.CDLL(util.find_library('gobject-2'), ctypes.RTLD_GLOBAL)
#ctypes.CDLL(util.find_library('libXext'), ctypes.RTLD_GLOBAL)
#a=cy.pyA()
#a.pyGUI()
#t# = threading.Thread( target=a.pyGUI ) 
#t.daemon=False
#t.start()
