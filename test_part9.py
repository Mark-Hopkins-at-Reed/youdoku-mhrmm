import unittest
import cnf
from resolution import unit_resolution_closure, limited_unit_resolution_closure
from search import dpll, search_solver

class TestUnitResolution(unittest.TestCase):
        
    def test_unit_resolution_closure1(self):
        clauses = [cnf.c('!b || d'), 
                   cnf.c('b'),
                   cnf.c('!d')]
        expected = {cnf.c('!b || d'), 
                    cnf.c('b'),
                    cnf.c('!d'),
                    cnf.c('d'),
                    cnf.c('!b'),
                    cnf.c('FALSE')}
        assert unit_resolution_closure(clauses) == expected

    def test_unit_resolution_closure2(self):
        clauses = [cnf.c('!a'),
                   cnf.c('!b || d'), 
                   cnf.c('!b || e'), 
                   cnf.c('!c || !e || !f'), 
                   cnf.c('!e || f'), 
                   cnf.c('a || !b'), 
                   cnf.c('b || !d || e'), 
                   cnf.c('c || !e'), 
                   cnf.c('d || !e'), 
                   cnf.c('d || e')]
        expected = {cnf.c('!a'),
                    cnf.c('!b || d'), 
                    cnf.c('!b || e'), 
                    cnf.c('!c || !e || !f'), 
                    cnf.c('!e || f'), 
                    cnf.c('a || !b'), 
                    cnf.c('b || !d || e'), 
                    cnf.c('c || !e'), 
                    cnf.c('d || !e'), 
                    cnf.c('d || e'),
                    cnf.c('!b'),
                    cnf.c('!d || e')}
        assert unit_resolution_closure(clauses) == expected

    def test_unit_resolution_closure3(self):
        clauses = [cnf.c('!b || d'), 
                   cnf.c('b || e')]
        assert unit_resolution_closure(clauses) == set(clauses)
            
class TestLimitedUnitResolution(unittest.TestCase):
    
    def test_limited_unit_resolution_closure1(self):
        clauses = [cnf.c('!b || d'), 
                   cnf.c('b'),
                   cnf.c('d')]
        closure = limited_unit_resolution_closure(cnf.c('!d'), clauses)
        expected = {cnf.c('!b || d'), 
                    cnf.c('b'),
                    cnf.c('!d'),
                    cnf.c('d'),
                    cnf.c('!b'),
                    cnf.c('FALSE')}
        assert closure == expected

    def test_limited_unit_resolution_closure2(self):
        clauses = [cnf.c('!b || c'), 
                   cnf.c('b')]
        closure = limited_unit_resolution_closure(cnf.c('!d'), clauses)
        expected = {cnf.c('!b || c'), 
                    cnf.c('b'),
                    cnf.c('!d')}
        assert closure == expected

    def test_limited_unit_resolution_closure3(self):
        clauses = [cnf.c('!b || d'), 
                   cnf.c('b')]
        closure = limited_unit_resolution_closure(cnf.c('!d'), clauses)
        expected = {cnf.c('!b || d'), 
                    cnf.c('b'),
                    cnf.c('!d'),
                    cnf.c('!b'),
                    cnf.c('FALSE')}
        assert closure == expected


class TestDPLL(unittest.TestCase):

    def test_dpll1(self):
        clauses =  ['a || b',
                    '!a || b',
                    '!a || !b']
        result = dpll(cnf.sentence('\n'.join(clauses)))
        assert result == {'a': False, 'b': True}

    def test_dpll2(self):
        clauses =  ['a || b',
                    '!a || !b']
        result = dpll(cnf.sentence('\n'.join(clauses)))
        assert result == {'a': False, 'b': True}

    def test_dpll3(self):
        clauses =  ['a || b',
                    '!a || b',
                    'a || !b',
                    '!a || !b']
        result = dpll(cnf.sentence('\n'.join(clauses)))
        assert result == None

    def test_dpll4(self):
        clauses =  ['a || b',
                    '!a || b || e', 
                    'a || !b', 
                    'b || !e', 
                    'd || !e', 
                    '!b || !c || !f', 
                    'a || !e', 
                    '!b || f', 
                    '!b || c']
        result = dpll(cnf.sentence('\n'.join(clauses)))
        assert result == None
        result = dpll(cnf.sentence('\n'.join(clauses[1:])))
        assert result == {'a': False, 'b': False, 'c': False, 'd': False, 'e': False,  'f': False}
        result = dpll(cnf.sentence('\n'.join(clauses[:-1])))
        assert result == {'a': True, 'b': True, 'c': False, 'd': False, 'e': False,  'f': True}

class TestDPLLSpeed(unittest.TestCase):

    def test_dpll_contrastive(self):
        clauses =  ['a || b',
                    '!a || b || e', 
                    'a || !b', 
                    'b || !e', 
                    'd || !e', 
                    '!b || !c || !f', 
                    'a || !e', 
                    '!b || f', 
                    '!b || c',
                    'g1 || !a || b',
                    'g2 || !a || b',
                    'g3 || !a || b',
                    'g4 || !a || b',
                    'g5 || !a || b',
                    'g6 || !a || b',
                    'g7 || !a || b',
                    'g8 || !a || b',
                    'g9 || !a || b',
                    'g10 || !a || b',
                    'g11 || !a || b']
        result = dpll(cnf.sentence('\n'.join(clauses)))
        assert result == None

class TestSearchSolverSpeed(unittest.TestCase):

    def test_search_solver(self):
        clauses =  ['a || b',
                    '!a || b || e', 
                    'a || !b', 
                    'b || !e', 
                    'd || !e', 
                    '!b || !c || !f', 
                    'a || !e', 
                    '!b || f', 
                    '!b || c',
                    'g1 || !a || b',
                    'g2 || !a || b',
                    'g3 || !a || b',
                    'g4 || !a || b',
                    'g5 || !a || b',
                    'g6 || !a || b',
                    'g7 || !a || b',
                    'g8 || !a || b',
                    'g9 || !a || b',
                    'g10 || !a || b',
                    'g11 || !a || b']
        result, models = search_solver(cnf.sentence('\n'.join(clauses)))
        assert result == None
        assert len(models) == 131072
