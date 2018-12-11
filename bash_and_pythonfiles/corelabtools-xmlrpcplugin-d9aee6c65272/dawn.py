#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 05:46:07 2017

@author: sorenc
"""


import  xmlrpclib
import openpyxl
import re
import DAWNsheet
from datetime import datetime, timedelta 
from osirixutils import *
import time
#get ID from sheet and compare to DB
server = xmlrpclib.Server("http://localhost:8080",verbose=False)


IDs_sheet=set(DAWNsheet.getIDs())

IDs_DB=set(server.getPatientIDs( ))

#in DB not in sheet
IDs_DB-IDs_sheet
#in sheet, not in DB
IDs_sheet-IDs_DB



#lets label time points

bltimepoints=DAWNsheet.getCoreTimes()

for cid in [] :#IDs_DB:
    BLtime=bltimepoints[cid]
    
    FUtime=BLtime+timedelta(days=1)
    
    crule=PatientTimePointLabel(cid,'BL',[BLtime-timedelta(minutes=60),BLtime+timedelta(minutes=60)])

    crule.addrule('FU',[FUtime-timedelta(hours=8),FUtime+timedelta(hours=36)])
    
    matches=crule.labelstudies(server,dryrun=0)

    print matches



ncctrule=LabelPattern('NCCT','head|noncon|non con|soft|non|5mm axial|H41s|axial|brain','bone|cor|sag|mip|ax bn',slicesmin=5,slicesmax=2000,framesmin=-1,framesmax=2,modality='CT') #frames=-1 allows no isophasic
tofrule=LabelPattern('TOF','tof|mra|pjn|mip|cow|spin|tumble|reformat|right|left|posterior|processed images','bone',slicesmin=1,slicesmax=2000,framesmin=-1,framesmax=100,modality='MR')
clearrule=LabelPattern('','.*','NOMATCH')
dwirule=LabelPattern('DWI','dwi|diff','exponen|adc|apparent|RAPID')
ruleset=[tofrule,ncctrule,dwirule]

IDwBLNCCT=set()
BLforCase=set()
for cid in IDs_DB:
    studies=server.PatientIDtoStudies(  {"patientID": cid})  
    print cid
    
    for istudy in studies:
        studylabel="UN"
        if istudy.has_key("comment2") and istudy["comment2"]=="BL":
            BLforCase.add(cid)
            studylabel="BL"
            
        seriesdicts=getImageSeriesUIDsForStudies(server,[istudy])
    
        for iseries in seriesdicts:
            if iseries.has_key("comment3") and iseries["modality"]=="CT" and not iseries["comment3"]=="NCCT":
                IDwBLNCCT.add(cid)
                
                
            if iseries.has_key("name") and (re.search('RAPID|tmax|mtt|cbf|cbv|aif-plot|vof-plot|Lesion Sizes|vof plot|vof point|aif points',iseries["name"],re.IGNORECASE)):
                pass
                #print "deleting " + iseries["name"] 
#               #server.deleteSeries( {"seriesInstanceUID": iseries} ) 
          
#                     # t=server.SetComment2forSeries({"seriesInstanceUID": iseries , "Comment2":"ADC" } )
    #labelcomment3forseries(seriesdicts,server,ruleset,dryrun=0)  


#now count BL CT    
#for cid in IDs_DB:
#    studies=server.PatientIDtoStudies(  {"patientID": cid}) 
#    for istudy in studies:
                  
    
    
    
    
    