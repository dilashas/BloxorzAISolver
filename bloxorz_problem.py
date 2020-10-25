##############################################################################
#
# File:         bloxorz_problem.py
# Date:         Wed 31 Aug 2011  11:40
# Author:       Ken Basye
# Description:  Bloxorz search problem
#
##############################################################################

import cs210_utils
from searchProblem import Arc, Search_problem
import searchGeneric
import searchBFS
# import searchBranchAndBound
import io
from bloxorz import Board
from bloxorz import next_position

class BloxorzProblem(Search_problem):
    """
    >>> board_string = (
    ... '''BLOX 1
    ... 5 3
    ... X X X O O
    ... S X G X O
    ... W W W W X
    ... ''')
    
    >>> fake_file = io.StringIO(board_string)
    >>> board0 = Board.read_board(fake_file)
    >>> bp0 = BloxorzProblem(board0)
    >>> bp0.start
    ((0, 1), (0, 1))

    >>> searcher = searchBFS.BFSSearcher(bp0) 
    >>> path = searcher.search()  
    2507 paths have been expanded and 2399 paths remain in the frontier

    >>> path  
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))
    
    >>> a_pos, b_pos = path.end() 
    >>> a_pos == b_pos == board0.goal 
    True

    >>> searcher = searchBFS.BFSMultiPruneSearcher(bp0)
    >>> path = searcher.search() 
    16 paths have been expanded and 1 paths remain in the frontier

    >>> path   
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

    >>> searcher = searchGeneric.AStarSearcher(bp0)
    >>> path = searcher.search()  
    1259 paths have been expanded and 1880 paths remain in the frontier

    >>> path   
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))


    >>> bp0.heuristic = bp0.heuristic1  
    >>> searcher = searchGeneric.AStarSearcher(bp0)
    >>> path = searcher.search()  
    1113 paths have been expanded and 1793 paths remain in the frontier

    >>> path   
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

    >>> bp0.heuristic = bp0.heuristic1  
    >>> searcher = searchGeneric.AStarMultiPruneSearcher(bp0)
    >>> path = searcher.search()   
    15 paths have been expanded and 1 paths remain in the frontier

    >>> path   
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

"""
    def __init__(self, board):
        """
        Build a problem instance from a board
        """
        self.board = board
        self.start = (board.start, board.start)
        self.goal = (board.goal, board.goal)
        
    def start_node(self):
        """Returns start node"""
        return self.start
    
    def is_goal(self,node):
        """Returns True if node is a goal"""
        return node == self.goal

    def neighbors(self,node):
      """
      Given a node, return a sequence of Arcs usable
      from this node. 
      """
      arcs = []
      ACTIONS = tuple(('U', 'D', 'L', 'R'))
      for action in ACTIONS:
        next_pos = next_position(node, action)
        if Board.legal_position(self.board, next_pos):
          newArc = Arc(node, next_pos, cost = 1, action=action)
          arcs.append(newArc)
      return arcs


    def heuristic(self, node):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden."""
        return 0

    def heuristic1(self, node):
      """Gives the heuristic value of node n.
      Returns 0 if not overridden."""
      manhattan = 0.0

      #Coordinates of the goal
      goal_xCoord = self.goal[0][0]
      goal_yCoord = self.goal[0][1]
      
      #Coordinates of the current position
      tile1_xCoord = node[0][0]
      tile1_yCoord = node[0][1]

      tile2_xCoord = node[1][0]
      tile2_yCoord = node[1][1]

      #Calculating the difference between the goal and the current position
      #Tile 1
      diff1_tile_xCoord = abs(goal_xCoord - tile1_xCoord)
      diff1_tile_yCoord = abs(goal_yCoord - tile1_yCoord)

      #Tile 2
      diff2_tile_xCoord = abs(goal_xCoord - tile2_xCoord)
      diff2_tile_yCoord = abs(goal_yCoord - tile2_yCoord)

      #Finding the minimum distance
      min_xCoord = min(diff1_tile_xCoord, diff2_tile_xCoord)
      min_yCoord = min(diff1_tile_yCoord, diff2_tile_yCoord)

      #Finding the manhattan distance
      manhattan = (min_xCoord + min_yCoord)/1.5

      return manhattan


if __name__ == '__main__':
    cs210_utils.cs210_mainstartup()

