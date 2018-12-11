#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:15:40 2017

@author: amar
"""
import json
import re
import os.path
import glob

fid=open('/Users/amar/Desktop/rapid46_testresult/96970_96971-MR/output.json')
ojson=json.loads(fid.read())
fid.close()

fid1=open('/Users/amar/Desktop/rapid46_testresult/96970_96971-MR/rapid_processing.log.txt','r')      
logtxt=fid1.read()
fid1.close()  

#Measurements_list=ojson['Measurements']
#cbf_or_tmax_mismatch_dict=Measurements_list[0]
#cbf_or_tmax_mismatch_results_list=cbf_or_tmax_mismatch_dict['Results']
#cbf_or_tmax_mismatch_results_list_slab0=cbf_or_tmax_mismatch_results_list[0]
#cbf_or_tmax_mismatch_results_list_slab1=cbf_or_tmax_mismatch_results_list[1]
#
#cbf_mismatch_results_list_slab0_dict=cbf_or_tmax_mismatch_results_list_slab0[0]['Volumes']
#tmax_mismatch_results_list_slab0_dict=cbf_or_tmax_mismatch_results_list_slab0[1]['Volumes']
#
#cbf_mismatch_results_list_slab1_dict=cbf_or_tmax_mismatch_results_list_slab1[0]['Volumes']
#tmax_mismatch_results_list_slab1_dict=cbf_or_tmax_mismatch_results_list_slab1[1]['Volumes']

if ojson['NumberOfPerfusionSlabs']==1:
    
    cbf_30_volume_slab0=ojson['Measurements'][0]['Results'][0][0]['Volumes']
#cbf_30_volume_slab1=ojson['Measurements'][0]['Results'][1][0]['Volumes']

    tmax_6_volume_slab0=ojson['Measurements'][0]['Results'][0][1]['Volumes']
#tmax_6_volume_slab1=ojson['Measurements'][0]['Results'][1][1]['Volumes']

    tmax_10_volume_slab0=ojson['Measurements'][1]['Results'][0]['Volumes'][3]
#tmax_10_volume_slab1=ojson['Measurements'][1]['Results'][1]['Volumes'][3]
    Numberofslabs=ojson['NumberOfPerfusionSlabs']

    Patientid=ojson['DICOMHeaderInfo']['Patient']['PatientID']

#dict = {'PatientID': Patientid, 'NumofSlabs':Numberofslabs, 'SlabAtmax6': tmax_6_volume_slab0,'SlabBtmax6': tmax_6_volume_slab1, 'SlabAtmax10':tmax_10_volume_slab0,'SlabBtmax10': tmax_10_volume_slab1, 'SlabAcore': cbf_30_volume_slab0, 'SlabBcore': cbf_30_volume_slab1 }
    dict = {'PatientID': Patientid, 'NumofSlabs':Numberofslabs, 'SlabAtmax6': tmax_6_volume_slab0, 'SlabAtmax10':tmax_10_volume_slab0, 'SlabAcore': cbf_30_volume_slab0 }

if ojson['NumberOfPerfusionSlabs']==2:
    
    cbf_30_volume_slab0=ojson['Measurements'][0]['Results'][0][0]['Volumes']
    cbf_30_volume_slab1=ojson['Measurements'][0]['Results'][1][0]['Volumes']

    tmax_6_volume_slab0=ojson['Measurements'][0]['Results'][0][1]['Volumes']
    tmax_6_volume_slab1=ojson['Measurements'][0]['Results'][1][1]['Volumes']

    tmax_10_volume_slab0=ojson['Measurements'][1]['Results'][0]['Volumes'][3]
    tmax_10_volume_slab1=ojson['Measurements'][1]['Results'][1]['Volumes'][3]
    Numberofslabs=ojson['NumberOfPerfusionSlabs']

    Patientid=ojson['DICOMHeaderInfo']['Patient']['PatientID']

    dict = {'PatientID': Patientid, 'NumofSlabs':Numberofslabs, 'SlabAtmax6': tmax_6_volume_slab0,'SlabBtmax6': tmax_6_volume_slab1, 'SlabAtmax10':tmax_10_volume_slab0,'SlabBtmax10': tmax_10_volume_slab1, 'SlabAcore': cbf_30_volume_slab0, 'SlabBcore': cbf_30_volume_slab1 }


  
    
op= re.search('Spatial resolution \((.* x .* x .*)\): (.*) x (.*) x (.*)',logtxt)
       

dict.update({op.group(1):[float(op.group(2)), float(op.group(3)), float(op.group(4))]})