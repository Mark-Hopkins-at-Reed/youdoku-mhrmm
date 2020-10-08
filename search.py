import cnf
from cnf import Clause, Literal, Cnf
from resolution import limited_unit_resolution_closure, unit_resolution_closure

def assign(model_so_far, symbol, bool_assignment):
    return {**model_so_far, symbol: bool_assignment}


class SearchSolver:
            
    def __call__(self, sent):
        symbols = sent.symbols()
        result = self._search_solver_helper(sent, symbols)
        return result
    
    def _search_solver_helper(self, sent, symbols):                       
        m = sent.implicit_model()
        unassigned_symbols = sorted(symbols - m.keys())
        if len(unassigned_symbols) == 0:
            if sent.check_model(m):
                return m, [m]
            else:
                return None, [m]
        else:
            next_symbol = unassigned_symbols[0]
            negative_unit_clause = Clause([Literal(next_symbol, polarity=False)])
            sent_if_false = Cnf(sent.clauses | { negative_unit_clause })            
            sat_if_false, models_if_false = self._search_solver_helper(sent_if_false, symbols)            
            if sat_if_false != None: # early termination if already satisfied
                return sat_if_false, models_if_false
            positive_unit_clause = Clause([Literal(next_symbol, polarity=True)])
            sent_if_true = Cnf(sent.clauses | { positive_unit_clause })
            sat_if_true, models_if_true = self._search_solver_helper(sent_if_true, symbols) 
            return sat_if_true, models_if_false + models_if_true  
    

search_solver = SearchSolver()

class DPLL:
            
    def __call__(self, sent):
        symbols = sent.symbols()
        sent = Cnf(unit_resolution_closure(sent.clauses))
        result = self._search_solver_helper(sent, symbols)
        return result
    
    def _search_solver_helper(self, sent, symbols):    
        m = sent.implicit_model()
        unassigned_symbols = sorted(symbols - m.keys())  # TODO: different orders
        if len(unassigned_symbols) == 0:
            if sent.check_model(m):
                return m
            else:
                return None
        else:
            next_symbol = unassigned_symbols[0]
            negative_unit_clause = Clause([Literal(next_symbol, polarity=False)])
            closure = limited_unit_resolution_closure(negative_unit_clause,
                                                      sent.clauses)
            if cnf.c('FALSE') not in closure:
                sat_if_false = self._search_solver_helper(Cnf(closure), symbols) 
                if sat_if_false != None: # early termination if already satisfied
                    return sat_if_false
            positive_unit_clause = Clause([Literal(next_symbol, polarity=True)])
            closure = limited_unit_resolution_closure(positive_unit_clause,
                                                      sent.clauses)
            if cnf.c('FALSE') not in closure:                
                sat_if_true = self._search_solver_helper(Cnf(closure), symbols)
                return sat_if_true 
            else:
                return None
    
dpll = DPLL()


