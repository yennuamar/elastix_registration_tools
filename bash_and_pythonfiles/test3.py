#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 11:06:10 2017

@author: amar


"""
import sys
import random
import os
import pydicom
import pylab
import numpy
import scipy
import matplotlib
import datetime
import subprocess




def osexec(cmd):
    pid = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
    op = pid.communicate()
    #print pid.poll()
    return (op,pid.poll())




def transferid_date_time(datetime_now):
    # cmd="ssh perf@172.25.169.28 \"psql -d rapid -U perfuser -c \"select rapid_transfer_id,transfer_date_time from mni_transfers where transfer_date_time >= \'2017-03-03 00:00:00.000000\' and transfer_date_time <= \'2017-03-04 00:00:00.000000\' \"\""
    cmd= "ssh perf@172.25.169.28 \"psql -t -d rapid -U perfuser -c \\\"select rapid_transfer_id from mni_transfers where transfer_date_time >= \'" + datetime_now + "\'::timestamp - interval \'10 days\' and transfer_date_time <= \'" + datetime_now+ "\'\\\" \" "
    print(cmd)
    op=osexec(cmd)
    return op

today = datetime.datetime.today()
today= today.replace(second=0, microsecond=00000)

op=transferid_date_time(str(today))
mystr=str(op[0][0])
myarray=mystr.split("\\n")

#psql -d rapid -U perfuser -c \"select * from mni_transfers\"\
print(myarray)

strippedarray=[]
for cstring in myarray:
    strippedarray.append( cstring.strip()  )
    
flag=strippedarray[0][len(strippedarray)-5:]
flag=flag.replace(' ','')
strippedarray[0]=flag

strippedarray1=strippedarray[0:len(strippedarray)-2][:]
with open("test4.txt", "wt") as out_file:
    out_file.write(str(strippedarray1))
    
#op=transferid_date_time()
#op
     
print(strippedarray1)