#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 08:47:45 2017

@author: sorenc
"""


import dicom as pydicom
import  xmlrpclib
from osirixutils import *
import time
import icas_sheet

server = xmlrpclib.Server("http://172.25.169.100:8080",verbose=False)




#set up labelling rules
#ncctrule=LabelPattern('NCCT','head|noncon|non con|soft|non|5mm axial|H41s|axial|brain','bone|cor|sag|mip|ax bn',slicesmin=5,slicesmax=2000,framesmin=-1,framesmax=2,modality='CT') #frames=-1 allows no isophasic
tofrule=LabelPattern('TOF','tof|mra|pjn|mip|cow|spin|tumble|reformat|right|left|posterior|processed images','bone',slicesmin=1,slicesmax=2000,framesmin=-1,framesmax=100,modality='MR')
clearrule=LabelPattern('','.*','NOMATCH')
dwirule=LabelPattern('DWI','dwi|diff','exponen|adc|apparent|summary|colored|iso|COR|MULTI|Resampled|lesion')
mrprule=LabelPattern('PWI','pwi|perf','TTP|screensave|fmri',slicesmin=1,slicesmax=320,framesmin=30,framesmax=100,modality='MR')
ctprule=LabelPattern('CTP1','CTP|perf|prox','RAPID|neuro',slicesmin=2,slicesmax=320,framesmin=30,framesmax=100,modality='CT')
ctprule2=LabelPattern('CTP2','2nd|distal','RAPID|neuro',slicesmin=2,slicesmax=320,framesmin=30,framesmax=100,modality='CT')
flairrule=LabelPattern('FLAIR','flair|tirm','bone',slicesmin=1,slicesmax=2000,framesmin=-1,framesmax=100,modality='MR')
#ctprule=LabelPattern('CTP','perf|shuttle|axial|40cc|above','bone',slicesmin=2,slicesmax=320,framesmin=10,framesmax=100,modality='CT')
#ctarule=LabelPattern('CTA','thin|cow|cta|angio','perf|ctp|above',slicesmin=-1,slicesmax=2000,framesmin=-1,framesmax=100,modality='CT')
aslrule=LabelPattern('ASLCBF','eASL\ TT\ recon\:\ TT\ corrected\ CBF\ \(color\)|\(Color\ Transit\ corrected\ CBF\)\ eASL\:\ TT\ map','RAPID')
#corclear=LabelPattern('','COR DIFFUSION','NOMATCH')
#ruleset=[mrprule]
#ruleset=[mrprule,dwirule]
#ruleset=[mrprule]
ruleset2=[aslrule]
#remove_ctp_rule=LabelPattern('','perf','exponen')
#ruleset2=[remove_ctp_rule]

#connect
IDs=server.getPatientIDs( )
sortedIDs=sorted(IDs)


for cid in sortedIDs[0:0]: #sortedIDs: #sortedIDs:  #sortedIDs[0:1]:
    #iterate series and label each series
    print cid
    studies=server.PatientIDtoStudies(  {"patientID": cid})  
    
    #for s in studies:
    #    server.SetComment2forStudy({"studyInstanceUID": s["studyInstanceUID"] , "Comment":"" } )  
    
    
    seriesdicts=getImageSeriesUIDsForStudies(server,studies)
    
#    labelcomment3forseries(seriesdicts,server,ruleset2,dryrun=0)
   # labelcomment2forstudy(seriesdicts,server,ruleset,dryrun=0)      #label the series if there is a match
    labelcomment3forseries(seriesdicts,server,ruleset2,dryrun=0)      #label the series if there is a match
    
#    labelcomment3forseries(seriesdicts,server,ruleset2,dryrun=0) 
    time.sleep(1)
            




bl_times=icas_sheet.getBLtimes()

for cid in sortedIDs[0:0]:   #sortedIDs[74:75]:   #sortedIDs[0:10]:
    
    if not bl_times.has_key(cid):  #some patients are not in the sheet all all
        print cid + " is not in the sheet"
        continue

    BLtime=bl_times[cid]
    

    
    BL_trange_min=BLtime - timedelta(hours=6)
    BL_trange_max=BLtime + timedelta(hours=2)  #we dont want to capture the eFU here
    crule=PatientTimePointLabel(cid,'BL',[BL_trange_min,BL_trange_max])

    crule.labelstudies(server,dryrun=0)
    time.sleep(1)
    
for cid in sortedIDs[0:0]:   #sortedIDs[74:75]:   #sortedIDs[0:10]:
    
    if not bl_times.has_key(cid):  #some patients are not in the sheet all all
        print cid + " is not in the sheet"
        continue

    BLtime=bl_times[cid]
    

    
    BL_trange_min=BLtime + timedelta(hours=2)
    BL_trange_max=BLtime + timedelta(hours=48)  #we dont want to capture the eFU here
    crule=PatientTimePointLabel(cid,'FU',[BL_trange_min,BL_trange_max])

    crule.labelstudies(server,dryrun=0)
    time.sleep(1)
#
##check all cases for 1xDWI and 1xPWI at BL
#for cid in sortedIDs[0:0]: #sortedIDs: #sortedIDs:  #sortedIDs[0:1]:
#    #iterate series and label each series
#    print cid
#    studies=server.PatientIDtoStudies(  {"patientID": cid})  
#    
#    BLstudies=[k for k in studies if (k.has_key("comment2") and k["comment2"]=="BL" )]
#    #for s in studies:
#    #    server.SetComment2forStudy({"studyInstanceUID": s["studyInstanceUID"] , "Comment":"" } )  
#    
#    for cstudy in BLstudies:
#        npwi=0
#        ndwi=0
#        nctp=0
#        seriesdicts=getImageSeriesUIDsForStudies(server,[cstudy])
#        for l in range(len(seriesdicts)):
##            if (seriesdicts[l].has_key("comment3") and seriesdicts[l]["comment3"]=="DWI"):
##                ndwi=ndwi+1
##                targetfolder='/Volumes/ICAS/RAPID/'+cid + '/BL/DWI'
##                get_dicom_for_series_ICAS(server,seriesdicts[l]["seriesInstanceUID"],targetfolder)
#                #transfer
##            elif (seriesdicts[l].has_key("comment3") and seriesdicts[l]["comment3"]=="PWI"):
##                npwi=npwi+1
##                targetfolder='/Volumes/ICAS/RAPID/'+cid + '/BL/PWI'
##                get_dicom_for_series_ICAS(server,seriesdicts[l]["seriesInstanceUID"],targetfolder)
#                #transfer
#            if (seriesdicts[l].has_key("comment3") and seriesdicts[l]["comment3"]=="CTP1"):
#                nctp=nctp+1
#                targetfolder='/Volumes/ICAS/RAPID_BLCT/'+cid + '/BL/CTP1'
#                get_dicom_for_series_ICAS(server,seriesdicts[l]["seriesInstanceUID"],targetfolder)
#            elif (seriesdicts[l].has_key("comment3") and seriesdicts[l]["comment3"]=="CTP2"):
#                nctp=nctp+1
#                targetfolder='/Volumes/ICAS/RAPID_BLCT/'+cid + '/BL/CTP2'
#                get_dicom_for_series_ICAS(server,seriesdicts[l]["seriesInstanceUID"],targetfolder)
#                #transfer
##    with open('/Users/amar/Desktop/data_arrange/TEST.txt', 'a') as f:
##        f.write( 'Patient {0} has {1} dwi and {2} pwi \n'.format(cid,ndwi,npwi))
#    
#    time.sleep(1)
            

for cid in sortedIDs[0:108]: #sortedIDs: #sortedIDs:  #sortedIDs[0:1]:
    #iterate series and label each series
    print cid
    studies=server.PatientIDtoStudies(  {"patientID": cid})  
    
    FUstudies=[k for k in studies if (k.has_key("comment2") and k["comment2"]=="FU" )]
    #for s in studies:
    #    server.SetComment2forStudy({"studyInstanceUID": s["studyInstanceUID"] , "Comment":"" } )  
    
    for cstudy in FUstudies:
        npwi=0
        ndwi=0
        nctp=0
        seriesdicts=getImageSeriesUIDsForStudies(server,[cstudy])
        for l in range(len(seriesdicts)):
            if (seriesdicts[l].has_key("comment3") and seriesdicts[l]["comment3"]=="ASLCBF"):
                ndwi=ndwi+1
                targetfolder='/Volumes/ICAS/RAPID_ASL/'+cid + '/FU/ASLCBF'
                get_dicom_for_series_ICAS(server,seriesdicts[l]["seriesInstanceUID"],targetfolder)
              
#            elif (seriesdicts[l].has_key("comment3") and seriesdicts[l]["comment3"]=="PWI"):
#                npwi=npwi+1
#                targetfolder='/Volumes/ICAS/RAPID_FU/'+cid + '/FU/PWI'
#                get_dicom_for_series_ICAS(server,seriesdicts[l]["seriesInstanceUID"],targetfolder)
#                
#            elif (seriesdicts[l].has_key("comment3") and seriesdicts[l]["comment3"]=="CTP1"):
#                nctp=nctp+1
#                targetfolder='/Volumes/ICAS/RAPID_FU/'+cid + '/FU/CTP1'
#                get_dicom_for_series_ICAS(server,seriesdicts[l]["seriesInstanceUID"],targetfolder)
#            elif (seriesdicts[l].has_key("comment3") and seriesdicts[l]["comment3"]=="CTP2"):
#                nctp=nctp+1
#                targetfolder='/Volumes/ICAS/RAPID_FU/'+cid + '/FU/CTP2'
#                get_dicom_for_series_ICAS(server,seriesdicts[l]["seriesInstanceUID"],targetfolder)
#                #transfer
#    with open('/Users/amar/Desktop/data_arrange/TEST.txt', 'a') as f:
#        f.write( 'Patient {0} has {1} dwi and {2} pwi \n'.format(cid,ndwi,npwi))
    
    time.sleep(1)
    
for cid in []: #sortedIDs: #sortedIDs: #sortedIDs:  #sortedIDs[0:1]:
    #iterate series and label each series

    studies=server.PatientIDtoStudies(  {"patientID": cid})  
    
    BLstudies=[]
    for k in studies:
        if k.has_key("comment2") and k["comment2"]=="BL":
            BLstudies.append(k)
            
            
    seriesdicts=getImageSeriesUIDsForStudies(server,BLstudies)
    
    
    dwipwiseries=[]
    for k in seriesdicts:
        if k.has_key("comment3") and (k["comment3"]=="PWI" or k["comment3"]=="DWI"):
            dwipwiseries.append(k)
    
    
    #iterate series to transfer
    for k in dwipwiseries:    
        targetfolder="/Users/sorenc/NCCT_B2/"+ cid +"/"+k["comment3"] + "_"+k["seriesDICOMUID"]
        get_dicom_for_series_ICAS(server,k["seriesInstanceUID"],targetfolder)
                
    
   # labelcomment2forstudy(seriesdicts,server,ruleset,dryrun=0)      #label the series if there is a match
    


#IDs=server.getPatientIDs( )



#label series

#studies=server.PatientIDtoStudies(  {"patientID": '212'} )  


#seriesdicts=getImageSeriesUIDsForStudies(server,studies)


#server.SeriesUIDtoImages({"seriesInstanceUID":   seriesUID })
