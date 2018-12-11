#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 08:24:23 2017

@author: sorenc
"""


import  xmlrpclib
import openpyxl
import re
import os
from datetime import datetime, timedelta 
import numpy as np
import subprocess
import dicom as pydicom
import sys

   # server = Server("http://171.65.168.30:8080",verbose=True)
#server = Server("http://172.25.169.28:8085",verbose=False)

   # server = Server("localhost:8080",verbose=False)

#print server
#v=server.GetDisplayed2DViewerStudies()

#t=server.DBWindowFind( {"request": "name == '100'", "table": "Study", "execute": "Nothing"})

#==============================================================================
#     
#     #get all IDs
#     t=server.getPatientIDs( )
#     for cid in t:
#         print cid
#     
#     
#     st=server.PatientIDtoStudies(  {"patientID": t[0]})
#     for cstudy in st:
#         print cstudy
#     
#     
#     series=server.StudyUIDtoSeries(  {"studyInstanceUID": st[0]} )
#     
#     for cseries in series:
#        print cseries
#     
#     
#     images=server.SeriesUIDtoImages( {"seriesInstanceUID": series[0]})
#     
#==============================================================================
#bricasvej 22, hillerod
#t=server.SetComment1forStudy({"studyInstanceUID": st[0] , "Comment":"BL" } )

def osexec(cmd):
    pid = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)  #the +p prepends the hierachy and makes sure the match below only \
                                                 
    op = pid.communicate()
    return (pid.poll(),op)


def modify_tags(dirpath,tagdict,erase_private=False):
    #alter all the dicom files in the given path
    
    onlyfiles = [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]
    
    for ff in onlyfiles:
        ds = pydicom.read_file(dirpath+"/"+ff) 
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
                    print "deleting " + str(k.tag)
                    del ds[k.tag]   
        
        try:
            ds.save_as(dirpath+"/"+ff)
        except:
            print "problem modifying " + dirpath+"/"+ff 
            print "erasing file..."
            osexec("rm -f '" + dirpath+"/"+ff + "'")
            
            
def imgpathtopath(imgpath):
    loc=str( int(np.ceil( (float(imgpath)+1)/10000.0)*10000)) + "/" +imgpath+ ".dcm"
    return loc

   
def get_dicom_for_series(server, seriesUID, targetlocation):   #retrieve the files of that series  and writes it to the targetlocation (which must exist)
    #retrieve series info
    images=server.SeriesUIDtoImages({"seriesInstanceUID":   seriesUID })
    
    #make sure the folder is created if not present:
    if not os.path.exists(targetlocation):
        os.makedirs(targetlocation)
    
    for cimg in images:
        imgpath=cimg["pathNumber"]
        #sourcefilepath="/Users/sorenc/Documents/DEFUSE2DB/OsiriX\ Data/DATABASE.noindex/"+imgpathtopath(imgpath)
        sourcefilepath="/Users/sorenc/Documents/Horos\ Data/DATABASE.noindex/"+imgpathtopath(imgpath)
        cmd="cp " + sourcefilepath + " '" + targetlocation +"/'"
        op=osexec(cmd)
      #  print cmd
      #  print op
        
        
    #retrieve images and their location
    
def get_dicom_for_series_ICAS(server, seriesUID, targetlocation):   #retrieve the files of that series  and writes it to the targetlocation (which must exist)
    #retrieve series info
    images=server.SeriesUIDtoImages({"seriesInstanceUID":   seriesUID })
    
    #make sure the folder is created if not present:
    if not os.path.exists(targetlocation):
        pass
        #os.makedirs(targetlocation)
    #create an empty file called myscript.sh
    fid=open('myscript.sh','w')
    fid.write("mkdir -p "+ targetlocation + "\n")
    for cimg in images:
        imgpath=cimg["pathNumber"]
        #sourcefilepath="/Users/sorenc/Documents/DEFUSE2DB/OsiriX\ Data/DATABASE.noindex/"+imgpathtopath(imgpath)
        sourcefilepath="/Users/icasdb/Documents/Horos\ Data/DATABASE.noindex/"+imgpathtopath(imgpath)
        cmd="cp " + sourcefilepath + " '" + targetlocation +"/'"
        #print cmd to file
        print cmd
        fid.write(cmd + "\n")
        
    fid.close()    
    
    
    #transfer script
    o1=osexec("rsync -a myscript.sh icasdb@172.25.169.100:~/")
    o2=osexec("ssh  icasdb@172.25.169.100 " +"sh ./myscript.sh")
    #run script
    
    
      #  op=osexec(cmd)
      #  print cmd
      #  print op
            

    #typical use case. Get Series into particular folders, eg BL/seriesname_seriesUID
    
    
def deident_dicom_folder(folder):
    #use pydicom to strip files in folder
    pass

def get_series_info(server,seriesinfo_raw):
    seriesinfo={'status':1,'seriesInstanceUID':'','SeriesDescription':'','slicecount':-1,'framecount':-1,'modality':'','isophasic':False,"date":''}
    #seriesinfo_raw=server.DBWindowFind( {"request": "seriesInstanceUID == '" +  seriesuid +  "'", "table": "Series", "execute": "Nothing"})
            #print(seriesinfo["elements"][0]  )              
            #print( len(seriesinfo["elements"]))
    #assert(len(seriesinfo_raw["elements"])==1)    
    
    if seriesinfo_raw.has_key("modality"):
        seriesinfo["modality"]=seriesinfo_raw["modality"]
        
    if seriesinfo_raw.has_key("name"):
        seriesinfo["SeriesDescription"]=seriesinfo_raw["name"]
        
    if seriesinfo_raw.has_key("date"):
       seriesinfo["date"]=seriesinfo_raw["date"]
           
        
        
    seriesinfo["seriesInstanceUID"]=seriesinfo_raw["seriesInstanceUID"]
    #get the image info so we can calc slices and frames
    #print "seriesInstanceUID: " +seriesinfo_raw["seriesInstanceUID"]
    try:
        images=server.SeriesUIDtoImages({"seriesInstanceUID":   seriesinfo_raw["seriesInstanceUID"] })
    except:
        print "fatal error - UID not present, should never happen!" 
        print seriesinfo_raw
        #exit()
        
    imagelocations =set()
    locations_valid=True
    for k in images:
        if k.has_key("sliceLocation"):
            imagelocations.add(k["sliceLocation"])
        else:
            locations_valid=False
            break
        
    seriesinfo["slicecount"]=len(images)    #if case is isophasic this is altered below
    if locations_valid:   #we could read locations of all slices
        totalimages=len(images)
        uniquelocations=len(imagelocations)
        if (totalimages%uniquelocations)==0:
            seriesinfo["isophasic"]=True
            seriesinfo["slicecount"]=uniquelocations
            seriesinfo["framecount"]=totalimages/uniquelocations

        
    return seriesinfo    
    #TODO - enhanced DICOMs....
        
    
class PatientTimePointLabel:
    def __init__(self,ID,label,timerange,modal='ANY',requiredserieslabels=[]):
        self._ID=ID
        labelarray=[label,timerange,modal,requiredserieslabels]

        self._labels=[labelarray]
    
    def addrule(self,label,timerange,modal='ANY',requiredserieslabels=[]):
        labelarray=[label,timerange,modal,requiredserieslabels]

        self._labels.append(labelarray)
        
        
    def labelstudies(self,server,dryrun=1):   #search for matches on server and label them       
        matches=set()
        
        studies=server.PatientIDtoStudies(  {"patientID": self._ID})  
        dates=[d["date"] for d in studies]
        
        sorted_studies=[study for (cdate,study) in sorted(zip(dates,studies))]
        
        for cstudy in sorted_studies:
             studytime= cstudy["date"]  
             studydatetime=datetime.strptime(studytime[0:19],'%Y-%m-%d %H:%M:%S')
            #print   "   " +studytime[0:19]
             
             for crule in self._labels:
                 label=crule[0]
                 timerange=crule[1]
                 modal=crule[2]
                 requiredlabels=crule[3]
                 if ((studydatetime>timerange[0])and studydatetime<timerange[1]):
                 #elapsed time
                      print "\t" +label +' at ' +   self._ID + " " +  cstudy["date"][0:19] 
                      matches.add(label)
                      if not dryrun:
                          print "about to label: " +  cstudy["studyInstanceUID"] + "  with " + label
                          labelout=server.SetComment2forStudy({"studyInstanceUID": cstudy["studyInstanceUID"] , "Comment":label } )  
                          assert(labelout==label)
        #return matches
        return matches

#composite use - find all Series called something with DWI....
class LabelPattern:
    def __init__(self,label,rein,reout,slicesmin=0,slicesmax=float("inf"),framesmin=-1,framesmax=float("inf"),modality='ANY'):  #eventually this could also contain a dicom dict for matching
        self._label=label
        self._rein=rein
        self._reout=reout
        self._slicesmin=slicesmin
        self._slicesmax=slicesmax
        self._framesmin=framesmin
        self._framesmax=framesmax
        self._modality=modality

    def ismatch(self,seriesname,slicecount,framecount,modality):
        rein_ok=re.search(self._rein,seriesname,re.IGNORECASE)
        #if not rein_ok:
        #    print "t"
        reout_ok=False if re.search(self._reout,seriesname,re.IGNORECASE) else True
        slicecount_ok=True if ((slicecount>=self._slicesmin) and (slicecount<=self._slicesmax) ) else False
        framecount_ok=True if ((framecount>=self._framesmin) and (framecount<=self._framesmax) ) else False
        modality_ok=True if self._modality=='ANY' else (True if self._modality==modality else False)
        if (rein_ok and reout_ok and slicecount_ok and framecount_ok and modality_ok):
            return True
        else:
            return False
   
def labelcomment2forseries(seriesdicts,server,ruleset,dryrun=1):
    labels={}
    for cseries in seriesdicts:
        seriesinfo=get_series_info(server,cseries)
        
        for crule in ruleset: 
            if crule.ismatch(seriesinfo["SeriesDescription"],seriesinfo["slicecount"],seriesinfo["framecount"],seriesinfo["modality"]):
                if not dryrun:
                    aa=server.SetComment2forSeries({"seriesInstanceUID": seriesinfo["seriesInstanceUID"] , "Comment2":crule._label } )  
                    print "\t" +crule._label + ":" +seriesinfo["SeriesDescription"] + seriesinfo["date"]
                    if not aa==crule._label:
                        print "error in " + seriesinfo["seriesInstanceUID"] + " label is " +crule._label+ " but i am reading: " + aa
                else:
                    print "\t" + crule._label + ":" +seriesinfo["SeriesDescription"] + seriesinfo["date"]
                
                labels[cseries["seriesInstanceUID"]]   = crule._label
                
               
          
def labelcomment3forseries(seriesdicts,server,ruleset,dryrun=1):
    labels={}
    for cseries in seriesdicts:
        try:
            seriesinfo=get_series_info(server,cseries)
       # print seriesinfo["SeriesDescription"]
        except:
           print "tmp abort"
           print cseries
           return
       
        for crule in ruleset: 
            if crule.ismatch(seriesinfo["SeriesDescription"],seriesinfo["slicecount"],seriesinfo["framecount"],seriesinfo["modality"]):
                if not dryrun:
                    if seriesinfo.has_key("comment3") and (seriesinfo["comment3"]==rule._label):
                        continue
                    #print "\t" +  crule._label + ":" +seriesinfo["SeriesDescription"] + " " +seriesinfo["date"]
                    aa=server.SetComment3forSeries({"seriesInstanceUID": seriesinfo["seriesInstanceUID"] , "Comment2":crule._label } )  
                  #  print "\t" +  crule._label + ":" +seriesinfo["SeriesDescription"] + " " +seriesinfo["date"]
                    if not aa==crule._label:
                        print "error in " + seriesinfo["seriesInstanceUID"] + " label is " +crule._label+ " but i am reading: " + aa
                    
                    
                else:
                     print "\t" +  crule._label + ":" +seriesinfo["SeriesDescription"] + " " +seriesinfo["date"]
                
                labels[cseries["seriesInstanceUID"]]   = crule._label
                
            else:
                pass
                #print seriesinfo["SeriesDescription"]
                #print "no match"
          

     
    
    
def getImageSeriesUIDsForStudies(server,studyUIDarray):     
    imageseriesobjects=[]
    for istudy in studyUIDarray:
        try:
            series=server.StudyUIDtoSeries(  {"studyInstanceUID": istudy["studyInstanceUID"]} )    
        except:
            print "Fatal comm failure for studyInstanceUID:"   +istudy["studyInstanceUID"]
            #quit()
            
        for iseries in series:        
            if iseries['seriesInstanceUID']=='OsiriX Annotations SR' or iseries['seriesInstanceUID']=='OsiriX Report SR' or iseries['seriesInstanceUID']=='LOCALIZER' or iseries['seriesInstanceUID']=='OsiriX ROI SR' or iseries['seriesInstanceUID']=='PresentationStates':
                continue
           
            imageseriesobjects.append(iseries)     
        
        
    return imageseriesobjects
#==============================================================================
#     seriesinfo["status"]=0
#     seriesinfo["seriesInstanceUID"]=seriesuid
#     seriesinfo["SeriesDescription"]=seriesinfo_raw["elements"][0]["name"] if seriesinfo_raw["elements"][0].has_key("name") else ''
#     seriesinfo["slicecount"]=
#     seriesinfo["framecount"]=
#     seriesinfo["modality"]=seriesinfo_raw["elements"][0]["modality"]
#==============================================================================
#==============================================================================
#server = xmlrpclib.Server("http://172.25.169.28:8085",verbose=False)
#server = xmlrpclib.Server("http://192.168.0.10:8080",verbose=False)



