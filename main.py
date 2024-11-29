"""
Alunos:
  Gabriel Reimann Cervi (22204117)
  João Pedro Schmidt Cordeiro (22100628)
"""

from sys import argv
from grammar import Grammar

#input = argv[1]

input = "{E,A,T,B,F}{m,v,i,o,c}{E}{E = TA; A = mTA; A = &; T = FB; B = vFB; B = &; F = i; F = oEc};\"oimicvi\""

grammar_input, sentence = input.strip('\"').split('\"')

grammar = Grammar.from_string(grammar_input)
grammar.generate_ll1_table()