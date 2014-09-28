#!/usr/bin/env python
import sys

count_Loc_From = {}
count_Loc_To = {}
count_Pair = {}
count_Modi_From ={}
count_Modi_To ={}

def get_relation (fn, locmapping):
    
    mapping = {}
    for line in open(locmapping):
	line = line.rstrip().split()
	mapping[line[0]] = line[1]

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

	relation = get_type(consumed, produced, contorls, mapping) 

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

    '''
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
    '''
    '''
    print count_Loc_From
    print count_Loc_To
    print count_Pair
    '''
    
    a = [(v,k) for k, v, in count_Modi_From.iteritems()]
    b = [(v,k) for k, v, in count_Modi_To.iteritems()]
    a.sort();
    b.sort()
    for v, k in a:
        print v, k 
    print "============"
    for v, k in b:
	print v, k
    '''   
    print count_Modi_From
    print count_Modi_To
    '''

#print relocation_type + modification_changed_type + trans_modif_changed_type + synthesis_type + only_control_type + binding_type + binding_more_type + binding_less_type + multiple_translocation_type + multiple_trans_mod_changed_type + unbiding_type
def get_component (line):
    line = line.replace("\"","").replace(",","")
    line = line.rstrip().split()
    if line[3] == "[":
	return []
    else:
	return line[3:-1]

def get_type (consumed, produced, controls, mapping):
    
    if len(consumed) == 1 and len(produced) == 1: # check translocation or modification changed
       con_arr = consumed[0].split("@")
       pro_arr = produced[0].split("@")
       if con_arr[0] == pro_arr[0] and con_arr[1] != pro_arr[1]: # translocation
          fromLoc = mapping[con_arr[1]]
	  toLoc = mapping[pro_arr[1]]
	  pairLoc = fromLoc + " to " + toLoc
	  
	  if fromLoc not in count_Loc_From:
	     count_Loc_From[fromLoc] = 1
	  else:
	     count_Loc_From[fromLoc] += 1
	  
	  if toLoc not in count_Loc_To:
	     count_Loc_To[toLoc] = 1
	  else:
	     count_Loc_To[toLoc] += 1

	  if pairLoc not in count_Pair:
	     count_Pair[pairLoc] = 1
	  else:
	     count_Pair[pairLoc] += 1

	  return "translocation"
       elif con_arr[0] != pro_arr[0] and con_arr[1] == pro_arr[1]: # modification_changed
          con = con_arr[0].split("-")
	  pro = pro_arr[0].split("-")
	  con = " ".join(con [1:])
	  pro = " ".join(pro [1:])
	  if len(con) == 0:
	     con = "empty"
	  if len(pro) == 0:
	     pro = "empty"

          if con not in count_Modi_From:
	     count_Modi_From[con] = 1
	  else:
	     count_Modi_From[con] += 1

	  if pro not in count_Modi_To:
	     count_Modi_To[pro] = 1
	  else:
	     count_Modi_To[pro] += 1

	  return "modification_changed"
       elif con_arr[0] != pro_arr[0] and con_arr[1] != pro_arr[1]: # translocation + modification_changed
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
#get_relation(sys.argv[1])
    get_relation(sys.argv[1], sys.argv[2]) # rules.json, locMapping


