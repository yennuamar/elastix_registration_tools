#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 14:13:08 2017

@author: sorenc
"""


from openpyxl import load_workbook

from datetime import datetime




def getSheet():
    wb = load_workbook(filename = 'DAWN.xlsx')
    ws= wb.get_sheet_by_name("TIMES")

 
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


def getVar(colname):   #delivers colname keyed by ID
    dat=getSheet()
     
    IDs_tmp=dat["SubjectNumber"]
    var_tmp=dat[colname]
    retval={}
     
    merge=zip(IDs_tmp,var_tmp)
    
    for cID,val in merge:
        if cID:  
            retval[str(cID)]=    val      
        else:
            break
    
    
    return retval
             

def getIDs():
    IDs=getVar("SubjectNumber")
    return sorted(IDs.keys())
     
def getCoreTimes():
    ID_times= getVar("ACCORETIME")
  
    for cID in ID_times.keys():
        ctime=datetime.strptime(str(ID_times[cID]).strip(),'%Y%m%d %H:%M')
        ID_times[cID]=ctime
             
              
    return ID_times
     
if __name__ == "__main__":
      IDs=getIDs()
      times=getCoreTimes()