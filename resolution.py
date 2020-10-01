import queue
import cnf

def resolve_symbol(clause1, clause2, symbol):
    if symbol in clause1 and symbol in clause2:
        if clause1[symbol] and not clause2[symbol]:
            return clause1.remove(symbol) | clause2.remove(symbol)
        if not clause1[symbol] and clause2[symbol]:
            return clause1.remove(symbol) | clause2.remove(symbol)
    return None

def optimized_resolve_symbol(clause1, clause2, symbol):
    """ Caller must ensure that the symbol appears in both clauses. """
    if clause1[symbol] != clause2[symbol]:
        return clause1.remove(symbol) | clause2.remove(symbol)
    return None

def resolve(clause1, clause2):
    resolvents = []
    for sym in clause1.syms & clause2.syms:
       resolvent = optimized_resolve_symbol(clause1, clause2, sym)  
       if resolvent is not None:
           resolvents.append(resolvent)
    return resolvents


class ClauseQueue:
    def __init__(self):
        self.queue = queue.PriorityQueue()
        self.priority_function = lambda clause: len(clause)
        self.cached_clauses = set([])
        
    def push(self, clause):
        if not clause in self.cached_clauses:
            self.queue.put((self.priority_function(clause), clause))
            self.cached_clauses.add(clause)
            return True
        else:
            return False
    
    def pop(self):
        if not self.empty():
            return self.queue.get()[1]
        else:
            return None
    
    def empty(self):
        return self.queue.empty()
    
    def num_generated(self):
        return len(self.cached_clauses)


def resolution_closure(initial_unprocessed, early_stopping=False,
                       resolution_filter = lambda c1, c2: True):
    processed = set([])    
    unprocessed = ClauseQueue()
    for c in initial_unprocessed:
        if early_stopping and not bool(c):
            return set([c])   
        unprocessed.push(c)
    while not unprocessed.empty():
        next_to_process = unprocessed.pop()
        for clause in processed:
            if resolution_filter(clause, next_to_process):
                for resolvent in resolve(next_to_process, clause):
                    unprocessed.push(resolvent)                  
                    if early_stopping and not bool(resolvent):
                        return set([resolvent])   
        processed.add(next_to_process)
    return processed


def full_resolution(sent):
    return cnf.c('FALSE') not in resolution_closure(sent.clauses, 
                                                    early_stopping = True)



def unit_resolution_closure(initial_unprocessed, early_stopping=False):
    resolution_filter = lambda c1, c2: len(c1) == 1 or len(c2) == 1
    return resolution_closure(initial_unprocessed,
                              early_stopping = early_stopping,
                              resolution_filter = resolution_filter)


class FifoClauseQueue:
    def __init__(self):
        self.queue = []
        self.cached_clauses = set([])
        
    def push(self, clause):
        if not clause in self.cached_clauses:
            self.queue.append(clause)
            self.cached_clauses.add(clause)
            return True
        else:
            return False
    
    def pop(self):
        if len(self.queue) > 0:
            result, self.queue = self.queue[0], self.queue[1:]
            return result
        else:
            return None
    
    def empty(self):
        return len(self.queue) == 0
    
    def num_generated(self):
        return len(self.cached_clauses)

    
def limited_unit_resolution_closure(unit_clause, processed, early_stopping=False):
    processed_unit_clauses = set([clause for clause in processed if len(clause) == 1])
    processed = set(processed)
    unprocessed = FifoClauseQueue()
    unprocessed.push(unit_clause)
    while not unprocessed.empty():
        next_to_process = unprocessed.pop()
        if len(next_to_process) == 1:
            comparisons = processed
        else:
            comparisons = processed_unit_clauses
        for clause in comparisons:
            for resolvent in resolve(next_to_process, clause):
                unprocessed.push(resolvent)
                if early_stopping and not bool(resolvent):
                    return set([resolvent])   
        processed.add(next_to_process)
        if len(next_to_process) == 1:
            processed_unit_clauses.add(next_to_process)
    return processed




    


