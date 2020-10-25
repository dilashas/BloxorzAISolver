################################################################################
#
# File:         driver.py
# Date:         Tue 11 Sep 2018  11:33
# Author:       Ken Basye
# Description:  Driver for testing bloxorz algorithms
#
################################################################################

"""
Driver for testing bloxorz algorithms

"""
from bloxorz_problem import BloxorzProblem
from bloxorz import Board
import searchGeneric
import searchBFS
import os
import glob
import pandas as pd 

if __name__ == "__main__":
    board_names = glob.glob("boards/*.blx")
    skip_boards = ['ryan.blx'   ,
                   'ben.blx'    ,
                   'cat.blx'    , 
                   'mike.blx'   ,
                   'navid.blx'  ,
                   'rayyan.blx' ,
                   'skyler.blx' ,
                   'yu.blx'     ,
                   'zongyao.blx']
  
    statsDict = {'BoardName'                       :[],
                #  'BFS_Searcher_length'             :[],
                #  'BFS_Searcher_expansions'         :[],
                 'BFS_MLP_Searcher_length'         :[],
                 'BFS_MLP_Searcher_expansions'     :[],
                #  'AStar_H1_length'                 :[],
                #  'AStar_H1_expansions'             :[],
                 'AStar_Manhattan_length'          :[],
                 'AStar_Manhattan_expansions'      :[],
                 'AStar_MLP_H1_length'             :[],
                 'AStar_MLP_H1_expansions'         :[],
                 'AStar_MLP_Manhattan_length'      :[],
                 'AStar_MLP_Manhattan_expansions'  :[]
                 }

    for board_name in board_names:

        # if board_name[7:] in skip_boards:
        #   print('Skipped ' + str(board_name[7:]))
        #   continue

        print("Loading board file %s" % (board_name,))
        with open(board_name) as file:
            board = Board.read_board(file)

        statsDict['BoardName'].append(board_name[7:])
        bp0 = BloxorzProblem(board)

        # #BFS Searcher
        # searcher = searchBFS.BFSSearcher(bp0)
        # result = searcher.search()
        # if result is None:
        #     print("For board %s, found no solution!" % (board_name,))
        #     continue

        # sequence = [arc.action for arc in result.arcs()]
        # print("For board %s, found solution with length %d using %d expansions" % (board_name, len(sequence), searcher.num_expanded))

        #BFS MultiPrune Searcher
        searcher = searchBFS.BFSMultiPruneSearcher(bp0)
        result = searcher.search()
        if result is None:
          print("For board %s, found no solution!" % (board_name,))
          statsDict['BFS_MLP_Searcher_length'].append('N/A')
          statsDict['BFS_MLP_Searcher_expansions'].append('N/A')
        else:
          sequence = [arc.action for arc in result.arcs()]
          print("For board %s, found solution with length %d using %d expansions" % (board_name, len(sequence), searcher.num_expanded))
          statsDict['BFS_MLP_Searcher_length'].append(str(len(sequence)))
          statsDict['BFS_MLP_Searcher_expansions'].append(str(searcher.num_expanded))

        if board_name[7:] in skip_boards:
          print('Skipped ' + str(board_name[7:]))
          statsDict['AStar_Manhattan_length'].append('SKIP')
          statsDict['AStar_Manhattan_expansions'].append('SKIP')
        else:
          #A Star Searcher
          bp0.heuristic = bp0.heuristic1
          searcher = searchGeneric.AStarSearcher(bp0)
          result = searcher.search()
          if result is None:
            print("For board %s, found no solution!" % (board_name,))
            statsDict['AStar_Manhattan_length'].append('N/A')
            statsDict['AStar_Manhattan_expansions'].append('N/A')
          else:
            sequence = [arc.action for arc in result.arcs()]
            print("For board %s, found solution with length %d using %d expansions" % (board_name, len(sequence), searcher.num_expanded))
            statsDict['AStar_Manhattan_length'].append(str(len(sequence)))
            statsDict['AStar_Manhattan_expansions'].append(str(searcher.num_expanded))

        # #A Star Multi Prune Searcher H1 (return 0)
        bp0.heuristic = bp0.heuristic
        searcher = searchGeneric.AStarMultiPruneSearcher(bp0)
        result = searcher.search()
        if result is None:
          print("For board %s, found no solution!" % (board_name,))
          statsDict['AStar_MLP_H1_length'].append('N/A')
          statsDict['AStar_MLP_H1_expansions'].append('N/A')
        else:
          sequence = [arc.action for arc in result.arcs()]
          print("For board %s, found solution with length %d using %d expansions" % (board_name, len(sequence), searcher.num_expanded))
          statsDict['AStar_MLP_H1_length'].append(str(len(sequence)))
          statsDict['AStar_MLP_H1_expansions'].append(str(searcher.num_expanded))


        #A Star Multi Prune Searcher Manhattan
        bp0.heuristic = bp0.heuristic1
        searcher = searchGeneric.AStarMultiPruneSearcher(bp0)
        result = searcher.search()
        if result is None:
          print("For board %s, found no solution!" % (board_name,))
          statsDict['AStar_MLP_Manhattan_length'].append('N/A')
          statsDict['AStar_MLP_Manhattan_expansions'].append('N/A')
        else:
          sequence = [arc.action for arc in result.arcs()]
          print("For board %s, found solution with length %d using %d expansions" % (board_name, len(sequence), searcher.num_expanded))
          statsDict['AStar_MLP_Manhattan_length'].append(str(len(sequence)))
          statsDict['AStar_MLP_Manhattan_expansions'].append(str(searcher.num_expanded))

    statsDf = pd.DataFrame(statsDict) 

    statsDf.to_excel("/content/drive/My Drive/CS210/Project1/Stats2.xlsx", index = False)
    #render dataframe as html
    html = statsDf.to_html(index = False)

    #write html to file
    text_file = open("/content/drive/My Drive/CS210/Project1/Stats2.html", "w")
    text_file.write(html)
    text_file.close()

    print(statsDf)
    print(); print()










