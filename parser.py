import os, sys
import xml.etree.cElementTree as ET
import re
from collections import OrderedDict
import json
import string
import StringIO

printable = set(string.printable)

## Reader: ToDo: use another file reader.py to import various formats, convert to txt and clean docs, here, below
def read_document(filepath):
    f = open(filepath)
    #with open(filepath, 'rb') as f:
    raw = f.read()
    raw=raw.upper()
    raw=raw.replace('EDUCATION','EDUCATION:',10)
    raw=raw.replace('SKILLS','SKILLS:',10)
    raw=raw.replace('SUMMARY','SUMMARY:',10)
    raw=raw.replace('EXPERIENCE','EXPERIENCE:',10)
    raw=raw.replace('::',':',10)
    f.close()
    return raw

### Extraction Methods, called by string "name" as specified in config

# Regex based single value extractor
def univalue_extractor( document, section, subterms_dict, parsed_items_dict ):
    retval = OrderedDict()
    get_section_lines = parsed_items_dict["Sections"].get(section)
    if get_section_lines is not None:
    	section_doc = "\n".join(get_section_lines)
    	if section_doc != "NA":
        	for node_tag, pattern_list in subterms_dict.items():
            		for pattern in pattern_list:
                		regex_pattern = re.compile(r"{}".format(pattern))
                		match = regex_pattern.search(section_doc)
                		if match != None and len(match.groups()) > 0 and match.group(1) != "":
                    			retval[node_tag] = match.group(1)
                    		break
    	return retval

# Section Information value extractor
def section_value_extractor_1( document, section, subterms_dict, parsed_items_dict ):
    retval = OrderedDict()
    #print("Section is",section)
    #print("parsed_items_dict is",parsed_items_dict)
    #print("subterms_dict is ",parsed_items_dict)    
    single_section_lines = parsed_items_dict["Sections"].get(section)
    #print("Hwellll  Before :::single_section_lines    :",single_section_lines)
    
    if single_section_lines is not None:
       #print("after arman single_section_lines    :",single_section_lines)
       #print("Section is ",section)
       for line in single_section_lines:
           #print("Line is  ::::: ",line)
           for node_tag, pattern_string in subterms_dict.items():
               pattern_list = re.split(r",|:", pattern_string[0])
               matches = [pattern for pattern in pattern_list if pattern in line]
               if len(matches):
                   #print("Matches is ",matches)
                   info_string = ", ".join(list(matches)) + " "
                   #print("Info string is ",info_string)
                   numeric_values = re.findall(r"([\d']{4})\s?-?(\d{2}[^\w+])?", line)
                   #print("Numberic Value",numeric_values)
                   if len(numeric_values):
                       value_list = list(numeric_values[0])
                       #print("Value list is",value_list)
                       info_string = info_string + "-".join([value for value in value_list if value != ""])
                   retval[node_tag] = info_string
                   break
       return retval

def section_value_extractor_2(document, section, subterms_dict, parsed_items_dict):
    #retval = []
    retval = OrderedDict()
    single_exp_lines = parsed_items_dict["Sections"].get(section)
    if single_exp_lines is not None:

        l = len(single_exp_lines)
        for i,line in enumerate(single_exp_lines):
            #line = single_exp_lines(i)
            line = filter(lambda x: x in printable, line)
            for node_tag, pattern_string in subterms_dict.items():
                pattern_list = re.split(r",|:", pattern_string[0])
                matches = [pattern for pattern in pattern_list if pattern in line]
            
                if len(matches):
                    info_string = ", ".join(list(matches)) + " "
                    if i < (l - 3):
                       Nextline1 = filter(lambda x: x in printable, single_exp_lines[i + 1])
                       Nextline2 = filter(lambda x: x in printable, single_exp_lines[i + 2])
                       Nextline3 = filter(lambda x: x in printable, single_exp_lines[i + 3])
                       finalline = Nextline1 + Nextline3 + Nextline3
    
                       numeric_values = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", finalline)
                       if len(numeric_values):
                       	  value_list = list(numeric_values[0])
                      	 #line1 = re.findall(r'\t([A-Za-z0-9()+ &,/.-: ]+)', line)
                        
                       	  info_string = info_string + "".join([value for value in value_list if value != ""])
                       	  retval [node_tag] = info_string
                       break
        return retval


# Section Information experience extractor
# Armaan Singala
def section_exp_extractor_tech(document, section, subterms_dict, parsed_items_dict):
    retval = OrderedDict()
    #print("Section is 1         ",section)
    #print("dOCUMENT is 1         ",document)
    #single_exp_lines = parsed_items_dict["Sections"].get(section)
    single_exp_lines = StringIO.StringIO(document)
    if single_exp_lines != None:
        #print("single_exp_lines is ",single_exp_lines)
    	#l = len(single_exp_lines)
        for line in single_exp_lines:
            	#line = single_exp_lines(i)
    		#line = filter(lambda x: x in printable, line)
                #print("lineee is ",line)
        	for node_tag, pattern_string in subterms_dict.items():
        		pattern_list = re.split(r",|:", pattern_string[0])
                	matches = [pattern for pattern in pattern_list if pattern in line]
            		#print("Section is ",section)
                	#print("Line is",line)
                	#if len(matches):
                	#print("Matches is",matches)
            		info_string = ", ".join(list(matches)) + " "
               		if len(matches):
                               # Nextline = single_exp_lines[i + 1]
                            #print("Next line is ",Nextline)
                		value_list = list(line[0])
                  		#print("Value list is ",value_list)
                  		line1 = re.findall(r'\t([A-Za-z0-9()+ &,/.-: ]+)', line)
                  		info_string = info_string + line
                                #info_string = info_string + Nextline
                  		retval [node_tag] = info_string
                
        return retval

def section_exp_extractor(document, section, subterms_dict, parsed_items_dict):
    retval = []
    single_exp_lines = parsed_items_dict["Sections"].get(section)
    if single_exp_lines is not None:
        l = len(single_exp_lines)
        for i,line in enumerate(single_exp_lines):
            Line = filter(lambda x: x in printable, line)
            for node_tag, pattern_string in subterms_dict.items():
                pattern_list = re.split(r",|:", pattern_string[0])
                matches = [pattern for pattern in pattern_list if pattern in line]
            
                if len(matches):
                    info_string = ", ".join(list(matches)) + " "
                    numeric_values = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", Line)
                    if len(numeric_values):
                        value_list = list(numeric_values[0])
                        line1 = re.findall(r'\t([A-Za-z0-9()+ &,/.-: ]+)', Line)
                        retval.append (Line)
                    #break
        return retval



def section_pro_extractor(document, section, subterms_dict, parsed_items_dict):
    retval = []
    single_exp_lines = parsed_items_dict["Sections"].get(section)
    if single_exp_lines != None:
        l = len(single_exp_lines)
        for i,line in enumerate(single_exp_lines):
            #line = single_exp_lines(i)
            Line = filter(lambda x: x in printable, line)
            for node_tag, pattern_string in subterms_dict.items():
                pattern_list = re.split(r",|:", pattern_string[0])
                matches = [pattern for pattern in pattern_list if pattern in line]
            
                if len(matches):
                    info_string = ", ".join(list(matches)) + " "
                    numeric_values = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", Line)
                    if len(numeric_values):
                        value_list = list(numeric_values[0])
                        line1 = re.findall(r'\t([A-Za-z0-9()+ &,/.-: ]+)', line)
                        if i < (l - 1):
                            Nextline = filter(lambda x: x in printable, single_exp_lines[i + 1])
                            #print("Next line is ",Nextline)
                        if i > 0:
                            Prevline = filter(lambda x: x in printable, single_exp_lines[i - 1])
                            #print("Prev line is ",Prevline)
                        
                        #print("current line is ",line)
    
                            retval.append (Prevline)
                            retval.append (Line)
                            retval.append (Nextline)
                    #break
        return retval




# Find if new section has started
def is_new_section(line,subterms_dict):
    new_section = ""
    first_word_of_line = ""
    regex_pattern = re.compile(r"^[\s]?(\w+)?[:|\s]")
    match = regex_pattern.search(line)
    if match != None and len(match.groups()) > 0 and match.group(1) != "":
        first_word_of_line = match.group(1)
        if first_word_of_line != None:
            for node_tag, pattern_list in subterms_dict.items():
                for pattern in pattern_list:
                    if first_word_of_line in pattern:
                        new_section = node_tag
    return new_section

# Segementation into sections, a sentence collector
'''
Read line by line
Get first token, send it to section_finder(token, subterm_dict),returns section node_tag or ""
Once section is found, make it current_section, and add sentences to it till, a next section is found
'''
def section_extractor( document, section, subterms_dict,parsed_items_dict ):
    retval = OrderedDict()
    if document != "NA":
        current_section = ""
        lines = re.split(r'[\n\r]+', document)
        for line in lines:
            new_section = is_new_section(line, subterms_dict)
            if new_section != "":
                current_section = new_section
                continue
            retval[current_section] = retval.get(current_section, []) + [line]

    return retval

#read config and store in equivalent internal list-of-dictionaries structure. No processing-parsing.
def read_config( configfile ):

    tree = ET.parse(configfile)
    root = tree.getroot()

    config = []
    for child in root:
        term = OrderedDict()
        term["Term"] = child.get('name', "")
        for level1 in child:
            term["Method"] = level1.get('name', "")
            term["Section"] = level1.get('section', "")
            for level2 in level1:
                term[level2.tag] = term.get(level2.tag, []) + [level2.text]

        config.append(term)
#x.encode('utf-8') for x in tmp
    jason_result = json.dumps(config, indent=4)
    # print("Specifications:\n {}".format(jason_result))
    return config

# Processes docuemtn as per specifications in config and returns result in dictionary
def parse_document(document, config):
    parsed_items_dict = OrderedDict()
    #print("parse_document",document)
    for term in config:
        term_name = term.get('Term')
        extraction_method = term.get('Method')
        extraction_method_ref = globals()[extraction_method]
        section = term.get("Section") # Optional
        subterms_dict = OrderedDict()
        for node_tag, pattern_list in term.items()[3:]:
            #print("Node tag is ",node_tag)
            subterms_dict[node_tag] = pattern_list
        parsed_items_dict[term_name] = extraction_method_ref(document, section, subterms_dict, parsed_items_dict)

    # key of section extractors is not to be printed
    del parsed_items_dict["Sections"]
    return parsed_items_dict

###### MAIN ##############
def main1(configPath,document):

    final_result = []

    configfile = "./" + configPath
    config = read_config(configfile)
    
    #print("This is Main function. config is ",config)

    document=document.upper()
    document=document.replace('EDUCATION','EDUCATION:',10)
    document=document.replace('SKILLS','SKILLS:',10)
    document=document.replace('SUMMARY','SUMMARY:',10)
    document=document.replace('EXPERIENCE','EXPERIENCE:',10)
    document=document.replace('PROJECT','EXPERIENCE:',10)
    document=document.replace('::',':',10)

    #print("Document is ",document)
    result = parse_document(document, config)
    final_result.append(result)

    jason_result = json.dumps(final_result, indent=4)
    print("Final Result:\n {}".format(jason_result))

    return jason_result

