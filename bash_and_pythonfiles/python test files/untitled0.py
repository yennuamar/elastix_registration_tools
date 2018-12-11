#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 16:34:35 2017

@author: amar
"""
import sys
import random
import os

first_name="amarnath"
last_name=" yennu"
name=first_name+last_name
print("my name is %s" %(name))

a=10 ;b=20
print("a * b =", a**b)

matr=[[1,2,3],[2,3,4],[3,4,5]]
for x in range(0,3):
    for y in range(0,3):
        print("[%d][%d]=[%d]"%(x,y,matr[x][y]))
        
print(len(matr))

file = open(“testfile.txt”,”r+”) 
        