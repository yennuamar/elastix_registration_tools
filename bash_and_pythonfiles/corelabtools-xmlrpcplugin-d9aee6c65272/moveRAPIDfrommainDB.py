#!/usr/bin/env pyth
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 22:06:00 2017

@author: sorenc
"""

import  xmlrpclib
import openpyxl
import re

from datetime import datetime, timedelta 
import os
server = xmlrpclib.Server("http://171.65.168.30:8080",verbose=False)


IDs=server.GetPatientIDs()