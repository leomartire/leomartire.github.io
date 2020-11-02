#!/bin/bash

import sys
import re

def bibtex_open(filename):
  fid = open(filename, 'r')
  #lines = [line.rstrip('\n') for line in fid]
  lines = [line for line in fid]
  fid.close()
  #if(lines[0]=='Automatically generated by Mendeley Desktop 1.19.4' and lines[1]=='Any changes to this file will be lost if it is regenerated by Mendeley.' and lines[2]=='' and lines[3]=='BibTeX export options can be customized via Options -> BibTeX in Mendeley Desktop' and lines[4]==''):
  if(lines[0]=='Automatically generated by Mendeley Desktop 1.19.4\n' and lines[1]=='Any changes to this file will be lost if it is regenerated by Mendeley.\n' and lines[2]=='\n' and lines[3]=='BibTeX export options can be customized via Options -> BibTeX in Mendeley Desktop\n' and lines[4]=='\n'):
    lines = lines[5:]
  else:
    print('ERROR, FORMAT OF REFERENCE FILE NOT RECOGNISED.'); stop
  #print(lines[0:5]); stop
  return(lines)

def bibtex_format(lines):
  joined_lines = ''.join(lines)
  items = joined_lines.split('}\n@')
  items[0] = items[0][1:]
  #print(items[0]); stop
  return(items)

def bibtex_dictionnarise(items):
  listed_items = []
  for it in items:
    m = re.search('^[a-z]*\{', it);
    item_type = m.group(0)[:-1] # get item type
    #print(item_type); stop
    it = re.sub(m.group(0), '', it) # delete item type
    m = re.search('^[^,]*,\n', it)
    if(m==None):
      print('Item type regex returned nothing on "'+it+'" .'); stop
    item_key = m.group(0)[:-2] # get item type
    #print(item_key); stop
    it = re.sub(m.group(0), '', it) # delete item key
    #print(it); stop
    splitted_item = it.split(',\n')
    splitted_item[-1] = splitted_item[-1][:-1]
    #print(splitted_item); stop
    curdict = dict()
    curdict['type'] = item_type
    curdict['key'] = item_key
    #print(curdict); stop
    for field in splitted_item:
      #print(field)
      splitted_field = field.split(' = {')
      #print(splitted_field); stop
      if(len(splitted_field)!=2):
        print(splitted_field); stop
      else:
        curkey = splitted_field[0]
        curval = splitted_field[1][:-1]
        if(curkey=='author'):
          curdict[curkey] = authors_str2list(curval)
          #print(authors_str2list(curval)); stop
        elif(curkey=='title'):
          curdict[curkey] = curval[1:-1] # cut second set of braces
        elif(curkey=='type'):
          continue # skip if "type" field is found (stick to sorting)
        else:
          curdict[curkey] = curval
    #print(curdict); stop
    if(not('author' in curdict)):
      # Safeguard.
      print('  No "author" key in current dictionnary.')
      if(curdict['type']=='book' and ('editor' in curdict)):
        # Save the day.
        curdict['author'] = curdict['editor']
        print('    Saved the day by setting author as the editor.')
      else:
        print('    Could not save the day.')
        print(curdict);stop
    listed_items.append(curdict)
  return(listed_items)

def authors_str2list(authstr):
  return([auth.split(', ') for auth in authstr.split(' and ')])

def authors_match_sought(authlist, sought_lastname):
  for i in range(len(authlist)):
    if(authlist[i][0]==sought_lastname):
      return(i+1)
  return(-1)

def bibtex_load(filename):
  #lines = bibtex_open(filename)
  #items = bibtex_format(lines)
  #listed_items = bibtex_dictionnarise(items)
  listed_items = bibtex_dictionnarise(bibtex_format(bibtex_open(filename)))
  #print(listed_items); stop
  print('Finished loading and formatting references.')
  print(' ')
  return(listed_items)

def bibtex_fetch(filename):
  listed_items = bibtex_load(filename)
  sought = 'Martire'
  kept_articles_1st = list()
  kept_articles_2nd = list()
  kept_articles_nth = list()
  kept_presenta_1st = list()
  kept_presenta_2nd = list()
  kept_presenta_nth = list()
  for i in listed_items:
    #print(' '); print(' '); print(i)
    nth_author = authors_match_sought(i['author'], sought)
    #if(i['type']=='phdthesis'):
      #print(i['author'])
    
    if(nth_author==1):
      if(i['type']=='article' or i['type']=='phdthesis'):
        kept_articles_1st.append(i)
      elif(i['type']=='inproceedings'):
        kept_presenta_1st.append(i)
    elif(nth_author==2):
      if(i['type']=='article'):
        kept_articles_2nd.append(i)
      elif(i['type']=='inproceedings'):
        kept_presenta_2nd.append(i)
    elif(nth_author!=-1):
      if(i['type']=='article'):
        kept_articles_nth.append(i)
      elif(i['type']=='inproceedings'):
        kept_presenta_nth.append(i)
  return([kept_articles_1st, kept_articles_2nd, kept_articles_nth, kept_presenta_1st, kept_presenta_2nd, kept_presenta_nth])

def auth_fmt(item, i):
  #return(item['author'][i][1]+' '+item['author'][i][0])
  #return(item['author'][i][1][0]+'. '+item['author'][i][0])
  return(' '.join([pp[0]+'.' for pp in item['author'][i][1].split(' ')]) + ' ' + item['author'][i][0])

def bibitem_print(item, n):
  # print authors
  nauth = len(item['author'])
  if(n==1):
    string = '<b>'+auth_fmt(item, 0)+'</b>'
    if(nauth==2):
      string = string+' and '+auth_fmt(item, 1)
    elif(nauth>2):
      string = string+' <i>et al.</i>'
  elif(n==2):
    if(nauth==2):
      string = auth_fmt(item, 0)+' and <b>'+auth_fmt(item, 1)+'</b>'
    else:
      string = auth_fmt(item, 0)+', <b>'+auth_fmt(item, 1)+'</b>, <i>et al.</i>'
  else:
    string = auth_fmt(item, 0)+' <b><i>et al.</i></b>'
  
  # print year and title
  string = string+' ('+str(item['year'])+') - '+item['title']
  
  # print type (journal or other)
  if(item['type']=='article'):
    string = string+' - <i>'+item['journal']+'</i>'
  elif(item['type']=='phdthesis'):
    string = string+' - PhD Thesis (<i>'+item['school']+'</i>)'
  
  # finally add doi if available
  if('doi' in item):
    doi = item['doi']
    #print(doi)
    if(doi[0:3]=='10.'):
      string = string+' - '+'<a href="doi.org/'+doi+'" target="_blank">DOI: '+doi+'</a>'
  
  string = string+'.'
  return(string)
