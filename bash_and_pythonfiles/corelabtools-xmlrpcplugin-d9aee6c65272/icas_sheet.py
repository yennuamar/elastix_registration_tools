#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 09:30:49 2017

@author: sorenc
"""



from openpyxl import load_workbook

from datetime import datetime




def getSheet():
    wb = load_workbook(filename = '/Users/amar/Desktop/icas-labels-v3.1-Sept18.xlsx')
    ws= wb.get_sheet_by_name("data")

 
    p=0;
    mydict={}   #dict of header, list
    headerlist=[]
    for irow in ws.rows:
        if p==0:
            for icol in irow:
                mydict[icol.value]=[]   #init array for column
                headerlist.append(icol.value) #and remember the ordering
        else:
            ccolnum=0
            for icol in irow:
                mydict[headerlist[ccolnum]].append(icol.value)   #init array for column
                ccolnum=ccolnum+1    
        p=p+1

    return mydict



def getBLtimes():
     dat=getSheet()
     
     IDs=dat["StudyID"]
     datetime=dat["BLMRI"]
     
     mydatetime={}
     for k in range(len(datetime)):
         #print times[k]
         mydatetime[str(IDs[k])]=datetime[k]
    
     return mydatetime
     
 
def geteFUtimes():
     dat=getSheet()
     
     IDs=dat["studyNumber"]
     dates=dat["earlyFUmriObtainedDate"]
     times=dat["earlyFUmriObtainedTime"]
     mydatetime={}
     for k in range(len(dates)):
         #print times[k]
         if dates[k]:
             mydatetime[str(IDs[k])]=datetime.combine(datetime.date(dates[k]),times[k])
         else:
             mydatetime[str(IDs[k])]=None
             
             
     return mydatetime
         
def getlFUtimes():
     dat=getSheet()
     
     IDs=dat["studyNumber"]
     dates=dat["MRI5dObtainedDate"]
     times=dat["MRI5dObtainedTime"]
     mydatetime={}
     for k in range(len(dates)):
         #print times[k]
         if dates[k]:
             mydatetime[str(IDs[k])]=datetime.combine(datetime.date(dates[k]),times[k])
         else:
             mydatetime[str(IDs[k])]=None
             
     return mydatetime
             
     
if __name__ == "__main__":
      dt=getBLtimes()  