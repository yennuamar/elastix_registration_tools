#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 21:35:47 2017

@author: sorenc
"""

import pydicom
import os
import collin_sheet
#create a deidentified DWI/NCCT data set. 
sourcefolder='/home/sorenc/DWINCCTALL'
targetfolder='/home/sorenc/DWINCCT_DEIDENT_SORTED_COLLIN'
#read all files in this folder and sort into the targetfolder. Then deidentify in-place

tagdictCT={"StudyComments":"","PatientID":"","PatientName":"","InstitutionName":"","ReferringPhysicianName":"","StationName":"",
                                "NameOfPhysiciansReadingStudy":"","OperatorsName":"","IssuerOfPatientID":"","PatientBirthDate":"","PatientAddress":"","PatientAge":"",
                                "AccessionNumber":"","PatientWeight":"","AdditionalPatientHistory":"","ProtocolName":"","StudyDescription":"NCCT RATING",
                                "PhysiciansOfRecord":"","PerformingPhysicianName":"","OtherPatientIDs":"","DeviceSerialNumber":""}
    
tagdictMR={"StudyComments":"","PatientID":"","PatientName":"","InstitutionName":"","ReferringPhysicianName":"","StationName":"",
                                "NameOfPhysiciansReadingStudy":"","OperatorsName":"","IssuerOfPatientID":"","PatientBirthDate":"","PatientAddress":"","PatientAge":"",
                                "AccessionNumber":"","PatientWeight":"","AdditionalPatientHistory":"","ProtocolName":"","StudyDescription":"",
                                "PhysiciansOfRecord":"","PerformingPhysicianName":"","OtherPatientIDs":"","DeviceSerialNumber":""}
     
sheet=collin_sheet.getSheet()
sheetIDs=sheet[0]["studyNumber"]
sheetLat=sheet[0]["Laterality"]


erase_private=True
matches = []
for root, dirnames, filenames in os.walk(sourcefolder):
    for f  in filenames:
        matches.append( root +"/"+ f )
    #matches.append(os.path.join(root, filename))
        
        
for ff in matches:
    ds = pydicom.read_file(ff) 
    
    
    
    ID=ds.PatientID[0:5]
    
    laterality=sheetLat[ sheetIDs.index(ID) ]
    
    modality=ds.Modality
    
    localtargetfolder=targetfolder+'/' + ID+ '/' + modality
    
    if not os.path.exists(localtargetfolder):
        os.makedirs(localtargetfolder)
    #extract ID and DWI or NCCT (MR or CT)
    localtargetfilename=localtargetfolder+'/'+os.path.basename(ff)
    
    if modality=="MR":
        tagdict=tagdictMR  
    elif modality=="CT": #for Collin
        tagdict=tagdictCT 
        tagdict["SeriesDescription"]="NCCT"
        tagdict["ProtocolName"]="NCCT"
        tagdict["StudyDate"]=tagdict["SeriesDate"]=tagdict["ContentDate"]=tagdict["AcquisitionDate"]="20000101"
        tagdict["StudyTime"]=tagdict["SeriesTime"]=tagdict["ContentTime"]=tagdict["AcquisitionTime"]="120000"
        
    
    tagdict["PatientID"]=tagdict["PatientName"]=ID+"_"+laterality
    
    #print dirpath+"/"+ff
    for itag in tagdict.keys():
      #  de=ds.data_element(itag)
        if itag in ds:
            ds.data_element(itag).value=tagdict[itag]
            #print "setting " + itag
        else:
            #print "adding " + itag
            tag=pydicom.datadict.tag_for_name(itag)
            VR=pydicom.datadict.dictionaryVR(tag)
            ds.add_new(tag,VR,tagdict[itag])
       
        
    if "ReferencedStudySequence" in ds:
        del ds[ds.data_element("ReferencedStudySequence").tag]
        
    if erase_private:
        for k in ds:
            if k.tag.is_private:
                #print "deleting " + str(k.tag)
                del ds[k.tag]   
    
    try:
        print "saving " + localtargetfilename
        ds.save_as(localtargetfilename)
    except:
        print "problem modifying " + localtargetfilename
        print "erasing file..."
        osexec("rm -f '" + localtargetfilename+ "'")