import unittest
import cnf
from resolution import resolve_symbol, resolve, ClauseQueue



class TestClauseDisjunction(unittest.TestCase):
        
    def test_clause_disjunction1(self):
        result = cnf.c('!a || b') | cnf.c('c || !e')
        assert result == cnf.c('!a || b || c || !e') 

    def test_clause_disjunction2(self):
        result = cnf.c('!a || b') | cnf.c('b || c || !e')
        assert result == cnf.c('!a || b || c || !e')

    def test_clause_disjunction3(self):
        result = cnf.c('FALSE') | cnf.c('!b || c || !e')
        assert result == cnf.c('!b || c || !e')

    def test_clause_disjunction4(self):
        assert cnf.c('!a || b') | cnf.c('!b || c || !e') == None

    def test_clause_disjunction5(self):
        assert cnf.c('FALSE') | cnf.c('FALSE') == cnf.c('FALSE')
        
        
        
class TestResolveSymbol(unittest.TestCase):
        
    def test_resolve_symbol1(self):
        resolvent = resolve_symbol(cnf.c('!b || !c'), cnf.c('b || d'), 'b')
        assert resolvent == cnf.c('d || !c')

    def test_resolve_symbol2(self):
        resolvent = resolve_symbol(cnf.c('!b || !c || e'), cnf.c('b || d'), 'b')
        assert resolvent == cnf.c('d || !c || e')

    def test_resolve_symbol3(self):
        resolvent = resolve_symbol(cnf.c('!b || !c'), cnf.c('b || d'), 'c')
        assert resolvent == None

    def test_resolve_symbol4(self):
        resolvent = resolve_symbol(cnf.c('b || !c'), cnf.c('b || d'), 'b')
        assert resolvent == None

    def test_resolve_symbol5(self):
        resolvent = resolve_symbol(cnf.c('!b || !c'), cnf.c('b || c || e || d'), 'b')
        assert resolvent == None

    def test_resolve_symbol6(self):
        resolvent = resolve_symbol(cnf.c('!b || !c'), cnf.c('b || !c || e || d'), 'b')
        assert resolvent == cnf.c('d || !c || e')
 
        
class TestResolve(unittest.TestCase):

    def test_resolve1(self):
        resolvents = resolve(cnf.c('!b || !c'), cnf.c('b || d'))
        assert resolvents == [cnf.c('!c || d')]
        
    def test_resolve2(self):
        resolvents = resolve(cnf.c('!b || !c'), cnf.c('b || c || d'))
        assert resolvents == []
        
    def test_resolve3(self):
        resolvents = resolve(cnf.c('!b || !c'), cnf.c('b || !c || d'))
        assert resolvents == [cnf.c('!c || d')]
    
    def test_resolve4(self):
        resolvents = resolve(cnf.c('!b || !c || e || !f'), cnf.c('b || d'))
        assert resolvents == [cnf.c('!c || d || e || !f')]


class TestClauseQueue(unittest.TestCase):
    
    def test_queue1(self):
        queue = ClauseQueue()
        assert queue.empty()
        assert queue.pop() == None
        
    def test_queue2(self):
        queue = ClauseQueue()
        assert queue.push(cnf.c('!b || !c'))
        assert not queue.empty()
        assert queue.push(cnf.c('b'))
        assert queue.push(cnf.c('!b || c || d'))
        assert not queue.push(cnf.c('!b || !c'))
        assert queue.pop() == cnf.c('b')
        assert queue.pop() == cnf.c('!b || !c')
        assert not queue.empty()
        assert queue.pop() == cnf.c('!b || c || d')
        assert queue.pop() == None
        assert queue.empty()
        
   