def l(s):
    """
    Convenience method for constructing literals.
        
    e.g., c('!b') should create a negative literal for symbol b.
    
    The symbol should only consist of alphanumeric characters [A-Za-z0-9] 
    and underscores, however it can be of arbitrary length. The symbol may
    optionally be prefixed with !, which indicates a negative literal.
    
    """
    if s[0] == '!':
        return Literal(s[1:], False)
    else:
        return Literal(s, True)

def c(s):
    """
    Convenience method for constructing CNF clauses.
        
    e.g., c('!a || b || e') should create a Clause instance that is the
    disjunction of negative literal a, positive literal b and, and 
    positive literal e.   

    There is a special string "FALSE" that creates a Clause, representing
    a disjunction of zero literals.
    
    """
    if s == 'FALSE':
        literal_strings = []
    else:
        literal_strings = [x.strip() for x in s.split('||')]
    return Clause([l(x) for x in literal_strings])

def sentence(s):
    """
    Convenience method for constructing CNF sentences.
        
    e.g., c('\n'.join(['!a || b', '!b || d']) should create a Sentence 
    instance with two clauses: (!a || b) AND (!b || d').


    """
    clauses = s.split('\n')
    return Cnf([c(clause.strip()) for clause in clauses])


class Literal:
    def __init__(self, symbol, polarity = True):
        self.symbol = symbol
        self.polarity = polarity
    
    def __eq__(self, other):
        return self.symbol == other.symbol and self.polarity == other.polarity
    
    def __lt__(self, other):
        if self.symbol < other.symbol:
            return True
        elif other.symbol < self.symbol:
            return False
        else:
            return self.polarity < other.polarity

    def __hash__(self):
        return hash(self.symbol) + hash(self.polarity)
    
    def __str__(self):
        result = ''
        if not self.polarity:
            result = '!'
        return result + self.symbol
 
class Clause:
    def __init__(self, literals):
        self.literals = literals
        self.literal_values = dict()
        for lit in self.literals:
            self.literal_values[lit.symbol] = lit.polarity
        self.syms = set([l.symbol for l in self.literals])
        self.num_literals  = len(literals)

    def __len__(self):
        return self.num_literals

    def __bool__(self):
        return len(self.literals) > 0

    def __eq__(self, other):
        return set(self.literals) == set(other.literals)

    def __lt__(self, other):
        return str(self) < str(other)

    def __hash__(self):
        return hash(tuple(sorted([str(l) for l in self.literals])))

    def __str__(self):
        if len(self.literals) == 0:
            return 'FALSE'
        else:
            ordered = sorted(self.literals)
            return ' || '.join([str(l) for l in ordered])
        
    def __contains__(self, sym):
        return sym in self.literal_values

    def __getitem__(self, sym):
        return self.literal_values[sym]
    
    def __or__(self, other):
        common_symbols = self.literal_values.keys() & other.literal_values.keys()
        for sym in common_symbols:
            if self.literal_values[sym] != other.literal_values[sym]:
                return None
        return Clause(list(set(self.literals + other.literals)))

    def symbols(self):
        return self.syms

    def remove(self, sym):
        new_literals = [lit for lit in self.literals if lit.symbol != sym]        
        return Clause(new_literals)


class Cnf:
    def __init__(self, clauses):
        self.clauses = set(clauses)

    def symbols(self):
        syms = set([])
        for clause in self.clauses:
            syms = syms | clause.symbols()
        return syms
    
    def __str__(self):
        clause_strs = sorted([str(c) for c in self.clauses])     
        return '\n'.join(clause_strs)
        
    ## new
    def check_model(self, term):
        def check_against_clause(clause):
            for symbol in clause.symbols():
                if ((not term[symbol] and not clause[symbol]) or
                    (term[symbol] and clause[symbol])):
                    return True                
            return False
        for clause in self.clauses:
            if not check_against_clause(clause):
                return False
        return True   

    ## new
    def implicit_model(self):
        unit_clauses = [c.literals[0] for c in self.clauses if len(c) == 1]
        model = {c.symbol: c.polarity for c in unit_clauses}
        return model
    

