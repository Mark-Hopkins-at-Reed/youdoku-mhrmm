import unittest
import cnf
from search import search_solver, assign

class TestModelAssignment(unittest.TestCase):

    def test_assign1(self):
        model = {'a': False, 'b': True}
        assert assign(model, 'c', True) == {'a': False, 'b': True, 'c': True}
        assert model == {'a': False, 'b': True}

    def test_assign2(self):
        model = {'a': False, 'b': True}
        assert assign(model, 'c', False) == {'a': False, 'b': True, 'c': False}
        assert model == {'a': False, 'b': True}
        
    def test_assign3(self):
        model = {'a': False, 'b': True}
        assert assign(model, 'b', False) == {'a': False, 'b': False}
        assert model == {'a': False, 'b': True}


class TestImplicitModel(unittest.TestCase):
    
    def test_implicit1(self):
        clauses = ['a || b',
                   '!a || b']
        sent = cnf.sentence('\n'.join(clauses))
        assert sent.implicit_model() == {}

    def test_implicit2(self):
        clauses = ['a || b',
                   '!a || b',
                   'c']
        sent = cnf.sentence('\n'.join(clauses))
        assert sent.implicit_model() == {'c': True}

    def test_implicit3(self):
        clauses = ['a',
                   '!b']
        sent = cnf.sentence('\n'.join(clauses))
        assert sent.implicit_model() == {'a': True, 'b': False}        

class TestCheckModel(unittest.TestCase):

    def test_check_model1(self):
        clauses = ['a || b',
                   '!a || !b']
        sent = cnf.sentence('\n'.join(clauses))
        assert not sent.check_model({'a': False, 'b': False})
        assert not sent.check_model({'a': True, 'b': True})
        assert sent.check_model({'a': False, 'b': True})
        assert sent.check_model({'a': True, 'b': False})

    def test_check_model2(self):
        clauses =  ['!a || b || e', 
                    'a || !b', 
                    'b || !e', 
                    'd || !e', 
                    '!b || !c || !f', 
                    'a || !e', 
                    '!b || f', 
                    '!b || c']
        sent = cnf.sentence('\n'.join(clauses))
        model = {'a': False, 'b': False, 'c': True, 'd': True, 'e': False, 'f': True }
        assert sent.check_model(model)
        model = {'a': False, 'b': True, 'c': False, 'd': False, 'e': False, 'f': False }
        assert not sent.check_model(model) 
    
class TestSearchSolverBasic(unittest.TestCase):

    def test_search_solver1(self):
        clauses =  ['a || b',
                    '!a || b',
                    '!a || !b']
        result, models = search_solver(cnf.sentence('\n'.join(clauses)))
        assert result == {'a': False, 'b': True}
        assert models == [{'a': False, 'b': False}, {'a': False, 'b': True}]

    def test_search_solver2(self):
        clauses =  ['a || b',
                    '!a || !b']
        result, models = search_solver(cnf.sentence('\n'.join(clauses)))
        assert result == {'a': False, 'b': True}
        assert models == [{'a': False, 'b': False}, {'a': False, 'b': True}]

    def test_search_solver3(self):
        clauses =  ['a || b',
                    '!a || b',
                    'a || !b',
                    '!a || !b']
        result, models = search_solver(cnf.sentence('\n'.join(clauses)))
        assert result == None
        assert models == [{'a': False, 'b': False}, 
                          {'a': False, 'b': True}, 
                          {'a': True, 'b': False}, 
                          {'a': True, 'b': True}]

    def test_search_solver4(self):
        clauses =  ['a || b',
                    '!a || b || e', 
                    'a || !b', 
                    'b || !e', 
                    'd || !e', 
                    '!b || !c || !f', 
                    'a || !e', 
                    '!b || f', 
                    '!b || c']
        result, models = search_solver(cnf.sentence('\n'.join(clauses)))
        assert result == None
        assert len(models) == 64
        result, models = search_solver(cnf.sentence('\n'.join(clauses[1:])))
        assert result == {'a': False, 'b': False, 'c': False, 'd': False, 'e': False,  'f': False}
        assert models == [{'a': False, 'b': False, 'c': False, 
                           'd': False, 'e': False,  'f': False}]
        result, models = search_solver(cnf.sentence('\n'.join(clauses[:-1])))
        assert result == {'a': True, 'b': True, 'c': False, 'd': False, 'e': False,  'f': True}
        assert len(models) == 50

            
 