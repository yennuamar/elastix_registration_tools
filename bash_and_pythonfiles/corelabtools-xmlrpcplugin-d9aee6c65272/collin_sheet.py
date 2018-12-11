#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 23:06:40 2017

@author: sorenc
"""



from openpyxl import load_workbook

from datetime import datetime




def getSheet():
    wb = load_workbook(filename = 'ptlist_collin.xlsx')
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
                #print icol.value
                mydict[headerlist[ccolnum]].append(str(icol.value))  #init array for column
                ccolnum=ccolnum+1    
        p=p+1

    return (mydict,headerlist)



    

     
if __name__ == "__main__":
      sh=getSheet() 