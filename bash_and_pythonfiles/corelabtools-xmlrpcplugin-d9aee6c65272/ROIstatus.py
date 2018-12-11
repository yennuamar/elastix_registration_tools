#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 14:11:27 2017

@author: sorenc
"""
import  xmlrpclib
import openpyxl
import re

from datetime import datetime, timedelta 
import os
server = xmlrpclib.Server("http://171.65.168.30:8080",verbose=False)



#read in the total to-do
fid=open('casesWROI.lst')

expectedIDs=set(fid.read().rstrip().split('\n'))
fid.close()



fid=open('todos')
todos=set(fid.read().split('\n'))
fid.close()


#read in what we have in the final DB (assume that DB is active)

IDs_server=set(server.getPatientIDs())


missing=expectedIDs-IDs_server



#lets get the series UIDs so we can go look for the scan IDs from Michael
ll=open('/home/sorenc/matlabwork/DEFUSE3/ROIexport/ID_suid.lst').read().rstrip().split('\n')
suids={}
for p in ll:
    cc=p.split(" ")
    suids[cc[0]]=  cc[1]      


#just go over what we have


#now for each studyUID, get the scan ID

for ID in sorted(expectedIDs):
    lookingfor=suids[ID] 
          
    studies=server.PatientIDtoStudies(  {"patientID": ID})  
    print ID
    found=False
    for p in studies:
       if p["studyInstanceUID"]==lookingfor:
           found=True
           if p.has_key('comment2'):
               print "\t" + p["comment2"]
           else:
               print "\tUnexpected, did not find comment2 in " + lookingfor 
    if not found:
        print "\tNo Match..."