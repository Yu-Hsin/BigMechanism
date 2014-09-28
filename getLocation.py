#!/usr/bin/env python 
import sys



if __name__ == "__main__":
  locFn = open(sys.argv[1])
  locFn.readline()
  locFn.readline()

  while (True):
    end = False
    locAbbrev = ""
    locDef = ""
    for i in range(5):
        line = locFn.readline()
        if not line or len(line) == 2:
           end = True
           break
        if i == 0:
	   line = line.rstrip().replace("\""," ").split()
	   locAbbrev = line[0]
	   print locAbbrev
	   

    if end:
       break    
