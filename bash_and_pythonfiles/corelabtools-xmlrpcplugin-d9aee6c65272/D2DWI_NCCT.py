#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 16:29:59 2017

@author: sorenc
"""



import  xmlrpclib
from osirixutils import *
import openpyxl
import re
import D2worksheet
from datetime import datetime, timedelta 
import numpy as np
import time



server = xmlrpclib.Server("http://localhost:8080",verbose=False)


IDs=server.getPatientIDs( )
sheet=D2worksheet.getSheet()

treatmentIDs=[cid for (cid,cohort) in zip(sheet["studyNumber"], sheet["cohortType"]) if cohort==1]


CoreLab_CTASPECTS=sheet["CoreLab_CT-ASPECTS"]
Time_CTtoMRIbl=sheet["Time_CTtoMRIbl"]
studyNumber=sheet["studyNumber"]

#we expect:
    # acure nnct for all cases with aspects
    #in these cases, we expect the image delta to reflect the sheet delta

    #generate a "have" dict of NCCT vs MR-CT delta and then a "shouldhave" dict of similar structure. Then compare these sets for overlap and time where in correspondence
    

shouldhavedict={}
havedict={}
      
for tid in studyNumber:
    if CoreLab_CTASPECTS[studyNumber.index(tid)]:
        shouldhavedict[tid]=Time_CTtoMRIbl[studyNumber.index(tid)]


sortedIDs=sorted(IDs)
sortedIDs=sortedIDs[0:10]


timearray=np.zeros((len(sortedIDs)))
IDarray_hastime=[]
hasDWIandNCCT=0
#list cases with CT but no NCCT to detect inadequate labelling

for cid in sortedIDs:   #sortedIDs[0:10]:
    studies=server.PatientIDtoStudies(  {"patientID": cid})  
    #print cid
    BLstudies=[k for k in studies  if ( k.has_key("comment2") and k["comment2"]=="BL" ) ]
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
            if iseries.has_key("comment3") and iseries["comment3"]=="DWI":    
                dwi_present=True
                dwi_time=datetime.strptime(iseries["date"][0:19],'%Y-%m-%d %H:%M:%S')
               
               
            
    if ncct_present and dwi_present:
        havedict[cid]=(dwi_time-ncct_time).total_seconds()/(60*60)
        timearray[hasDWIandNCCT]=havedict[cid]
        IDarray_hastime.append(cid)
        hasDWIandNCCT=hasDWIandNCCT+1
        if shouldhavedict.has_key(cid[0:5]):
            diff_hours=havedict[cid]-shouldhavedict[cid[0:5]]
        
            print "diff in hours: " +str(diff_hours)
        else:
            print cid + " is in the imageDB but not in the sheet!"
        #now compare this time with the sheet


    if ncct_present and not dwi_present:
        print cid + " does not have BL DWI, this should never happen!"
        
    if (not ncct_present) and (not dwi_present):
        print cid + " does not have BL DWI or NCCT, this should never happen!"
            
        
    if  (not ncct_present) and  dwi_present:
        if cid in shouldhavedict.keys():  #should we have a ncct for this casE?
            print cid + " does not have BL NCCT, but sheet says it does!" 




print "Cases with DWI and NCCT: " + str(hasDWIandNCCT)
print "Median time between NCCT and DWI " + str(np.median(timearray[0:hasDWIandNCCT]))
print "# with delta time <2h " + str(np.sum(timearray[0:hasDWIandNCCT]<2  ) )
print "# with delta time <1h " + str(np.sum(timearray[0:hasDWIandNCCT]<1  ) )
print "# with delta time <0.5h " + str(np.sum(timearray[0:hasDWIandNCCT]<.5  ) )

print "Cases with delta<150 mins: " + str(hasDWIandNCCT)


ID_time=zip(IDarray_hastime,timearray[0:hasDWIandNCCT])

IDslt2p5=set([ID for (ID,dtime) in ID_time if dtime<1.0])


allIDs=set(IDarray_hastime)

#copy BL DWI and NCCT to "DWINCCT DB"
storelist=allIDs-IDslt2p5

for cid in sortedIDs[0:50]:
    studies=server.PatientIDtoStudies(  {"patientID": cid})  
    #print cid
    BLstudies=[k for k in studies  if ( k.has_key("comment2") and k["comment2"]=="BL" ) ]
    if len (BLstudies)==0:
        continue
    #late take the studies 1-by-1
    seriesdicts=getImageSeriesUIDsForStudies(server,BLstudies)
 
    for iseries in seriesdicts:
            
        if iseries.has_key("comment3") and (iseries["comment3"]=="NCCT" or iseries["comment3"]=="DWI"):    
        #if iseries.has_key("comment3") and (iseries["comment3"]=="NCCT"):    
            print iseries["name"]
            
            targetfolder="/Users/sorenc/NCCT_B2/"+ cid[0:5] +"/"+iseries["comment3"] + "_"+iseries["seriesDICOMUID"]
            #get_dicom_for_series(server,iseries["seriesInstanceUID"],targetfolder)
          
            #server.copySeries2DB( {"seriesInstanceUID": iseries["seriesInstanceUID"], "targetDB":'DWINCCT DB'} )  
                #time.sleep(2)



#for reg iteration 1:
    #'01015_SCH' no acute DWI lesion
     
   #  '02003_V_V',  DWI positive
   
   #'02004_J_W', DWI positive 
   #'02007_BES', DWI+
   #'03003_DCL', DWI+
  # '03011_JMD', DWI+
   
   #'03014_RLS', DWI+
   #'05002_KHC', DWI+
   #'05008_E_K', DWI+
  # '05009_R_S', DWI+
   
  # '11001_G_M'], DWI+