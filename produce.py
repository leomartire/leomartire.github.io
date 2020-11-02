#!/bin/bash

from scripts.bibtex_utilities import bibtex_fetch, bibitem_print

def produce_publications(input_file, output_file):
  [a1, a2, an, p1, p2, pn] = bibtex_fetch(input_file)
  
  #print('\n\n'.join([str(a) for a in a1])); print('\n\n'); stop
  #print('\n\n'.join([str(a) for a in an])); print('\n\n'); stop
  
  fmt_a1 = [bibitem_print(a, 1) for a in a1]
  fmt_a2 = [bibitem_print(a, 2) for a in a2]
  fmt_an = [bibitem_print(a, -1) for a in an]
  
  join_a1 = '  <li>'+('</li>\n  <li>'.join(fmt_a1))+'</li>'
  join_a2 = '  <li>'+('</li>\n  <li>'.join(fmt_a2))+'</li>'
  join_an = '  <li>'+('</li>\n  <li>'.join(fmt_an))+'</li>'
  
  publications_str = '<ul>\n'+join_a1+'\n</ul>\n\n<ul>\n'+join_a2+'\n</ul>\n\n<ul>\n'+join_an+'\n</ul>'
  #print(publications_str); stop
  
  fid = open(output_file, 'w')
  fid.write(publications_str)
  fid.close()

produce_publications('./data/references.bib', './processed/publications.htm')

