import json
import pytest
from pathlib import Path
import sys
import os

# Get the project root directory
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.grammar import Grammar
from src.main import process_input

def load_test_cases(filename):
    test_cases_dir = Path(__file__).parent / "test_cases"
    with open(test_cases_dir / filename) as f:
        return json.load(f)

# def assert_ll1_table_equals(actual, expected):
#     """Helper function to compare LL(1) parsing tables"""
#     assert sorted(actual.keys()) == sorted(expected.keys()), "Non-terminals in table don't match"
#     for nt in expected:
#         assert nt in actual, f"Non-terminal {nt} missing from table"
#         assert sorted(actual[nt].keys()) == sorted(expected[nt].keys()), \
#             f"Terminals for {nt} don't match"
#         for t in expected[nt]:
#             assert actual[nt][t] == expected[nt][t], \
#                 f"Production for {nt},{t} doesn't match. Expected {expected[nt][t]}, got {actual[nt][t]}"

# @pytest.mark.parametrize("test_case", load_test_cases("ll1_table.json"))
# def test_ll1_table_generation(test_case):
#     print(f"\nTesting: {test_case['name']}")
    
#     # Create grammar from input string
#     grammar = Grammar.from_string(test_case["input"])
    
#     # Generate LL(1) parsing table
#     grammar.generate_ll1_table()
    
#     # Verify LL(1) table
#     assert_ll1_table_equals(grammar.ll1_table, test_case["expected_table"])

# @pytest.mark.parametrize("test_case", load_test_cases("sentence_validation.json"))
# def test_sentence_validation(test_case):
#     print(f"\nTesting: {test_case['name']}")
    
#     # Create grammar and generate LL(1) table
#     grammar = Grammar.from_string(test_case["grammar"])
#     grammar.generate_ll1_table()
    
#     # Verify sentence validation
#     result = grammar.verify_if_valid_sentence(test_case["sentence"])
#     assert result == test_case["expected_result"], \
#         f"Expected {test_case['expected_result']}, got {result}" 

@pytest.mark.parametrize("test_case", load_test_cases("complete_tests.json"))
def test_complete_grammar_processing(test_case):
    print(f"\nTesting: {test_case['name']}")
    
    # Process input and get output
    grammar_input = test_case["input"]
    result = process_input(grammar_input)
    
    # Verify output matches expected
    assert result == test_case["expected_output"], \
        f"Expected {test_case['expected_output']}, got {result}"