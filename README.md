HW: Youdoku (a.k.a. Sudoku 10)
------------------------------

Youdoku. The sudoku that puts you first.

1. All that remains at this point is to augment the SudokuBoard class 
   (in sudoku.py) so that it can use DPLL to solve itself!
   
   Create a method ```.solve()``` of sudoku.SudokuBoard that returns a
   new Sudokuboard instance corresponding to a valid completion of the
   puzzle. For instance, if
   
       board = SudokuBoard([[4, 1, 2, 3], 
                            [3, 4, 1, 2], 
                            [2, 3, 4, 1], 
                            [0, 0, 0, 0]])

   
   Then ```board.solve()``` should return a SudokuBoard instance equivalent
   to:
   
       SudokuBoard([[4, 1, 2, 3], 
                    [3, 4, 1, 2], 
                    [2, 3, 4, 1], 
                    [1, 2, 3, 4]])
                    
   If there are no valid completions,  then ```.solve()``` should
   return ```None```. If there are multiple valid completions, then any
   may be returned.
   
   Once you have a successful implementation, the following unit tests should
   succeed:
   
       python -m unittest test_part10.TestSudokuBoardSolve

2. With that method implemented, you should be able to run 
   ```python youdoku.py``` in a shell and use Youdoku. 
   
   If your implementations are not that fast, then it may run quite slowly
   (or not at all). My posted solution should be enough to run with only
   a little bit of lag on a decent laptop.
   
   Optimize the code so that it runs smoothly! This is also a great
   opportunity to add extensions, e.g.
   - you could try out conflict-driven learning (discussed in the lecture
     notes for DPLL) for speed improvements
   - you could extend the UI to support 3x3 Sudoku
   - you could improve the UI

   I'll award bonus points where appropriate, but really just do this part
   for fun.

   