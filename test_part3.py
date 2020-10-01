import unittest
import cnf


class TestLiteral(unittest.TestCase):
    
    def test_literal_eq(self):
        assert cnf.l('!a') == cnf.l('!a')
        assert cnf.l('a') == cnf.l('a')
        assert cnf.l('!a') != cnf.l('!b')
        assert cnf.l('!a') != cnf.l('a')
        assert cnf.l('a') != cnf.l('b')
        
    def test_literal_hash(self):
        assert len(set([cnf.l('!a'), cnf.l('!a'), cnf.l('b'), cnf.l('!c'), cnf.l('b')])) == 3

class TestClause(unittest.TestCase):
    
    def test_clause_eq(self):
        assert cnf.c('!c || d') == cnf.c('!c || d')
        assert cnf.c('d || !c') == cnf.c('!c || d')
        assert cnf.c('!c || d') != cnf.c('!c || !d')

    def test_clause_lt(self):
        assert cnf.c('a || b || e') < cnf.c('b || c || e')
           
    def test_clause_getitem(self):
        c1 = cnf.c('!a || b || e')
        assert c1['b'] 
        assert not c1['a']
        
    def test_clause_bool(self):    
        assert bool(cnf.c('a'))
        assert not bool(cnf.c('FALSE'))

    def test_clause_symbols(self):        
        c1 = cnf.c('!a || b || e')        
        assert c1.symbols() == {'a', 'b', 'e'}

    def test_clause_remove(self):        
        c1 = cnf.c('!a || b || e')        
        c2 = c1.remove('a')
        assert c2 == cnf.c('b || e')
        c3 = c1.remove('b')
        assert c3 == cnf.c('!a || e')
        c4 = c1.remove('d')
        assert c4 == c1
        
    def test_clause_hash(self):
        size = len(set([cnf.c('d || !c'), 
                        cnf.c('!c || d'), 
                        cnf.c('b'), 
                        cnf.c('!c || d || !e'), 
                        cnf.c('d || !e || !c')]))
        assert size == 3
        
    def test_clause_str(self):
        assert str(cnf.c('!c || d')) == '!c || d'
        assert str(cnf.c('FALSE')) == 'FALSE'
        
    def test_clause_in(self):
        assert 'a' in cnf.c('!a || !c')
        assert 'b' not in cnf.c('!a || !c')
        assert 'c' in cnf.c('!a || !c')
       

class TestSentence(unittest.TestCase):
    
    def test_sent_symbols(self):
        sent = cnf.sentence('\n'.join(['!a || b || e', 
                                       'a || !b', 
                                       'b || !e', 
                                       'd || !e', 
                                       '!b || !c || !f', 
                                       'a || !e', 
                                       '!b || f',
                                       '!b || c']))
        assert sent.symbols() == {'a', 'b', 'c', 'd', 'e', 'f'}
    
    def test_sent_str(self):
        sent = cnf.sentence('\n'.join(['!a || b || e', 
                                       'a || !b', 
                                       'b || !e']))
        assert str(sent) == '\n'.join(['!a || b || e', 
                                       'a || !b', 
                                       'b || !e'])
