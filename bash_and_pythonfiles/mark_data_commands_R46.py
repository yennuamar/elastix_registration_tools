#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 19:45:09 2017

@author: amar
"""


import os

import glob
import shutil
import re
import subprocess


def osexec(cmd):
    pid = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
    op = pid.communicate()
    #print pid.poll()
    return (op,pid.poll())

cmd1="pwd"
op1=osexec(cmd1)

files = []

start_dir = '/Users/amar/Desktop/data_arrange3'
pattern   = " "

for dir,_,_ in os.walk('/Users/amar/Desktop/data_arrange3'):
    files.extend(glob.glob(os.path.join(dir,''))) 
    


for i in range(len(files)):
    if (re.search('BL',files[i]) or re.search('FU',files[i])) and not re.search('CTP',files[i]) and not re.search('DWI',files[i]) and not re.search('PWI',files[i]):
        files1=glob.glob(files[i] + '/*')
        dwi=0; pwi=0; ctp=0;
        for j in range(len(files1)):
            if re.search('DWI1',files1[j]):
                dwi = dwi + 1
                files2=glob.glob(files1[j] + '/*')
                if not os.path.isfile(files[i] + 'rapid_dwi.txt'):
                    with open(files[i] + 'rapid_dwi.txt', 'a') as f:
                        for k in range(len(files2)):
                            print( 'DWI1/' + os.path.basename(files2[k]), file=f)
                if dwi == 2:
                    with open(files[i] + 'rapid_dwi.txt', 'a') as f:
                        for k in range(len(files2)):
                            print('DWI2/' + os.path.basename(files2[k]), file=f)
            if re.search('PWI1',files1[j]):
                pwi = pwi + 1
                files2=glob.glob(files1[j] + '/*')
                if not os.path.isfile(files[i] + 'rapid_pwi.txt'):
                    with open(files[i] + 'rapid_pwi.txt', 'a') as f:
                        for k in range(len(files2)):
                            print('PWI1/' + os.path.basename(files2[k]), file=f)                
            if re.search('CTP',files1[j]):
                ctp = ctp + 1
                files2=glob.glob(files1[j] + '/*')
                if not os.path.isfile(files[i] + 'rapid_ctp1.txt'):
                    with open(files[i] + 'rapid_ctp1.txt', 'a') as f:
                        for k in range(len(files2)):
                            print('CTP1/' + os.path.basename(files2[k]), file=f)
        
                if ctp == 2:
                    if not os.path.isfile(files[i] + 'rapid_ctp2.txt'):
                        with open(files[i] + 'rapid_ctp2.txt', 'a') as f:
                            for k in range(len(files2)):
                                print('CTP2/' + os.path.basename(files2[k]), file=f)
                                
                with open(files[i] + 'rapid_ctp.txt', 'a') as f:
                    for k in range(len(files2)):
                        print('CTP' + str(ctp) + '/' + os.path.basename(files2[k]), file=f)                 
                
        if (dwi == 1) and (pwi == 1) and (ctp == 0):
            print('dwi plus pwi case')
            if not os.path.exists(files[i] + '/' + 'Results_PWI_DWI_R46'):
                os.makedirs(files[i] + '/' + 'Results_PWI_DWI_R46');
            if not os.path.isfile(files[i] + 'command1.txt'):
                with open(files[i] + 'command1.txt', 'w') as f:
                    print("/opt/rapid4/bin/perf_mismatch_prg -c /opt/rapid4/local/mismatch_params.json -dwi rapid_dwi.txt -perf rapid_pwi.txt -od Results_PWI_DWI_R46/" + " > Results_PWI_DWI_R46/rapid_processing.log.txt 2>&1", file=f)            
          
        if (dwi == 1) and (pwi == 0) and (ctp == 1):
            print('dwi plus ctp case')
            if not os.path.exists(files[i] + '/' + 'Results_only_DWI_R46'):
                os.makedirs(files[i] + '/' + 'Results_only_DWI_R46');
            if not os.path.exists(files[i] + '/' + 'Results_CTP_R46'):
                os.makedirs(files[i] + '/' + 'Results_CTP_R46');
            if not os.path.isfile(files[i] + 'command1.txt'):
                with open(files[i] + 'command1.txt', 'w') as f:
                    print("/opt/rapid4/bin/perf_mismatch_prg  -c /opt/rapid4/local/mismatch_params.json -dwi rapid_dwi.txt -od Results_only_DWI_R46/" + " > Results_only_DWI_R46/rapid_processing.log.txt 2>&1", file=f)
                    print("/opt/rapid4/bin/perf_mismatch_prg  -c /opt/rapid4/local/mismatch_params.json -perf rapid_ctp1.txt -od Results_CTP_R46/"  + " > Results_CTP_R46/rapid_processing.log.txt 2>&1", file=f)  
        
        
        if (dwi == 0) and (pwi == 0) and (ctp == 2):
            print('2 slab ctp')
            if not os.path.exists(files[i] + '/' + 'Results_CTP_2SLABS_R46'):
                os.makedirs(files[i] + '/' + 'Results_CTP_2SLABS_R46');
            if not os.path.isfile(files[i] + 'command1.txt'):
                with open(files[i] + 'command1.txt', 'w') as f:
                    print("/opt/rapid4/bin/perf_mismatch_prg  -c /opt/rapid4/local/mismatch_params.json -perf rapid_ctp1.txt -perf rapid_ctp2.txt -od Results_CTP_2SLABS_R46/"  + " > Results_CTP_2SLABS_R46/rapid_processing.log.txt 2>&1", file=f)              
        if (dwi == 1) and (pwi == 0) and (ctp == 0):
            print('only dwi')
            if not os.path.exists(files[i] + '/' + 'Results_only_DWI_R46'):
                os.makedirs(files[i] + '/' + 'Results_only_DWI_R46');
            if not os.path.isfile(files[i] + 'command1.txt'):
                with open(files[i] + 'command1.txt', 'w') as f:
                    print("/opt/rapid4/bin/perf_mismatch_prg  -c /opt/rapid4/local/mismatch_params.json -dwi rapid_dwi.txt -od Results_only_DWI_R46/"  + " > Results_only_DWI_R46/rapid_processing.log.txt 2>&1", file=f)                   
        
        if (dwi == 0) and (pwi == 0) and (ctp == 1):
            print('only ctp')
            if not os.path.exists(files[i] + '/' + 'Results_CTP_R46'):
                os.makedirs(files[i] + '/' + 'Results_CTP_R46');
            if not os.path.isfile(files[i] + 'command1.txt'):
                with open(files[i] + 'command1.txt', 'w') as f:
                    print("/opt/rapid4/bin/perf_mismatch_prg  -c /opt/rapid4/local/mismatch_params.json -perf rapid_ctp1.txt -od Results_CTP_R46/"  + " > Results_CTP_R46/rapid_processing.log.txt 2>&1", file=f)  
        if (ctp > 2):
            print('multiple ctp')
            if not os.path.exists(files[i] + '/' + 'Results_MCTP_R46'):
                os.makedirs(files[i] + '/' + 'Results_MCTP_R46');
            if not os.path.isfile(files[i] + 'command1.txt'):
                with open(files[i] + 'command1.txt', 'w') as f:
                    print("/opt/rapid4/bin/perf_mismatch_prg  -c /opt/rapid4/local/mismatch_params.json -perf rapid_ctp.txt -od Results_MCTP_R46/"  + " > Results_MCTP_R46/rapid_processing.log.txt 2>&1", file=f)           
        
                
            
        
        
    