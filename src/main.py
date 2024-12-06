"""
Alunos:
  Gabriel Reimann Cervi (22204117)
  João Pedro Schmidt Cordeiro (22100628)
"""

import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.grammar import Grammar

def process_input(input_str):
    grammar_input, sentence = input_str.strip('\"').split('\"')

    grammar = Grammar.from_string(grammar_input)
    grammar.generate_ll1_table()
    
    return f"<{grammar.print_ll1_table()}{grammar.verify_if_valid_sentence(sentence)}>"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_str = sys.argv[1]
    else:
        input_str = "{E,A,T,B,F}{m,v,i,o,c}{E}{E = TA; A = mTA; A = &; T = FB; B = vFB; B = &; F = i; F = oEc};\"oimicvi\""
        input_str = "{P,K,T,V,L}{b,e,c,t,v,m}{P}{P = KL; P = bKLe; K = cK; K = TV; T = tT; T = &; V = vV; V = &; L = mL; L = &};\"bctvme\""
        input_str = "{P,K,V,F,C}{c,v,f,i,b,e,m}{P}{P = KVC; K = cK; K = &; V = vV; V = F; F = fPiF; F = &; C = bVCe; C = miC; C = &};\"cvfcvbveimi\""
    
    print(process_input(input_str))