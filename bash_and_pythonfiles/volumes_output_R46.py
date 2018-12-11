#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 10:02:21 2017

@author: amar
"""

import json
import re
import os.path
import glob



files =[]
files1= []
start_dir = '/Users/amar/Desktop/data_arrange3'
pattern   = "output.json"

for dir,_,_ in os.walk('/Volumes/RAPID_PROCESSING/proc_rapid45_20cases'):
    files.extend(glob.glob(os.path.join(dir,'output.json'))) 

    

for i in range(len(files)):
    
    fid=open(files[i])
    ojson=json.loads(fid.read())
    fid.close()
       

    rapid_output_volume_list=[]
    dict ={}
    print(i)
    print(files[i])
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
    try:
        print(ojson['ResultSourceSeriesType'])
    except:
        continue
    if  str(ojson['ResultSourceSeriesType'][0]) == 'diff':
        core_volume_slab0=ojson['Measurements'][0]['Results'][0]['Volumes']
       

        Patientid=ojson['DICOMHeaderInfo']['Patient']['PatientID']
        if re.search('BL',files[i],re.I):
            BLorFU='BL'
        if re.search('FU',files[i],re.I):
            BLorFU='FU'
            
        try:
            Seriesdate=ojson['DICOMHeaderInfo']['PerfusionSeries'][0]['SeriesDate']
            Seriestime=ojson['DICOMHeaderInfo']['PerfusionSeries'][0]['SeriesTime']
        except:
            Seriesdate=ojson['DICOMHeaderInfo']['DiffusionSeries'][0]['SeriesDate']
            Seriestime=ojson['DICOMHeaderInfo']['DiffusionSeries'][0]['SeriesTime']
#dict = {'PatientID': Patientid, 'NumofSlabs':Numberofslabs, 'SlabAtmax6': tmax_6_volume_slab0,'SlabBtmax6': tmax_6_volume_slab1, 'SlabAtmax10':tmax_10_volume_slab0,'SlabBtmax10': tmax_10_volume_slab1, 'SlabAcore': cbf_30_volume_slab0, 'SlabBcore': cbf_30_volume_slab1 }
        
        
        numberofslices=ojson['DICOMHeaderInfo']['DiffusionSeries'][0]['NumberOfSlices']
        slicethickness=ojson['DICOMHeaderInfo']['DiffusionSeries'][0]['SliceThickness']
        zcoverage=numberofslices*float(slicethickness)
        
        try:
            modality=numberofslices=ojson['DICOMHeaderInfo']['DiffusionSeries'][0]['Modality']
        except:
            modality=numberofslices=ojson['DICOMHeaderInfo']['PerfusionSeries'][0]['Modality']
            


        dict = {'PatientID': int(Patientid),'modality':modality, 'BL/FU': BLorFU, 'SeriesDate': Seriesdate+ '-' +Seriestime, 'NumofSlabs': 1, 'Zcoverage': zcoverage , 'SlabAcore': float(core_volume_slab0[0]),'SlabAtmax6': 'NA', 'SlabAtmax10': 'NA' }
    
        rapid_output_volume_list.append(dict)
        

        
        with open('/Users/amar/Desktop/data_arrange3/json_volumes/' + 'ALL' + '.txt', 'a') as f:
            print(dict.values(), file=f)
        
        with open('/Users/amar/Desktop/data_arrange3/json_volumes/' + Patientid + '.txt', 'a') as f:
            print(files[i] , file =f)
            print('\n', file =f)
            print( dict , file=f)
            print('\n\n\n', file =f)
        continue
    
    if ojson['NumberOfPerfusionSlabs']==1:
        try:
            core_volume_slab0=ojson['Measurements'][0]['Results'][0][0]['Volumes']
        except:
            print('No suitable AIF location was found')
            continue
#cbf_30_volume_slab1=ojson['Measurements'][0]['Results'][1][0]['Volumes']

        tmax_6_volume_slab0=ojson['Measurements'][0]['Results'][0][1]['Volumes']
#tmax_6_volume_slab1=ojson['Measurements'][0]['Results'][1][1]['Volumes']

        tmax_10_volume_slab0=ojson['Measurements'][1]['Results'][0]['Volumes'][3]
#tmax_10_volume_slab1=ojson['Measurements'][1]['Results'][1]['Volumes'][3]
        Numberofslabs=ojson['NumberOfPerfusionSlabs']

        Patientid=ojson['DICOMHeaderInfo']['Patient']['PatientID']
        if re.search('BL',files[i],re.I):
            BLorFU='BL'
        if re.search('FU',files[i],re.I):
            BLorFU='FU'
        try:
            Seriesdate=ojson['DICOMHeaderInfo']['PerfusionSeries'][0]['SeriesDate']
            Seriestime=ojson['DICOMHeaderInfo']['PerfusionSeries'][0]['SeriesTime']
        except:
            Seriesdate=ojson['DICOMHeaderInfo']['DiffusionSeries'][0]['SeriesDate']
            Seriestime=ojson['DICOMHeaderInfo']['DiffusionSeries'][0]['SeriesTime']
#dict = {'PatientID': Patientid, 'NumofSlabs':Numberofslabs, 'SlabAtmax6': tmax_6_volume_slab0,'SlabBtmax6': tmax_6_volume_slab1, 'SlabAtmax10':tmax_10_volume_slab0,'SlabBtmax10': tmax_10_volume_slab1, 'SlabAcore': cbf_30_volume_slab0, 'SlabBcore': cbf_30_volume_slab1 }
        
        
        numberofslices=ojson['DICOMHeaderInfo']['PerfusionSeries'][0]['NumberOfSlices']
        try:
            slicethickness=ojson['DICOMHeaderInfo']['PerfusionSeries'][0]['SliceThickness']
            zcoverage=numberofslices*float(slicethickness)
        except:
            print('slice thickness not found')
            zcoverage='NA'
                
        try:
            modality=numberofslices=ojson['DICOMHeaderInfo']['DiffusionSeries'][0]['Modality']
        except:
            modality=numberofslices=ojson['DICOMHeaderInfo']['PerfusionSeries'][0]['Modality']

        dict = {'PatientID': int(Patientid),'modality':modality, 'BL/FU': BLorFU,'SeriesDate': Seriesdate+ '-' +Seriestime, 'NumofSlabs': int(Numberofslabs), 'Zcoverage': zcoverage , 'SlabAcore': float(core_volume_slab0[0]) , 'SlabAtmax6': float(tmax_6_volume_slab0[0]), 'SlabAtmax10':tmax_10_volume_slab0}
        rapid_output_volume_list.append(dict)
        
        with open('/Users/amar/Desktop/data_arrange3/json_volumes/' + 'ALL' + '.txt', 'a') as f:
            print(dict.values(), file=f)
        with open('/Users/amar/Desktop/data_arrange3/json_volumes/' + Patientid + '.txt', 'a') as f:
            print(files[i], file =f)
            print('\n', file =f)
            print( dict , file=f)
            print('\n\n\n', file =f)
            
            
    if ojson['NumberOfPerfusionSlabs']==2:
        try:
            core_volume_slab0=ojson['Measurements'][0]['Results'][0][0]['Volumes']
            core_volume_slab1=ojson['Measurements'][0]['Results'][1][0]['Volumes']
        except:
            print('No suitable AIF location was found')
            

        tmax_6_volume_slab0=ojson['Measurements'][0]['Results'][0][1]['Volumes']
        tmax_6_volume_slab1=ojson['Measurements'][0]['Results'][1][1]['Volumes']

        tmax_10_volume_slab0=ojson['Measurements'][1]['Results'][0]['Volumes'][3]
        tmax_10_volume_slab1=ojson['Measurements'][1]['Results'][1]['Volumes'][3]
        Numberofslabs=ojson['NumberOfPerfusionSlabs']

        Patientid=ojson['DICOMHeaderInfo']['Patient']['PatientID']
        if re.search('BL',files[i],re.I):
            BLorFU='BL'
        if re.search('FU',files[i],re.I):
            BLorFU='FU'


        try:
            Seriesdate=ojson['DICOMHeaderInfo']['PerfusionSeries'][0]['SeriesDate']
            Seriestime=ojson['DICOMHeaderInfo']['PerfusionSeries'][0]['SeriesTime']
        except:
            Seriesdate=ojson['DICOMHeaderInfo']['DiffusionSeries'][0]['SeriesDate']
            Seriestime=ojson['DICOMHeaderInfo']['DiffusionSeries'][0]['SeriesTime']
        
        
        
        numberofslices0=ojson['DICOMHeaderInfo']['PerfusionSeries'][0]['NumberOfSlices']
        slicethickness0=ojson['DICOMHeaderInfo']['PerfusionSeries'][0]['SliceThickness']
        numberofslices1=ojson['DICOMHeaderInfo']['PerfusionSeries'][1]['NumberOfSlices']
        slicethickness1=ojson['DICOMHeaderInfo']['PerfusionSeries'][1]['SliceThickness']
        zcoverage0=numberofslices0*float(slicethickness0)
        zcoverage1=numberofslices1*float(slicethickness1)
        zcoverage=zcoverage0+zcoverage1
        
                
        try:
            modality=numberofslices=ojson['DICOMHeaderInfo']['DiffusionSeries'][0]['Modality']
        except:
            modality=numberofslices=ojson['DICOMHeaderInfo']['PerfusionSeries'][0]['Modality']
     
        dict = {'PatientID': int(Patientid),'modality':modality,'BL/FU': BLorFU, 'SeriesDate': Seriesdate+ '-' +Seriestime, 'NumofSlabs': int(Numberofslabs), 'Zcoverage': zcoverage ,  'TotalCoreVolume': float(core_volume_slab0[0]) + float(core_volume_slab1[0]),'Totaltmax6Volume': float(tmax_6_volume_slab0[0]) + float(tmax_6_volume_slab1[0]), 'Totaltmax10Volume': tmax_10_volume_slab0 + tmax_10_volume_slab1 }
        rapid_output_volume_list.append(dict)
        
        with open('/Users/amar/Desktop/data_arrange3/json_volumes/' + 'ALL' + '.txt', 'a') as f:
            print(dict.values(), file=f)
        with open('/Users/amar/Desktop/data_arrange3/json_volumes/' + Patientid + '.txt', 'a') as f:
            print(files[i], file =f)
            print('\n', file =f)
            print( dict , file=f)
            print('\n\n\n', file =f)

     
    