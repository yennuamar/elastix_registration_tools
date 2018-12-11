#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 12:09:51 2017

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

   # server = Server("localhost:8080",verbose=False)
#server = xmlrpclib.Server("http://172.25.169.28:8085",verbose=False)
#server = xmlrpclib.Server("http://192.168.0.10:8080",verbose=False)

from osirixutils import *



ncctrule=LabelPattern('NCCT','head|noncon|non con|soft|non|5mm axial|H41s|axial|brain','bone|cor|sag|mip|ax bn',slicesmin=5,slicesmax=2000,framesmin=-1,framesmax=2,modality='CT') #frames=-1 allows no isophasic
tofrule=LabelPattern('TOF','tof|mra|pjn|mip|cow|spin|tumble|reformat|right|left|posterior|processed images','bone',slicesmin=1,slicesmax=2000,framesmin=-1,framesmax=100,modality='MR')
clearrule=LabelPattern('','.*','NOMATCH')

dwirule=LabelPattern('DWI','dwi|diff','exponen|adc|apparent|RAPID')



mrprule=LabelPattern('PWI','pwi|perf|','TTP',slicesmin=1,slicesmax=320,framesmin=30,framesmax=150,modality='MR')
flairrule=LabelPattern('FLAIR','flair|tirm','bone',slicesmin=1,slicesmax=2000,framesmin=-1,framesmax=100,modality='MR')
ctprule=LabelPattern('CTP','perf|shuttle|axial|40cc|above','bone',slicesmin=2,slicesmax=320,framesmin=10,framesmax=100,modality='CT')
ctarule=LabelPattern('CTA','thin|cow|cta|angio','perf|ctp|above',slicesmin=-1,slicesmax=2000,framesmin=-1,framesmax=100,modality='CT')


corclear=LabelPattern('','COR DIFFUSION','NOMATCH')

ruleset=[clearrule,dwirule,tofrule,ncctrule,ctarule,ctprule,flairrule,mrprule]
#ruleset=[ncctrule]
#ruleset=[clearrule]
#ruleset=[ncctrule]

#server = xmlrpclib.Server("http://192.168.10.112:8080",verbose=False)
#server = xmlrpclib.Server("http://192.168.0.15:8080",verbose=False)
server = xmlrpclib.Server("http://localhost:8080",verbose=False)
IDs=server.getPatientIDs( )
sortedIDs=sorted(IDs)
sortedIDs=sortedIDs[20:30]
#sortedIDs=["01002_W_S"]


for cid in sortedIDs: #sortedIDs:  #sortedIDs[0:1]:
    #iterate series and label each series
    print cid
    studies=server.PatientIDtoStudies(  {"patientID": cid})  
    
    #for s in studies:
    #    server.SetComment2forStudy({"studyInstanceUID": s["studyInstanceUID"] , "Comment":"" } )  
    
    
    seriesdicts=getImageSeriesUIDsForStudies(server,studies)
    
    
   # labelcomment2forstudy(seriesdicts,server,ruleset,dryrun=0)      #label the series if there is a match
    labelcomment3forseries(seriesdicts,server,ruleset,dryrun=0)      #label the series if there is a match
    
    time.sleep(2)
            



labelstudies_BL=D2worksheet.getBLtimes() 
labelstudies_eFU=D2worksheet.geteFUtimes() 
labelstudies_lFU=D2worksheet.getlFUtimes()   
 #setup PatientTimePointLabel

for cid in sortedIDs:   #sortedIDs[0:10]:
    trunkid=cid[0:5]

    if not labelstudies_BL.has_key(trunkid):  #some patients are not in the sheet all all
        print cid + " is not in the sheet"
        continue

    BLtime=labelstudies_BL[trunkid]
    eFUtime=labelstudies_eFU[trunkid]
    lFUtime=labelstudies_lFU[trunkid]

    if eFUtime and BLtime:
        earlyFUdelta=eFUtime-BLtime
        print trunkid + "," + str(earlyFUdelta.total_seconds()/(60*60))
    else: 
        print  trunkid + ",None" 
    
    BL_trange_min=BLtime - timedelta(hours=6)
    BL_trange_max=BLtime + timedelta(hours=2)  #we dont want to capture the eFU here
    crule=PatientTimePointLabel(cid,'BL',[BL_trange_min,BL_trange_max])


    if eFUtime:
        eFU_trange_min=eFUtime - timedelta(minutes=30)
        eFU_trange_max=eFUtime + timedelta(hours=2)  
        
        if BL_trange_max>eFU_trange_min:
            print "eFU may overide BL in " + trunkid
        
        crule.addrule('eFU',[eFU_trange_min,eFU_trange_max])
    
    if lFUtime:
        lFU_trange_min=lFUtime - timedelta(hours=24)
        lFU_trange_max=lFUtime + timedelta(hours=24)  
        
        if eFU_trange_max>lFU_trange_min:
            print "lFU may overide eFU in " + trunkid
            
        crule.addrule('lFU',[lFU_trange_min,lFU_trange_max])
        
    
    

    crule.labelstudies(server,dryrun=0)
    time.sleep(1)




count=0
 #BLstudies=getStudiesWithLabel(server,"BL")
for cid in sortedIDs:   #sortedIDs[0:10]:
    studies=server.PatientIDtoStudies(  {"patientID": cid})  
    
    BLstudies=[k for k in studies  if ( k.has_key("comment2") and k["comment2"]=="BL") ]
     
    hasBLDWI=False
    hasBLNCCT=False
    seriesdicts=getImageSeriesUIDsForStudies(server,BLstudies)
    for iseries in seriesdicts:
        if iseries.has_key("comment3") and  iseries["comment3"]=="DWI":
            hasBLDWI=True
            continue
        elif iseries.has_key("comment3") and iseries["comment3"]=="NCCT":
            hasBLNCCT=True
            continue

    if hasBLDWI and hasBLNCCT:
        print "NCCT AND DWI in " + cid
        count=count+1
        
print count


#==============================================================================
# 
#          
# labelstudies_BL=D2worksheet.getBLtimes() 
# labelstudies_eFU=D2worksheet.geteFUtimes() 
# labelstudies_lFU=D2worksheet.getlFUtimes()   
# #setup PatientTimePointLabel
# patientrules=[]
# 
# for cid in sortedIDs[0:0]:   #sortedIDs[0:10]:
#    trunkid=cid[0:5]
#    
#    
#    if not labelstudies_BL.has_key(trunkid):  #some patients are not in the sheet all all
#        print cid + " is not in the sheet"
#        continue
#    BLtime=labelstudies_BL[trunkid]
#    eFUtime=labelstudies_eFU[trunkid]
#    lFUtime=labelstudies_lFU[trunkid]
#    
#    if eFUtime and BLtime:
#        earlyFUdelta=eFUtime-BLtime
#        print trunkid + "," + str(earlyFUdelta.total_seconds()/(60*60))
#    else: 
#        print  trunkid + ",None" 
#        
#    #BL    
#    
#   # print "BLmatch " + trunkid
#    BL_trange_min=BLtime - timedelta(hours=6)
#    BL_trange_max=BLtime + timedelta(hours=2)  #we dont want to capture the eFU here
#    crule=PatientTimePointLabel(cid,'BL',[BL_trange_min,BL_trange_max])
#    
#    
#    #eFU   eFU can potentially override a BL, warn me if so
#   # print "eFUmatch " + trunkid
#    if eFUtime:
#        eFU_trange_min=eFUtime - timedelta(minutes=30)
#        eFU_trange_max=eFUtime + timedelta(hours=2)  
#        if BL_trange_max>eFU_trange_min:
#            print "eFU may overide BL in " + trunkid
#            
#        crule.addrule('eFU',[eFU_trange_min,eFU_trange_max])
#        
#        
#        
#    
#    
#    #lFU
#   #print "lFUmatch " + trunkid
#    if lFUtime:
#        lFU_trange_min=lFUtime - timedelta(hours=24)
#        lFU_trange_max=lFUtime + timedelta(hours=24)  
#        
#        if eFU_trange_max>lFU_trange_min:
#            print "lFU may overide eFU in " + trunkid
#            
#        crule.addrule('lFU',[lFU_trange_min,lFU_trange_max])
#        
#        
#        
#    
#    crule.labelstudies(server,dryrun=0)
#        
#    
#    
#    
#    
# #now locate all cases with DWI+NCCT at BL
# 
# count=0
# #BLstudies=getStudiesWithLabel(server,"BL")
# for cid in sortedIDs:   #sortedIDs[0:10]:
#     studies=server.PatientIDtoStudies(  {"patientID": cid})  
#     
#     BLstudies=[k for k in studies  if ( k.has_key("comment3") and k["comment3"]=="BL") ]
#     
#     hasBLDWI=False
#     hasBLNCCT=False
#     seriesdicts=getImageSeriesUIDsForStudies(server,BLstudies)
#     for iseries in seriesdicts:
#         if iseries.has_key("comment2") and  iseries["comment2"]=="DWI":
#             hasBLDWI=True
#             continue
#         elif iseries.has_key("comment2") and iseries["comment2"]=="NCCT":
#             hasBLNCCT=True
#             continue
# 
#     if hasBLDWI and hasBLNCCT:
#         print "NCCT AND DWI in " + cid
#         count=count+1
#         
# print count
# 
# 
#==============================================================================




#for each patient get all studies with the BL label:
#    then find all series with NCCT or DWI



#who has BL NCCT and BL DWI?
   
   #crule=PatientTimePointLabel(cid,'BL',[trange_min,trange_max])
   
   
   #



#for cid in IDs[0:2]:
    


#now label the time points    
    
    
    
    
  #  patientscaninfo_object = PatientScanInfo(ID,sheet)   
    
    #now get the study times+modals+imagelabellings for each study and match it with the patientinfo object
    
    
    
    
#    copy_series2otherDB(server,seriesregex,'RAPIDTMPDB DB)
    
#==============================================================================
#     
#     studies=server.PatientIDtoStudies(  {"patientID": cid})    
#     for istudy in studies:
#         series=server.StudyUIDtoSeries(  {"studyInstanceUID": istudy} )    
#         
#         for iseries in series:
#             if iseries=='OsiriX Annotations SR' or iseries=='LOCALIZER' or iseries=='OsiriX ROI SR' or iseries=='PresentationStates':
#                 #seriesinfo=server.DBWindowFind( {"request": "seriesInstanceUID == '" +  iseries +  "'", "table": "Series", "execute": "Nothing"})
#                 #print seriesinfo["elements"]
#                 continue
#             
#             seriesinfo=server.DBWindowFind( {"request": "seriesInstanceUID == '" +  iseries +  "'", "table": "Series", "execute": "Nothing"})
#             #print(seriesinfo["elements"][0]  )              
#             #print( len(seriesinfo["elements"]))
#             assert(len(seriesinfo["elements"]))
#               #  print(seriesinfo["elements"])
#              
#                 
#             #server.copySeries2DB( {"seriesInstanceUID": istudy, "targetDB":targetDB} )     
#             if seriesinfo["elements"][0].has_key("name"):
#             #    print seriesinfo["elements"][0]["name"]   
#                 if (re.search('RAPID|tmax|mtt|cbf|cbv|aif-plot|vof-plot|Lesion Sizes|vof plot|vof point|aif points',seriesinfo["elements"][0]["name"],re.IGNORECASE)):
#                      print "deleting" + seriesinfo["elements"][0]["name"]  
#                      #server.copySeries2DB( {"seriesInstanceUID": iseries, "targetDB":'RAPIDTMPDB DB'} )  
#                      #server.deleteSeries( {"seriesInstanceUID": iseries} )  
#                     # t=server.SetComment2forSeries({"seriesInstanceUID": iseries , "Comment2":"ADC" } )
#             
#==============================================================================
            
            

   # t=server.DBWindowFind( {"request": "sopInstanceUID == '" +  sopinstanceuid[0] +  "'", "table": "Image", "execute": "Nothing"})

   # for e in t["elements"]:
   #     print e["studyInstanceUID"]
    
    #server.GetSeriesForStudyInstanceUID( {"request": "studyInstanceUID == '" +e["studyInstanceUID"]+ " '", "table": "Series", "execute": "Nothing"})

    #server.MarkStudy(seriesUIDlist,'NCCT')
    #server.MarkSeries(seriesUIDlist,'NCCT')
#typical use - find all the series of number x y and z and then find the images
#    t=server.DBWindowFind( {"request": "id == '*'", "table": "Series", "execute": "Nothing"})

