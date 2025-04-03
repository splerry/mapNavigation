# mapNavigation
Project demonstrating mastery of advanced search algorithms (greedy best-first-search and A Star) by mapping paths between state capitols. This project was developed using a specific given set of distances between state capitols, not the actual distances. Please check the supplied .csv files for the distances used. Made as an assignment for Intro to Artificial Intelligence @ Illinois Institute of Technology

To run:
1) requires both supplied .csv files to be in the same directory as mapNavigation.py
2) through the command line, navigate to said directory
3) py ./mapNavigation.py START_STATE END_STATE
   where START_STATE is the fully capitalized two-letter abbreviation of the starting position state, ie. Illinois -> IL, and END_STATE is the same abbreviation of the goal state
   example:

  $ py ./mapNavigation.py IL TX

  Initial state: IL
  Goal state: TX
  
  Greedy Best First Search:
  Solution: IL, MO, AR, TX
  Number of expanded nodes: 14
  Number of stops on path: 4
  Execution time: 0.0
  Complete path cost: 1054
  
  A* Search:
  Solution: IL, MO, OK, TX
  Number of expanded nodes: 16
  Number of stops on path: 4
  Execution time: 0.0
  Complete path cost: 1003
