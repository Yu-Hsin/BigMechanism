#!/usr/bin/env python
import sys


def get_relation (fn):
    
    f1 = open(fn)
    f1.readline() # read dummy line

    total = 0
    relocation_type = 0
    modification_changed_type = 0
    trans_modif_changed_type = 0
    synthesis_type = 0
    only_control_type = 0
    binding_type = 0
    binding_more_type = 0
    binding_less_type = 0
    multiple_translocation_type = 0
    multiple_trans_mod_changed_type = 0
    unbiding_type = 0

    while (True):
	total += 1
	end = False
	consumed =[]
	produced =[]
	controls =[]
	for i in range(11):
            line = f1.readline()
	    if not line:
	       end = True
	       break

	    if   i == 3: #consumed
		consumed = get_component(line)
	    elif i == 4: #produced
		produced = get_component(line)
	    elif i == 5: #controls
		contorls = get_component(line)

	relation = get_type(consumed, produced, contorls) 

	if relation == "translocation":
	    relocation_type += 1
	elif relation == "modification_changed":
	    modification_changed_type += 1
	elif relation == "trans_modif_changed":
	    trans_modif_changed_type += 1
	elif relation == "synthesis":
	    synthesis_type += 1
	elif relation == "only_controls":
	    only_control_type += 1
	elif relation == "binding":
	    binding_type += 1
	elif relation == "binding_more":
	    binding_more_type += 1
	elif relation == "binding_less":
	    binding_less_type += 1
        elif relation == "multiple_translocation":
	    multiple_translocation_type += 1
	elif relation == "multiple_translocation_modification_changed":
            multiple_trans_mod_changed_type += 1
	elif relation == "unbiding":
	    unbiding_type += 1
	
	if end:
	   break
#print total

    print "Translocation:", relocation_type
    print "Modification-type Changed:", modification_changed_type
    print "Translocation + Modfication-type Changed:", trans_modif_changed_type
    print "Synthesis:", synthesis_type
    print "Only Control:", only_control_type
    print "Binding:", binding_type
    print "Binding (more):", binding_more_type
    print "Binding (less):", binding_less_type
    print "Translocation (Multiple instances):", multiple_translocation_type
    print "Translocation + Modifcation-type Changed (Multiple instances):", multiple_trans_mod_changed_type
    print "Unbinding:", unbiding_type

#print relocation_type + modification_changed_type + trans_modif_changed_type + synthesis_type + only_control_type + binding_type + binding_more_type + binding_less_type + multiple_translocation_type + multiple_trans_mod_changed_type + unbiding_type
def get_component (line):
    line = line.replace("\"","").replace(",","")
    line = line.rstrip().split()
    if line[3] == "[":
	return []
    else:
	return line[3:-1]

def get_type (consumed, produced, controls):
    
    if len(consumed) == 1 and len(produced) == 1: # check translocation or modification changed
       con_arr = consumed[0].split("@")
       pro_arr = produced[0].split("@")
       if con_arr[0] == pro_arr[0] and con_arr[1] != pro_arr[1]: # translocation
	  return "translocation"
       elif con_arr[0] != pro_arr[0] and con_arr[1] == pro_arr[1]: # modification_changed
	  return "modification_changed"
       elif con_arr[0] != pro_arr[0] and con_arr[1] != pro_arr[1]: # translocation + modification_changed
          print "================"
          print consumed
	  print produced
	  print controls
	  print "========"

	  return "trans_modif_changed"
     
    if len(consumed) == 0 and len(produced) != 0:
       return "synthesis"

    if len(consumed) == 0 and len(produced) == 0: 
       return "only_controls"


    if len(consumed) > len(produced): # binding_type (might include the change of modification type TODO)
       con_element = []
       pro_element = []


       for entry in consumed:
	   protein = entry.split("@")[0]
	   words = protein.split(":")
	   for word in words:
	       if "-" in word:
	          word = word [0:word.find("-")]
	       con_element.append(word)
	   
       for entry in produced:
	   protein = entry.split("@")[0]
	   words = protein.split(":")
	   for word in words:
               if "-" in word:
	          word = word[0:word.find("-")]
	       pro_element.append(word)

       if sorted(con_element) == sorted(pro_element):
	  return "binding"
       elif len(con_element) < len (pro_element):
	  return "binding_more"
       elif len(con_element) > len (pro_element):
	  return "binding_less"
    
    if len(consumed) < len(produced): # split might change location TODO
       con_element = [] 
       pro_element = [] 
       for entry in consumed:
	   protein = entry.split("@")[0]
	   words = protein.split(":")
	   for word in words:
	       if "-" in word:
	           word = word [0:word.find("-")]
	       con_element.append(word)

       for entry in produced:
           protein = entry.split("@")[0]
	   words = protein.split(":")
	   for word in words:
               if "-" in word:
	          word = word[0:word.find("-")]
	       pro_element.append(word)

       if sorted(con_element) == sorted (pro_element):
	  
	  return "unbiding"
    

    if len(consumed) == len(produced): #multiple modification_changed or multiple translocation
       con_element = []
       pro_element = []
       con1_element = []
       pro1_element = []
      
       for entry in consumed:
           con_element.append(entry.split("@")[0])
	   con1_element.append(entry.split("@")[1])

       for entry in produced:
           pro_element.append(entry.split("@")[0])
	   pro1_element.append(entry.split("@")[1])

       if sorted(con_element) == sorted(pro_element):
	  return "multiple_translocation"
       else:
	  return "multiple_translocation_modification_changed"

if __name__ == "__main__":
   get_relation(sys.argv[1])


