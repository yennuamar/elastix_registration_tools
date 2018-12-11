# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 13:54:24 2016

@author: sorenc
"""
import re
def get_indx(mylist,regex):
    #iterate list and get index of match
    #p = re.compile(regex)
    for m in mylist:
        if re.match(regex,m):
            return mylist.index(m)

    return -1