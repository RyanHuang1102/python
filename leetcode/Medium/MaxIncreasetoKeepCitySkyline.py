#!/usr/bin/python

def maxIncreaseKeepingSkyline(grid):
    """
    :type grid: List[List[int]]
    :rtype: int
    807. Max Increase to Keep City Skyline
    """
    row_max, column_max = map(max, grid), map(max, zip(*grid))
    row_size = len(grid)
    column_size = len(grid[0])
    for i in range(row_size):
        for j in range(column_size):
            if row_max[i] < column_max[j]:
                grid[i][j] = row_max[i]
            else:
                grid[i][j] = column_max[j]
    print grid

grid = [[3,0,8,4],[2,4,5,7],[9,2,6,3],[0,3,1,0]]
maxIncreaseKeepingSkyline(grid)

