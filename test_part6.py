import unittest
import cnf
from resolution import full_resolution, resolution_closure
import time

class TestResolutionClosure(unittest.TestCase):
    def test_closure_1(self):
        clauses = ['a || b', 
                   '!a || b']
        resolvents = ['b']
        expected = {cnf.c(clause) for clause in clauses + resolvents}
        result = resolution_closure([cnf.c(clause) for clause in clauses])
        assert result == expected
        
    def test_closure_2(self):
        clauses = ['a || b', 
                   '!a || !b']
        resolvents = []
        expected = {cnf.c(clause) for clause in clauses + resolvents}
        result = resolution_closure([cnf.c(clause) for clause in clauses])
        assert result == expected

    def test_closure_3(self):
        clauses = ['a || b', 
                   '!a || b',
                   '!b']
        resolvents = ['!a', 'a', 'b', 'FALSE']
        expected = {cnf.c(clause) for clause in clauses + resolvents}
        result = resolution_closure([cnf.c(clause) for clause in clauses])
        assert result == expected
        
    def test_closure_4(self):
        clauses = ['a || b', 
                   '!a',
                   '!b || !c',
                   'c || d',
                   '!d || !e']        
        resolvents =   ['!b || !e', 
                        '!b || d', 
                        '!c', 
                        '!e', 
                        'a || !c', 
                        'a || !e',
                        'a || d', 
                        'b', 
                        'c || !e', 
                        'd']
        expected = {cnf.c(clause) for clause in clauses + resolvents}
        result = resolution_closure([cnf.c(clause) for clause in clauses])
        assert result == expected

class TestEarlyStopping(unittest.TestCase):
    def test_es_1(self):
        clauses = ['a || b', 
                   '!a || b']
        resolvents = ['b']
        expected = {cnf.c(clause) for clause in clauses + resolvents}
        result = resolution_closure([cnf.c(clause) for clause in clauses],
                                    early_stopping = True)
        assert result == expected
        
    def test_es_2(self):
        clauses = ['a || b', 
                   '!a || !b']
        resolvents = []
        expected = {cnf.c(clause) for clause in clauses + resolvents}
        result = resolution_closure([cnf.c(clause) for clause in clauses],
                                    early_stopping = True)
        assert result == expected

    def test_es_3(self):
        clauses = ['a || b', 
                   '!a || b',
                   '!b']
        result = resolution_closure([cnf.c(clause) for clause in clauses],
                                    early_stopping = True)
        assert result == { cnf.c('FALSE') }
        
    def test_es_4(self):
        clauses = ['a || b', 
                   '!a',
                   '!b || !c',
                   'c || d',
                   '!d || !e']        
        resolvents =   ['!b || !e', 
                        '!b || d', 
                        '!c', 
                        '!e', 
                        'a || !c', 
                        'a || !e',
                        'a || d', 
                        'b', 
                        'c || !e', 
                        'd']
        expected = {cnf.c(clause) for clause in clauses + resolvents}
        result = resolution_closure([cnf.c(clause) for clause in clauses],
                                    early_stopping = True)
        assert result == expected

    def test_es_5(self):
        clauses = ['a || b', 
                   '!a',
                   '!b || !c',
                   'c || d',
                   '!d || !e',
                   'e'] 
        result = resolution_closure([cnf.c(clause) for clause in clauses],
                                    early_stopping = True)
        assert result == { cnf.c('FALSE') }

    def test_es_6(self):
        clauses =  ['a || b',
                    '!a || b || e', 
                    'a || !b', 
                    'b || !e', 
                    'd || !e', 
                    '!b || !c || !f', 
                    'a || !e', 
                    '!b || f', 
                    '!b || c']
        start_time1 = time.perf_counter()
        result = resolution_closure([cnf.c(clause) for clause in clauses],
                                    early_stopping = True)
        end_time1 = time.perf_counter()
        assert result == { cnf.c('FALSE') }
        start_time2 = time.perf_counter()
        result = resolution_closure([cnf.c(clause) for clause in clauses],
                                    early_stopping = False)
        end_time2 = time.perf_counter()
        assert cnf.c('FALSE') in result
        print(f"\nWith early stopping: {end_time1 - start_time1:0.4f}s")
        print(f"W/o  early stopping: {end_time2 - start_time2:0.4f}s")


class TestFullResolution(unittest.TestCase):
    
    def test_full_resolution_1(self):
        clauses =  ['a || b',
                    '!a || b || e', 
                    'a || !b', 
                    'b || !e', 
                    'd || !e', 
                    '!b || !c || !f', 
                    'a || !e', 
                    '!b || f', 
                    '!b || c']
        assert not full_resolution(cnf.sentence('\n'.join(clauses)))
        assert full_resolution(cnf.sentence('\n'.join(clauses[1:])))
        
    def test_full_resolution_2(self):
        clauses = ['a || b', 
                   '!a || b']
        assert full_resolution(cnf.sentence('\n'.join(clauses)))

    def test_full_resolution_3(self):
        clauses = ['a || b', 
                   '!a',
                   '!b || !c',
                   'c']
        assert not full_resolution(cnf.sentence('\n'.join(clauses)))
        assert full_resolution(cnf.sentence('\n'.join(clauses[:-1])))

    def test_full_resolution_4(self):
        clauses = ['a || b', 
                   '!a',
                   '!b || !c',
                   'c || d',
                   '!d || !e',
                   'e']
        assert not full_resolution(cnf.sentence('\n'.join(clauses)))
        assert full_resolution(cnf.sentence('\n'.join(clauses[:-1])))

    def test_full_resolution_5(self):
        clauses = ['a || b', 
                   '!a',
                   '!b || c',
                   'c || d',
                   '!d || !e',
                   'e']
        assert full_resolution(cnf.sentence('\n'.join(clauses)))


    def test_full_resolution_6(self):
        clauses = ['a || b', 
                   '!a || b',
                   'FALSE']
        assert not full_resolution(cnf.sentence('\n'.join(clauses)))


    