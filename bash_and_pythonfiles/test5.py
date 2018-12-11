
#!/usr/bin/python

#@author: amar
 
 
import sys
import random
import os
import datetime
import subprocess


def osexec(cmd):
    pid = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
    op = pid.communicate()
    #print pid.poll()
    return (op,pid.poll())
 

def transferid_date_time(datetime_now):
    cmd0="echo " + datetime_now  + " >>  /home/perf/logfile.txt"
    cmd1= "psql  -d rapid -U perfuser -c \"select * from (select  mni_instance.rapid_patient_id,series_description, input_port, calling_aetitle, transfer_date_time, series_date_time, count(*) from mni_transfers inner join mni_instance using (rapid_transfer_id) inner join mni_series using (rapid_series_id) group by rapid_series_id, series_description, called_aetitle, calling_aetitle,rapid_transfer_id, series_date_time, transfer_date_time,mni_instance.rapid_patient_id,input_port order by rapid_series_id ) as tmp where transfer_date_time >= \'" + datetime_now + "\'::timestamp - interval \'5 days \' and transfer_date_time <= \'" + datetime_now+ "\'   \"  "
    osexec(cmd0)

    op1=osexec(cmd1)
    if  op1[0][0]:
        #print op1[0][0]
        fid=open('logfile.txt','a')
        fid.write(op1[0][0])
        fid.close()

    print('cmd1')      
    

now = datetime.datetime.today()
now= now.replace(second=0, microsecond=00000)
transferid_date_time(str(now))
print(op1)