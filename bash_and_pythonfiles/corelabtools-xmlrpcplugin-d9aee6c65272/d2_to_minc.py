#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 12:29:17 2017

@author: sorenc
"""

import  xmlrpclib
import openpyxl
import re

from osirixutils import *

#server = xmlrpclib.Server("http://localhost:8080",verbose=False)
server = xmlrpclib.Server("http://10.0.0.39:8080",verbose=False)


IDs=server.getPatientIDs( )
sortedIDs=sorted(IDs)
#sortedIDs=["11001_G_M"]


#lets get all possible TOF and list by datetime comment
for cid in sortedIDs:   #sortedIDs[0:10]:
    studies=server.PatientIDtoStudies(  {"patientID": cid})  
        
    dates=[k["date"] for k in studies]
    #sort by study date
    sorted_studies=[x for (y,x) in   sorted(zip(dates,studies))]
    #iterate studies and look for TOFs in the study, list those found with names
    
    for istudy in sorted_studies:
        print "studyun date" + istudy["date"]
        comment2="UN"
        if istudy.has_key("comment2") and not istudy["comment2"]=="":
            comment2=istudy["comment2"]
            
        seriesdicts=getImageSeriesUIDsForStudies(server,[istudy])    
        for iseries in seriesdicts:
            #print iseries["name"]
        
            if iseries.has_key("comment3") and not iseries["comment3"]=="": 
                modallabel=iseries["comment3"]
                targetfolder="DWINCCT/"+cid[0:5] + "/" + comment2 +"/"+modallabel + "/"+ iseries["seriesDICOMUID"]
                get_dicom_for_series_rhost(server,"sorenc@10.0.0.39",iseries["seriesInstanceUID"],targetfolder)
                print "got DICOMs for " + comment2
                tagdict={"StudyComments":"","PatientID":cid[0:5],"PatientName":cid[0:5],"InstitutionName":"","ReferringPhysicianName":"","StationName":"",
                                "NameOfPhysiciansReadingStudy":"","OperatorsName":"","IssuerOfPatientID":"","PatientBirthDate":"","PatientAddress":"","PatientAge":"",
                                "AccessionNumber":"","PatientWeight":"","AdditionalPatientHistory":"",
                                "PhysiciansOfRecord":"","PerformingPhysicianName":"","OtherPatientIDs":""}
          
                modify_tags(targetfolder, tagdict,True)
