class Grammar:
    def __init__(self, non_terminals, terminals, initial_symbol, productions):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.initial_symbol = initial_symbol
        self.productions = productions
        self.first_set = {}
        self.follow_set = {}
        self.ll1_table = {}

    def __str__(self):
        return f"Non-terminals: {self.non_terminals}\nTerminals: {self.terminals}\nInitial symbol: {self.initial_symbol}\nProductions: {self.productions}"

    @classmethod
    def from_string(cls, input_str):
        items = input_str.strip('{};').split('}{')
        
        # Extract information from separated input string
        non_terminals = items[0].split(',')
        terminals = items[1].split(',')
        initial_symbol = items[2]
        productions = {}

        # Separate productions in a list
        productions_strings = items[3].split(';')

        # Read every production
        for prod in productions_strings:
            if '=' in prod:
                left, right = prod.split('=')
                left = left.strip()
                right = right.strip()

                # If non_terminal is not a key in the productions dictionary
                if left not in productions:
                    productions[left] = []
                productions[left].append(right)
        
        return cls(sorted(non_terminals), sorted(terminals), initial_symbol, productions)
        
    
    def print_output_EI4(self):
        # Get all symbols and sort them
        first_symbols = list(self.first_set.keys())
        follow_symbols = list(self.follow_set.keys())
        
        # Format First sets
        first_parts = []
        for symbol in first_symbols:
            first_set = sorted(self.first_set[symbol])  # Sort the set elements
            first_parts.append(f"First({symbol}) = {{{', '.join(first_set)}}}")
        
        # Format Follow sets
        follow_parts = []
        for symbol in follow_symbols:
            follow_set = sorted(self.follow_set[symbol])  # Sort the set elements
            follow_parts.append(f"Follow({symbol}) = {{{', '.join(follow_set)}}}")
        
        # Combine all parts with semicolons and spaces
        output = '; '.join(first_parts + follow_parts) + ';'
        print(output)

    def print_productions(self):
        # Get all symbols and sort them
        symbols = list(self.productions.keys())
        # Move initial symbol to front
        if self.initial_symbol in symbols:
            symbols.remove(self.initial_symbol)
            symbols = [self.initial_symbol] + sorted(symbols)
        
        # Print productions
        for symbol in symbols:
            productions_str = " | ".join(self.productions[symbol])
            print(f"    {symbol} -> {productions_str}")

    def print_first_set(self):
        print("\nFIRST SET:")
        # Get all symbols and sort them
        symbols = list(self.first_set.keys())
        # Move initial symbol to front
        if self.initial_symbol in symbols:
            symbols.remove(self.initial_symbol)
            symbols = [self.initial_symbol] + sorted(symbols)
            
        for nt in symbols:
            print(f"{nt} -> {self.first_set[nt]}")

    def print_follow_set(self):
        print("\nFOLLOW SET:")
        # Get all symbols and sort them
        symbols = list(self.follow_set.keys())
        # Move initial symbol to front
        if self.initial_symbol in symbols:
            symbols.remove(self.initial_symbol)
            symbols = [self.initial_symbol] + sorted(symbols)
        
        for nt in symbols:
            print(f"{nt} -> {self.follow_set[nt]}")

    def calculate_first_set(self):
        # Initialize FIRST sets for all non-terminals
        for nt in self.non_terminals:
            self.first_set[nt] = set()
            
        # Keep iterating until no changes are made
        while True:
            changes_made = False
            
            # For each production rule
            for nt, productions in self.productions.items():
                for production in productions:
                    # Case 1: Empty production
                    if production == "&":
                        if "&" not in self.first_set[nt]:
                            self.first_set[nt].add("&")
                            changes_made = True
                        continue
                    
                    # Case 2: Production starts with terminal
                    if production[0] in self.terminals:
                        if production[0] not in self.first_set[nt]:
                            self.first_set[nt].add(production[0])
                            changes_made = True
                        continue
                    
                    # Case 3: Production starts with non-terminal
                    # Add all non-epsilon symbols from FIRST set of first symbol
                    first_symbol = production[0]
                    if first_symbol in self.first_set:
                        for symbol in self.first_set[first_symbol] - {"&"}:
                            if symbol not in self.first_set[nt]:
                                self.first_set[nt].add(symbol)
                                changes_made = True
                        
                        # If first symbol can derive epsilon, continue with next symbol
                        i = 0
                        all_can_be_empty = True
                        while i < len(production) and all_can_be_empty:
                            current = production[i]
                            if current in self.terminals:
                                if current not in self.first_set[nt]:
                                    self.first_set[nt].add(current)
                                    changes_made = True
                                all_can_be_empty = False
                            elif current in self.non_terminals:
                                if "&" not in self.first_set[current]:
                                    all_can_be_empty = False
                                for symbol in self.first_set[current] - {"&"}:
                                    if symbol not in self.first_set[nt]:
                                        self.first_set[nt].add(symbol)
                                        changes_made = True
                            i += 1
                        
                        # If all symbols in production can derive epsilon
                        if all_can_be_empty and "&" not in self.first_set[nt]:
                            self.first_set[nt].add("&")
                            changes_made = True
            
            # If no changes were made in this iteration, we're done
            if not changes_made:
                break

    def calculate_follow_set(self):
        # Initialize FOLLOW sets for all non-terminals
        for nt in self.non_terminals:
            self.follow_set[nt] = set()
        
        # Add $ to FOLLOW set of start symbol
        self.follow_set[self.initial_symbol].add('$')
        
        # Keep iterating until no changes are made
        while True:
            changes_made = False
            
            # For each production rule
            for nt, productions in self.productions.items():
                for production in productions:
                    if production == "&":  # Skip empty productions
                        continue
                    
                    # Scan the production from left to right
                    for i in range(len(production)):
                        current = production[i]
                        
                        # Skip if current symbol is a terminal
                        if current not in self.non_terminals:
                            continue
                        
                        # If this is not the last symbol in the production
                        if i < len(production) - 1:
                            remaining = production[i + 1:]
                            first_of_remaining = set()
                            
                            # Calculate FIRST set of remaining string
                            all_can_be_empty = True
                            for symbol in remaining:
                                if symbol in self.terminals:
                                    first_of_remaining.add(symbol)
                                    all_can_be_empty = False
                                    break
                                elif symbol in self.non_terminals:
                                    first_of_remaining.update(self.first_set[symbol] - {'&'})
                                    if '&' not in self.first_set[symbol]:
                                        all_can_be_empty = False
                                        break
                            
                            # Add FIRST(remaining) - {&} to FOLLOW(current)
                            for symbol in first_of_remaining:
                                if symbol not in self.follow_set[current]:
                                    self.follow_set[current].add(symbol)
                                    changes_made = True
                            
                            # If all remaining symbols can derive empty
                            if all_can_be_empty:
                                # Add FOLLOW(nt) to FOLLOW(current)
                                for symbol in self.follow_set[nt]:
                                    if symbol not in self.follow_set[current]:
                                        self.follow_set[current].add(symbol)
                                        changes_made = True
                        
                        # If this is the last symbol or all following symbols can derive empty
                        else:
                            # Add FOLLOW(nt) to FOLLOW(current)
                            for symbol in self.follow_set[nt]:
                                if symbol not in self.follow_set[current]:
                                    self.follow_set[current].add(symbol)
                                    changes_made = True
            
            # If no changes were made in this iteration, we're done
            if not changes_made:
                break

    def generate_ll1_table(self):
        # Calculate First and Follow sets
        self.calculate_first_set()
        self.calculate_follow_set()

        # Fill table
        for left_prod in self.productions:
            for right_prod in self.productions[left_prod]:
                # If first symbol is non-terminal, for every terminal in First(a), include A :== a in M[A,a]
                if right_prod[0] in self.non_terminals:
                    for first_t in self.first_set[right_prod[0]]:
                        self.ll1_table[(left_prod,first_t)] = right_prod
                # If first symbol is terminal, include A :== a in M[A,a]
                elif right_prod[0] in self.terminals:
                    self.ll1_table[(left_prod,right_prod[0])] = right_prod
                
                # If epsilon is in First(a) include A :== a in M[A,b] for every b in Follow(A)
                if right_prod == '&':
                    for follow_t in self.follow_set[left_prod]:
                        self.ll1_table[(left_prod,follow_t)] = right_prod
    
    def print_ll1_table(self):
        str_table = []
        for (line, column), production in self.ll1_table.items():
            str_table.append(f"[{line},{column},{production}]")

        string = (
            f"<{{{','.join(self.non_terminals)}}};"
            f"{self.initial_symbol};"
            f"{{{','.join(self.terminals)},$}};"
            f"{''.join(sorted(str_table))}>"
        )

        return string
    
    def verify_if_valid_sentence(self, sentence):
        sentence += '$'
        stack = '$' + self.initial_symbol

        try:
            while True:
                # If both top of stack and header are on $ (end of sentence symbol),
                # end accepting the sentence
                if stack[-1] == '$' and sentence[0] == '$':
                    return "<sim>"
                
                # If top of stack has the same symbol as the header and symbol =/= $,
                # pop top of stack and move header forward
                elif stack[-1] == sentence[0] and sentence[0] != '$':
                    stack = stack[:-1]
                    sentence = sentence[1:]
                
                # If symbol on top of stack is a non-terminal, check LL1 table,
                # pop non-terminal and push the corresponding production reversed
                elif stack[-1] in self.non_terminals:
                    production = self.ll1_table[(stack[-1],sentence[0])]

                    stack = stack[:-1]

                    if production != '&':
                        stack += production[::-1]
        
        except KeyError:
            return "<nao>"




