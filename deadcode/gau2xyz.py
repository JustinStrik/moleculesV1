#!/usr/bin/env python3
## Rangsiman Ketkaew
## https://github.com/rangsimanketkaew/compchem
##
## -------------------------Usage-------------------------
##  $ chmod +x gau2xyz.py
##  $ python3 gau2xyz.py Gaussian_output.log
## -------------------------------------------------------

#ORIGINAL CODE, UPDATED IN GAUSSIAN.PY!

import sys
import re
import numpy
import os
import subprocess
import glob

start = 0
end = 0
current = os.getcwd()
subfolders = glob.glob('*.log')
for foldername in subfolders:
  filename = str(foldername[0:len(foldername)-4]) + ".log"
  newfile = str(filename[0:len(filename)-4]) + "_opt.xyz"
  print(os.getcwd())
 
  openold = open(filename,"r")
  opennew = open(newfile,"w")

  rline = openold.readlines()
  for i in range (len(rline)):
    if "Standard orientation:" in rline[i]:
      start = i
  for m in range (start + 5, len(rline)):
    if "---" in rline[m]:
      end = m
      break
  natom = end-start-5

  print(natom,file=opennew)
  print("   ",file=opennew)

## Convert to Cartesian coordinates format
## convert atomic number to atomic symbol
  for line in rline[start + 5 : end]:
    words = line.split()
    word1 = int(words[1])
    word3 = str(words[3])
    if   word1 ==   1 : word1 = "H"
    elif word1 ==   2 : word1 = "He"
    elif word1 ==   3 : word1 = "Li"
    elif word1 ==   4 : word1 = "Be"
    elif word1 ==   5 : word1 = "B"
    elif word1 ==   6 : word1 = "C"
    elif word1 ==   7 : word1 = "N"
    elif word1 ==   8 : word1 = "O"
    elif word1 ==   9 : word1 = "F"
    elif word1 ==  10 : word1 = "Ne"
    elif word1 ==  11 : word1 = "Na"
    elif word1 ==  12 : word1 = "Mg"
    elif word1 ==  13 : word1 = "Al"
    elif word1 ==  14 : word1 = "Si"
    elif word1 ==  15 : word1 = "P"
    elif word1 ==  16 : word1 = "S"
    elif word1 ==  17 : word1 = "Cl"
    elif word1 ==  18 : word1 = "Ar"
    elif word1 ==  19 : word1 = "K"
    elif word1 ==  20 : word1 = "Ca"
    elif word1 ==  21 : word1 = "Sc"
    elif word1 ==  22 : word1 = "Ti"
    elif word1 ==  23 : word1 = "V"
    elif word1 ==  24 : word1 = "Cr"
    elif word1 ==  25 : word1 = "Mn"
    elif word1 ==  26 : word1 = "Fe"
    elif word1 ==  27 : word1 = "Co"
    elif word1 ==  28 : word1 = "Ni"
    elif word1 ==  29 : word1 = "Cu"
    elif word1 ==  30 : word1 = "Zn"
    elif word1 ==  31 : word1 = "Ga"
    elif word1 ==  32 : word1 = "Ge"
    elif word1 ==  33 : word1 = "As"
    elif word1 ==  34 : word1 = "Se"
    elif word1 ==  35 : word1 = "Br"
    elif word1 ==  36 : word1 = "Kr"
    elif word1 ==  37 : word1 = "Rb"
    elif word1 ==  38 : word1 = "Sr"
    elif word1 ==  39 : word1 = "Y"
## copy from atom list.
    print("%s%s" % (word1,line[30:-1]), file=opennew)

  openold.close()
  opennew.close()
  optname = str(filename[0:len(filename)-4])
  os.system('cp {}_opt.xyz ../optfile'.format(optname)) 

print("#"*10 + " Done " + "#"*10)
