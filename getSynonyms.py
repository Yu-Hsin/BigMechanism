#!/usr/bin/env python 
import sys



if __name__ == "__main__":
  locFn = open(sys.argv[1])
  locFn.readline()
  locFn.readline()

  while (True):
    end = False
    locAbbrev = ""
    for i in range(5):
        line = locFn.readline()
        if not line or len(line) <= 2:
           end = True
           break
        if i == 0:
	   line = line.rstrip().replace("\""," ").split()
	   locAbbrev = line[0]
	if i == 3:
	   if "synonyms" not in line:
	      print locAbbrev, "\t", locAbbrev
	      continue
	   start = line.find("[")
	   endpos = line.find("]")

	   if start == -1:
	      line = line.rstrip().replace("\"","").replace(",","")
	      linearr = line.split()
	      for i in range(len(linearr)):
		  if linearr[i] == "synonyms":
		     print locAbbrev, "\t", linearr[i+2]
	   else:
	      tmp_String =  line[start+2:endpos-1]
	      tmp_String = tmp_String.replace("\"","").replace(", ",",").split(",")
	      print locAbbrev, "\t", ", ".join(tmp_String)

    if end:
       break    
