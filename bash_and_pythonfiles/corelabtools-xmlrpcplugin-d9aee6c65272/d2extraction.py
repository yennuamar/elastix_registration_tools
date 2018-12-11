#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 04:02:29 2017

@author: sorenc
"""

#d2extraction

#extract all TOF marked BLs






for cid in sortedIDs:   #sortedIDs[0:10]:
    studies=server.PatientIDtoStudies(  {"patientID": cid})  
    
    BLstudies=[k for k in studies  if ( k.has_key("comment2") and k["comment2"]=="BL") ]
     
    if len (BLstudies)==0:
        continue
    #late take the studies 1-by-1
    seriesdicts=getImageSeriesUIDsForStudies(server,BLstudies)
    ncct_present=False
    dwi_present=False
    ncct_time=''
    dwi_time=''
    for iseries in seriesdicts:
            #print iseries["name"]
            if iseries.has_key("comment3") and iseries["comment3"]=="NCCT":    
                ncct_present=True
                ncct_time=datetime.strptime(iseries["date"][0:19],'%Y-%m-%d %H:%M:%S')
                
                targetfolder=cid + "/BL/NCCT"   #hmm - what if multiple?
                
            if iseries.has_key("comment3") and iseries["comment3"]=="DWI":    
                dwi_present=True
                dwi_time=datetime.strptime(iseries["date"][0:19],'%Y-%m-%d %H:%M:%S')
    
    