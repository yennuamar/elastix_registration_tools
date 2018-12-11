#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 12:29:17 2017

@author: sorenc
"""

import  xmlrpclib
import openpyxl
import re
import D2worksheet

from osirixutils import *

server = xmlrpclib.Server("http://localhost:8080",verbose=False)


IDs=server.getPatientIDs( )
sheet=D2worksheet.getSheet()

#treatmentIDs=[cid for (cid,cohort) in zip(sheet["studyNumber"], sheet["cohortType"]) if cohort==1]


sortedIDs=sorted(IDs)
sortedIDs=[sortedIDs[44] ,sortedIDs[47]]


#lets get all possible TOF and list by datetime comment



print "ID,BL,earlyFU,lateFU"
for cid in sortedIDs:   #sortedIDs[0:10]:
    studies=server.PatientIDtoStudies(  {"patientID": cid})  
    
    print cid[0:5] #+ "," +hasbl + "," +hasefu+","+haslfu

    
    
    dates=[k["date"] for k in studies]
    #sort by study date
    sorted_studies=[x for (y,x) in   sorted(zip(dates,studies))]
    #iterate studies and look for TOFs in the study, list those found with names
    
    for istudy in sorted_studies:
        
        comment2="UN"
        if istudy.has_key("comment2") and not istudy["comment2"]=="":
            comment2=istudy["comment2"]
            
        
        has_header_yet=False
        seriesdicts=getImageSeriesUIDsForStudies(server,[istudy])    
        for iseries in seriesdicts:
            #print iseries["name"]
            if iseries.has_key("comment3") and re.search("CTP|PWI|FLAIR|DWI",iseries["comment3"],re.IGNORECASE): 
                if not has_header_yet:
                    print "\t " + comment2 + " study date " + istudy["date"]    
                    has_header_yet=True
                    
                if comment2=="eFU":
                    #efucount=efucount+1
                    #efutofcases.add(cid[0:5])
                    
                    LABEL="eFU"
                    tagdict={"StudyDescription":"early follow up"}
#                
                if comment2=="lFU":
                    #lfucount=lfucount+1
                    #lfutofcases.add(cid[0:5])
                    LABEL="lFU"
                    tagdict={"StudyDescription":"late follow up"}
                  
               
                if comment2=="UN":
                    LABEL="UN"
                    tagdict={"StudyDescription":"unscheduled study"}
                    
                if comment2=="BL":
                    #blcount=blcount+1
                    #bltofcases.add(cid[0:5])
                    
                    LABEL="BL"
                    tagdict={"StudyDescription":"baseline"}
                    
                assert(comment2)   #it must have a value by now
                #now retrieve the DICOMS and rewrite as requested
                
                commentfield=LABEL+"_"+iseries["comment3"]
                
                targetfolder="/Volumes/G-DRIVE slim SSD USB-C/AA/"+ cid[0:5] + "/" + LABEL +"/"+iseries["comment3"] + "_"+iseries["seriesDICOMUID"]
                get_dicom_for_series(server,iseries["seriesInstanceUID"],targetfolder)
                #print "got DICOMs for " + comment2
                tagdict={"StudyComments":commentfield,"PatientID":cid[0:5],"PatientName":cid[0:5],"InstitutionName":"","ReferringPhysicianName":"","StationName":"",
                         "NameOfPhysiciansReadingStudy":"","OperatorsName":"","IssuerOfPatientID":"","PatientBirthDate":"","PatientAddress":"","PatientAge":"",
                         "AccessionNumber":"","PatientWeight":"","AdditionalPatientHistory":"",
                         "PhysiciansOfRecord":"","PerformingPhysicianName":"","OtherPatientIDs":""}
          
                modify_tags(targetfolder, tagdict)
                
                print "\t\t" + iseries["name"] + ":   " + iseries["numberOfImages"] + " " + LABEL
      
               

#todo get 08 series imported
#todo - ask Michael if we have a column indicating if F/U TOF was done?
    
#find out who is supposed to have MRA (and if we have ID'd all those)





