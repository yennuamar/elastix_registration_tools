#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 12:09:51 2017

@author: sorenc
"""

from osirixutils import *

import  xmlrpclib
import openpyxl
import re
import D2worksheet
from datetime import datetime, timedelta 
   # server = Server("http://171.65.168.30:8080",verbose=True)
#server = Server("http://172.25.169.28:8085",verbose=False)


#server = xmlrpclib.Server("http://172.25.169.28:8085",verbose=False)
#server = xmlrpclib.Server("http://192.168.0.10:8080",verbose=False)





server = xmlrpclib.Server("http://localhost:8080",verbose=False)

IDs=server.getPatientIDs( )


horos_has=set()


bltimes=D2worksheet.getBLtimes()

should_have=set(bltimes.keys())

for k in IDs:
    horos_has.add(k[0:5])
    


mustadd=should_have-horos_has