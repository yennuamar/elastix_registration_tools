#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 12:02:36 2017

@author: sorenc
"""
import  xmlrpclib
import openpyxl
import re
import D2worksheet
from datetime import datetime, timedelta 
import os
import time
   # server = Server("http://171.65.168.30:8080",verbose=True)
#server = Server("http://172.25.169.28:8085",verbose=False)

server = xmlrpclib.Server("http://localhost:8080",verbose=False)
#server = xmlrpclib.Server("http://172.25.169.28:8085",verbose=False)
#server = xmlrpclib.Server("http://192.168.0.10:8080",verbose=False)



from osirixutils import *



#d2 curation for DWI/NCCT


#which cases is in or our dataset

must_have=set(sorted(open('ncct_dwi.lst').read().split("\n")))

H_IDs=sorted(server.getPatientIDs( ))

#now find all IDs with BL DWI and NCCT
H_IDs_5dig=set([k[0:5] for k in H_IDs])

must_have-H_IDs_5dig

#missing rel to Collin:
#{'01038', '01040', '01042', '01044', '08007', '09004', '09005'}

#2mm CTA protocol '09004', '09005'






for cid in H_IDs[147:148]:
    if not cid[0:5] in must_have:
        continue
    
    
    studies=server.PatientIDtoStudies(  {"patientID": cid})  
    #print cid
    BLstudies=[k for k in studies  if ( k.has_key("comment2") and k["comment2"]=="BL" ) ]
    if len (BLstudies)==0:
        continue
    #late take the studies 1-by-1
    seriesdicts=getImageSeriesUIDsForStudies(server,BLstudies)
    hasDWI=False
    hasNCCT=False
    DWIUID=''
    NCCTUID=''
    dwilist=[]
    ncctlist=[]
    for iseries in seriesdicts:
        if iseries.has_key("comment3"):
            if iseries["comment3"]=="NCCT":
                hasNCCT=True
                ncctlist.append(iseries['seriesInstanceUID'])
            if iseries["comment3"]=="DWI": 
                hasDWI=True
                dwilist.append(iseries['seriesInstanceUID'])
                
        #if iseries.has_key("comment3") and (iseries["comment3"]=="NCCT"):    
    
    if hasNCCT and hasNCCT:
        print cid[0:5] + " OK"
        for f in dwilist:
            server.copySeries2DB( {"seriesInstanceUID": f, "targetDB":'/Users/sorenc/Documents/DWINCCT'} ) 

        for f in ncctlist:
            server.copySeries2DB( {"seriesInstanceUID": f, "targetDB":'/Users/sorenc/Documents/DWINCCT'} ) 

        
        time.sleep(5)
    else:
        print cid[0:5] + " not OK"     




