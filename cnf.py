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
    """Part 3, Question 1"""
    pass
     
class Clause:
    """
    Part 3, Question 2
    Part 4, Question 2
    
    """
    pass

class Cnf:
    """
    Part 3, Question 3
    Part 8, Question 2
    Part 8, Question 3
    
    """
    pass