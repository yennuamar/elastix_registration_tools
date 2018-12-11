#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 15:50:50 2017

@author: amar
"""


import os
import pydicom
import glob
import shutil
import re
import subprocess
import time

def osexec(cmd):
    pid = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
    op = pid.communicate()
    #print pid.poll()
    return (op,pid.poll())

cmd1="pwd"
op1=osexec(cmd1)

files = []

start_dir = '/Users/amar/Desktop/test_rapid_exec'
pattern   = " "

for dir,_,_ in os.walk('/Users/amar/Desktop/test_rapid_exec'):
    files.extend(glob.glob(os.path.join(dir,''))) 
    

files1=[]
for i in range(len(files)):
    if (re.search('BL',files[i]) or re.search('FU',files[i])) and not re.search('CTP',files[i]) and not re.search('DWI',files[i]) and not re.search('PWI',files[i]) and not re.search('Results',files[i]):
        print(files[i])
        