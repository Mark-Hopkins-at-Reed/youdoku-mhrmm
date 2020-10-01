import unittest
from sudoku import SudokuBoard

class TestSudokuBoardSolve(unittest.TestCase):    

    def test_solve1(self):
        board = SudokuBoard([[0, 0, 0, 3], 
                             [0, 0, 0, 2], 
                             [3, 0, 0, 0], 
                             [4, 0, 0, 0]])
        solved = board.solve()
        expected = '\n'.join(['2413',
                              '1342',
                              '3124',
                              '4231'])
        assert str(solved) == expected
        
    def test_solve2(self):
        board = SudokuBoard([[4, 1, 2, 3], 
                             [2, 3, 4, 1], 
                             [3, 4, 1, 2], 
                             [0, 0, 0, 0]])
        solved = board.solve()
        expected = '\n'.join(['4123',
                              '2341',
                              '3412',
                              '1234'])
        assert str(solved) == expected
        
    def test_solve3(self):
        board = SudokuBoard([[0, 0, 0, 3], 
                             [0, 0, 0, 2], 
                             [3, 3, 0, 0], 
                             [4, 0, 0, 0]])
        assert board.solve() == None
        
    def test_solve4(self):
        board = SudokuBoard([[2, 0, 0, 3], 
                             [0, 0, 0, 2], 
                             [0, 3, 1, 0], 
                             [4, 0, 0, 0]])
        assert board.solve() == None
 
 