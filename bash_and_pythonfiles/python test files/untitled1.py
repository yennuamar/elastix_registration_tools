#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 19:02:13 2017

@author: amar
"""

import pydicom
import pylab
import numpy
import scipy
import matplotlib


#ds=pydicom.read_file("/Users/amar/182ctp/182/16318007707/VPCT_Perfusion_100_H20f_105353/IM-0001-0001.dcm")
#print(ds)
#pylab.imshow(ds.pixel_array, cmap=pylab.cm.bone)
#pylab.show()
#a=ds.pixel_array
#pylab.gray()

#print(ds.pixel_array)

import glob   
path = '/Users/amar/182ctp/182/16318007707/VPCT_Perfusion_100_H20f_105353/*.dcm'   
files=glob.glob(path)   
for file in files:     
    f=open(file, 'r')  
    f.readlines()   
    f.close() 
    
for i in range(len(files)):
    ds=pydicom.read_file(files[i])
    print(ds.pixel_array)
    pylab.imshow(ds.pixel_array, cmap=pylab.cm.bone)
    pylab.gray()