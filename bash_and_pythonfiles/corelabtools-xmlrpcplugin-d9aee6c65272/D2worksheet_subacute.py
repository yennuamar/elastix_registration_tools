#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 14:13:08 2017

@author: sorenc
"""


from openpyxl import load_workbook

from datetime import datetime




def getSheet():
    wb = load_workbook(filename = 'D2_early_day5_MRA.xlsx')
    ws= wb.get_sheet_by_name("Sheet1")

 
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


def cases_with_lateMRA():
     dat=getSheet()
     
     IDs=dat["studyNumber"]
     followup5Day_mracow=dat["followup5Day_mracow"]
     cohortType=dat["cohortType"]
     cases=[]
     count=0
     for z in cohortType:
         if z=="case":
             count=count+1
     
     for k in range(len(followup5Day_mracow)):
         #print times[k]
         if followup5Day_mracow[k]=="Yes" and cohortType[k]=="case":
             cases.append(IDs[k])
             
     return cases
             
     
         
def cases_with_earlyMRA():
     dat=getSheet()
     
     IDs=dat["studyNumber"]
     followupEarly_mracow=dat["followupEarly_mracow"]
     cohortType=dat["cohortType"]
     cases=[]
     for k in range(len(followupEarly_mracow)):
         #print times[k]
         if followupEarly_mracow[k]=="Yes" and cohortType[k]=="case":
             cases.append(IDs[k])
             
     return cases
             
     
if __name__ == "__main__":
      earlyMRA=cases_with_earlyMRA()
      lateMRA=cases_with_lateMRA()