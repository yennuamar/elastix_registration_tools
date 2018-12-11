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
import numpy as np
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
    cmd1= "ssh perf@172.25.169.28 \"psql -t -d rapid -U perfuser -c \\\"select rapid_transfer_id from mni_transfers where transfer_date_time >= \'" + datetime_now + "\'::timestamp - interval \'4 days\' and transfer_date_time <= \'" + datetime_now+ "\'\\\" \" "
   # print(cmd1)
    op1=osexec(cmd1)
    return op1



today = datetime.datetime.today()
today= today.replace(second=0, microsecond=00000)

op1=transferid_date_time(str(today))
mystr1=str(op1[0][0])
myarray1=mystr1.split("\\n")
strippedarray1=[]
for cstring in myarray1:
    strippedarray1.append( cstring.strip()  )
    
flag1=strippedarray1[0][3:]
flag1=flag1.replace(' ','')
strippedarray1[0]=flag1

strippedarray1=strippedarray1[0:len(strippedarray1)-2][:]
with open("rapid_tr_ids.txt", "wt") as out_file:
    out_file.write(str(strippedarray1))
    
#for i in range(0,len(strippedarray1)):
#    print(strippedarray1[i])

 
cmd2= "ssh perf@172.25.169.28 \"psql -t -d rapid -U perfuser -c \\\"select rapid_transfer_id from mni_instance order by last_modified asc \\\" \" "
op2=osexec(cmd2)
mystr2=str(op2[0][0])
myarray2=mystr2.split("\\n")

strippedarray2=[]
for cstring in myarray2:
    strippedarray2.append( cstring.strip()  )
    
flag2=strippedarray2[0][3:]
flag2=flag2.replace(' ','')
strippedarray2[0]=flag2

strippedarray2=strippedarray2[0:len(strippedarray2)-2]
with open("rapid_tr_ids_instance.txt", "wt") as out_file:
    out_file.write(str(strippedarray2))
    

#for i in range(0,len(strippedarray2)):
#    print(strippedarray2[i])
    
cmd3= "ssh perf@172.25.169.28 \"psql -t -d rapid -U perfuser -c \\\"select rapid_series_id from mni_instance order by last_modified asc\\\" \" "
op3=osexec(cmd3)
mystr3=str(op3[0][0])
myarray3=mystr3.split("\\n")

strippedarray3=[]
for cstring in myarray3:
    strippedarray3.append( cstring.strip()  )
    
flag3=strippedarray3[0][3:]
flag3=flag3.replace(' ','')
strippedarray3[0]=flag3

strippedarray3=strippedarray3[0:len(strippedarray3)-2]
with open("rapid_sr_ids_instance.txt", "wt") as out_file:
    out_file.write(str(strippedarray3))
    

#for i in range(0,len(strippedarray3)):
#    print(strippedarray3[i])  
#    
cmd4= "ssh perf@172.25.169.28 \"psql -t -d rapid -U perfuser -c \\\"select num_frames from mni_instance order by last_modified asc \\\" \" "
op4=osexec(cmd4)
mystr4=str(op4[0][0])
myarray4=mystr4.split("\\n")

strippedarray4=[]
for cstring in myarray4:
    strippedarray4.append( cstring.strip()  )
    
flag4=strippedarray4[0][3:]
flag4=flag4.replace(' ','')
strippedarray4[0]=flag4

strippedarray4=strippedarray4[0:len(strippedarray4)-2]
with open("num_frames_instance.txt", "wt") as out_file:
    out_file.write(str(strippedarray4))
    

#for i in range(0,len(strippedarray1)):
#    for j in range(0,len(strippedarray2)):
#        if strippedarray1[i]==strippedarray2[j]:
            

def remove_redun(seq): 
   # order preserving
   noDupes = []
   [noDupes.append(i) for i in seq if not noDupes.count(i)]
   return noDupes


#for i in range(0,len(strippedarray4)):
#    print(strippedarray4[i])  
unique_transfer_ids=remove_redun(strippedarray1) 
unique_series_ids= remove_redun(strippedarray3) 
num_of_files =0
num_of_tr_ids=[]
for i in range(0,len(strippedarray1)):
    for j in range(0,len(strippedarray2)):
        if strippedarray1[i]==strippedarray2[j]:
            num_of_files=num_of_files+1
    
    num_of_tr_ids.insert(i,num_of_files)
    num_of_files=0


#print(num_of_tr_ids)                          
num_of_files=0
for i in range(len(num_of_tr_ids)):
    num_of_files =num_of_files +int(num_of_tr_ids[i])
    
total_files=num_of_files
#print(num_of_files)
    
#with open("test5.txt", "rt") as in_file:
#    text= in_file.read()
#
#print(text)
num_files_series =0
num_of_se_ids=[]
num_frames_series=0
num_of_frame_se=[]
for i in range(0,len(unique_series_ids)):
    for j in range(0,len(strippedarray3)):
        if unique_series_ids[i]==strippedarray3[j]:
            num_files_series=num_files_series+1
            num_frames_series=num_frames_series+int(strippedarray4[j])
    num_of_se_ids.insert(i,num_files_series)
    num_of_frame_se.insert(i,num_frames_series)
    num_files_series =0
    num_frames_series=0
print('Unique Rapid transfer IDs')

print(unique_transfer_ids)
print('\nNumer of files in each Rapid transfer ID')
print(num_of_tr_ids) 
print('\ntotal number of files')
print(total_files)
print('\nUnique series IDs')
print(unique_series_ids)    
print('\nNumber of files in each series ID')
print(num_of_se_ids)
print('\nNumber of frames in each series ID')
print(num_of_frame_se) 
#num_of_files=0
#for i in range(0,len(num_of_se_ids)):
#    num_of_files=num_of_files+int(num_of_se_ids[i])
#    
#print(num_of_files)
    
cmd5= "ssh perf@172.25.169.28 \"psql -t -d rapid -U perfuser -c \\\"select rapid_series_id from mni_series order by last_modified asc \\\" \" "
op5=osexec(cmd5)
mystr5=str(op5[0][0])
myarray5=mystr5.split("\\n")

strippedarray5=[]
for cstring in myarray5:
    strippedarray5.append( cstring.strip()  )
    
flag5=strippedarray5[0][3:]
flag5=flag5.replace(' ','')
strippedarray5[0]=flag5

strippedarray5=strippedarray5[0:len(strippedarray5)-2]
with open("series_ids.txt", "wt") as out_file:
    out_file.write(str(strippedarray5))

cmd6= "ssh perf@172.25.169.28 \"psql -t -d rapid -U perfuser -c \\\"select series_description from mni_series order by last_modified asc \\\" \" "
op6=osexec(cmd6)
mystr6=str(op6[0][0])
myarray6=mystr6.split("\\n")

strippedarray6=[]
for cstring in myarray6:
    strippedarray6.append( cstring.strip()  )
    
flag6=strippedarray6[0][3:]
flag6=flag6.replace(' ','')
strippedarray6[0]=flag6

strippedarray6=strippedarray6[0:len(strippedarray6)-2]
with open("series_descrip.txt", "wt") as out_file:
    out_file.write(str(strippedarray6))


#print(strippedarray5)
#print(strippedarray6)

series_des_of_unique_series_ids=[]
for i in range(0,len(unique_series_ids)):
    for j in range(0,len(strippedarray5)):
        if unique_series_ids[i]==strippedarray5[j]:
            series_des_of_unique_series_ids.insert(i,strippedarray6[j])
            print(series_des_of_unique_series_ids[i])


