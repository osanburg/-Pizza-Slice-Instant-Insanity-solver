# Pizza-Slice-Instant-Insanity-solver

Python program which solves a variation of Instant insanity puzzle.

Rules of the Puzzle:
- puzzle consists of a triangular vertical column with 9 horizontal slices.
- the puzzle contains 3 copies of each number from 1 to 9 with each side of a slice containing a number
- each slice can be rotated but flipping a slice may or may not be allowed
- objective: rotate(and flip) the slices of the puzzle so that every number on each side is unique

How the program works:
- generate each puzzle and exhaustively search for solution using every possible rotation
- if no solution is found and puzzle is impossible, then find the minimum obstacle for the puzzle,
  that is find the smallest number of slices that need to be present for the puzzle to remain unsolvable
- if the puzzle was unsolvable then show the solution where flipping the slices is allowed
