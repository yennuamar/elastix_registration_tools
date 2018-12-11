# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 17:33:50 2016

@author: sorenc
"""

import sys
import json

def get_no_voldict():
     return {"returncode":1,"tmaxthresholds":[-1,-1,-1,-1],"tmaxvolumes":[-1,-1,-1,-1],"coremodal":"NA",
                "corevolumes":[-1,-1,-1,-1],"corethresholds":[-1,-1,-1,-1],"numberofslabs":-1,"HypoperfusionIndex_slab1":-1,"CBVIndex_slab1":-1,"HypoperfusionIndex_slab2":-1,"CBVIndex_slab2":-1}

def readJSON(f):
    #f="/home/sorenc/RAPID46_TEST_OUTPUT/102026_20130908T174011_CT_SLABA/measurements.json";
    fid=open(f,"r")
    #print "opening " + f
    dat=json.loads(fid.read())
    fid.close()
    #dat is a list each entry is a view
    #is view is a dict with a type, description and number of slabs. It also has results which is a list of dicts too. Each dict here is
    #a parameter and the thresholds it was thresholded at. It also has the volume results at this threshold
    
    #find the mismatch view and extract core
    found_CTP_1SLAB=bool(0)
    found_PWI_DWI=bool(0)
    found_ONLY_DWI=bool(0)
    found_CTP_2SLABS=bool(0)
    HypoperfusionIndex_slab1=-1
    HypoperfusionIndex_slab2=-1
    CBVIndex_slab1=-1
    CBVIndex_slab2=-1
    for cview in dat:
        if cview["Type"]=="MismatchView":
            if cview["Results"][0][0]["ParameterName"]=='CBF':
                found_CTP_1SLAB=1
                break
            if cview["Results"][0][0]["ParameterName"]=='ADC':
                found_PWI_DWI=1
                break
            
    try: 
        if dat[0]["NumberOfSlabs"]==2:
            found_CTP_2SLABS=1
    except:
        found_CTP_2SLABS=0
           
    if found_CTP_2SLABS:
        try:
            corevols=[[],[]]
            corevols_slab0=dat[0]['Results'][0][0]['Volumes']
            corevols_slab1=dat[0]['Results'][1][0]['Volumes']
            corevols[0].append(corevols_slab0[0])
            corevols[1].append(corevols_slab1[0])
            coretholds=dat[0]['Results'][0][0]['Thresholds']
            tmaxvolumes=[[],[]]
            tmaxvolumes_slab0=dat[1]['Results'][0]['Volumes']
            tmaxvolumes_slab1=dat[1]['Results'][1]['Volumes']
            tmaxvolumes[0].append(tmaxvolumes_slab0)
            tmaxvolumes[1].append(tmaxvolumes_slab1)            
            thresholds=dat[1]['Results'][0]['Thresholds']
            coremodal='CT'
            number_of_slabs=2
            try:    
                if dat[1]['Results'][0]['HypoperfusionIndexComputed']:
                    HypoperfusionIndex_slab1=dat[1]['Results'][0]['HypoperfusionIndex']
                else:
                    HypoperfusionIndex_slab1='NC'                
                    print("slab 1 HypoperfusionIndex is NC")
                    
            except:
                HypoperfusionIndex_slab1='HypoperfusionIndex error'
            
            try:        
                if  dat[1]['Results'][1]['HypoperfusionIndexComputed']:
                    HypoperfusionIndex_slab2=dat[1]['Results'][1]['HypoperfusionIndex']
                else:
                    HypoperfusionIndex_slab2='NC'                    
                    print("slab2 HypoperfusionIndex is NC")
            except:
                HypoperfusionIndex_slab2='HypoperfusionIndex error'       

            try:
                if dat[4]['Results'][0]['CBVIndexComputed'] :
                    CBVIndex_slab1=dat[4]['Results'][0]['CBVIndex']                    
                else:
                    CBVIndex_slab1='NC'
                    print("slab1 CBVIndex is NC")                      
            except:
                CBVIndex_slab1='CBVIndex error'
                
            try:        
                if  dat[4]['Results'][1]['CBVIndexComputed']:
                    CBVIndex_slab2=dat[4]['Results'][1]['CBVIndex']
                else:
                    CBVIndex_slab2='NC'
                    print("slab2 CBVIndex is NC")    
            except:
                CBVIndex_slab2='CBVIndex error'
                
            return {"returncode":0,"tmaxthresholds":thresholds,"tmaxvolumes":tmaxvolumes,"coremodal":coremodal,
            "corevolumes":corevols,"corethresholds":coretholds,"numberofslabs":number_of_slabs,"HypoperfusionIndex_slab1":HypoperfusionIndex_slab1,"CBVIndex_slab1":CBVIndex_slab1,"HypoperfusionIndex_slab2":HypoperfusionIndex_slab2,"CBVIndex_slab2":CBVIndex_slab2}
        except:
            print('Possibly AIF error')
            return get_no_voldict()
            
            
    try:
        if dat[0]["Type"]=="ThresholdedView":  
            if dat[0]["Results"][0]["ParameterName"]=='ADC':
                found_ONLY_DWI=1
    except:
        found_ONLY_DWI=0
            
             
    if found_ONLY_DWI:
        print('foundonlydwi')
        corevols=dat[0]["Results"][0]["Volumes"]
        coretholds=dat[0]["Results"][0]["Thresholds"]
        coremodal="MR"
        number_of_slabs=1
        HypoperfusionIndex='NA'
        
        return {"returncode":0,"tmaxthresholds":['NA','NA','NA','NA'],"tmaxvolumes":['NA','NA','NA','NA'],"coremodal":coremodal,"corevolumes":corevols,"corethresholds":coretholds,"numberofslabs":number_of_slabs,"HypoperfusionIndex_slab1":'NA',"CBVIndex_slab1":'NA',"HypoperfusionIndex_slab2":'NA',"CBVIndex_slab2":'NA'}
    
    if found_CTP_1SLAB or found_PWI_DWI:
        #figure out slab and MR variations here
        v1=cview["Results"][0][0]
        
        
        if v1['ParameterName']=='CBF':
            #find the CBF and store just that one
            corevols=v1["Volumes"]
            coretholds=v1["Thresholds"]
            #coreparam="CBF"
            coremodal="CT"
      
        
        if v1['ParameterName']=='ADC':
        #find the CBF and store just that one
            corevols=v1["Volumes"]
            coretholds=v1["Thresholds"]
        #coreparam="CBF"
            coremodal="MR" 
            
        
        #if  MMview was there, then go look for thold view    
        for cview in dat:   #now find the threshlded view
            if cview["Type"]=="ThresholdedView":
                if cview["Results"][0]["ParameterName"]=="Tmax":
                    found=1
                    break
                
        thresholds=dat[1]["Results"][0]["Thresholds"]
        tmaxvolumes=dat[1]["Results"][0]["Volumes"]
        number_of_slabs=1
        HypoperfusionIndex_slab2=-1
        CBVIndex_slab2=-1
        try:
            if dat[1]['Results'][0]['HypoperfusionIndexComputed'] :
                HypoperfusionIndex_slab1=[dat[1]['Results'][0]['HypoperfusionIndex']]
            else:
                HypoperfusionIndex_slab1=['NC']
                print("HypoperfusionIndex is NC")
    
            if dat[3]['Results'][0]['CBVIndexComputed'] :
                CBVIndex_slab1=[dat[3]['Results'][0]['CBVIndex']]
            else:
                CBVIndex_slab1=['NC']
                print("CBVIndex is NC")    
        except:
            try:
                if dat[1]['Results'][0]['HypoperfusionIndexComputed'] :
                    HypoperfusionIndex_slab1=dat[1]['Results'][0]['HypoperfusionIndex']
                else:
                    HypoperfusionIndex_slab1=['NC']
                    print("HypoperfusionIndex is NC")
        
                if dat[4]['Results'][0]['CBVIndexComputed'] :
                    CBVIndex_slab1=dat[4]['Results'][0]['CBVIndex']
                else:
                    CBVIndex_slab1=['NC']
                    print("CBVIndex is NC")   
            except:
                HypoperfusionIndex_slab1=['HypoperfusionIndex error']
                CBVIndex_slab1=['CBVIndex error']
                print("check HypoperfusionIndex and/or CBVIndex measurements json")
        
        return {"returncode":0,"tmaxthresholds":thresholds,"tmaxvolumes":tmaxvolumes,"coremodal":coremodal,
            "corevolumes":corevols,"corethresholds":coretholds,"numberofslabs":number_of_slabs,"HypoperfusionIndex_slab1":HypoperfusionIndex_slab1,"CBVIndex_slab1":CBVIndex_slab1,"HypoperfusionIndex_slab2":HypoperfusionIndex_slab2,"CBVIndex_slab2":CBVIndex_slab2}
    else:
        return get_no_voldict()
            
        
    
#r47=readJSON("/Volumes/DEFUSE3/CORELAB/rapid_processing/D3_R47_RANDOMIZED_FINAL/101/BL/Results_CTP_R47/measurements.json")
#r46=readJSON("/Users/amar/Desktop/testcases_stanfordcleanup/results_r46/100/BL/Results_PWI_DWI_R46/measurements.json")   
#r46=readJSON("/Users/amar/Desktop/testcases_stanfordcleanup/results_r46/102/FU/Results_only_DWI_R46/measurements.json") 
    #print json.dumps(dat,indent=4, separators=(',', ': '))
    