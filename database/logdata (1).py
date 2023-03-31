#README:
#Sometimes the code will extract other info from .log file
#so make sure you look over the dat.csv file generated to fix
#the data

import sys
import re
import glob
import os

current= os.getcwd()
log=glob.glob('*.log')
opennew = open('data.csv','w')
#add what to check for
check= ["HF","RMSD","RMSF","Dipole"]
for x in log:
  newline=""
  start1=0
  opennew.write('{},'.format(x[0:len(x)-5]))
  openold = open(x, 'r')
  lines= openold.readlines()
  for i in range (len(lines)):
    if "The archive entry for this job was punched." in lines[i]:
      start= i-4
  for k in range (start-1500,start):   
    if "Alpha virt. eigenvalues" in lines[k]:
      start1= k-1
      break
  read= lines[start1]
  read= read.replace("\n","")
  read = read.split("--")
  read = read[1]
  read = read.split("  ")
  opennew.write('{},'.format(read[len(read)-1]))
  start1 = start1 + 1
  read = lines[start1]
  read= read.replace("\n","")
  read = read.split("--")
  read = read[1]
  read = read.split("  ")
  opennew.write('{},'.format(read[1]))
  for j in range (start, len(lines)):
    newline= str(newline) + lines[j]
  newline= newline.replace("\n","")
  newline= newline.replace(" ","")
  stop="\\"
  split= newline.split(stop) 
  for prop in check:  
    for idx in split:
      if prop in idx:
        res=""
        res= idx[len(prop)+1:len(idx)]
        opennew.write('{},'.format(res))
        continue
  opennew.write('\n')
  openold.close()
opennew.close()
