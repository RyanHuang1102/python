#!/usr/bin/python

def numTilePossibilities(tiles):
    """
    :type tiles: str
    :rtype: int
    1079. Letter Tile Possibilities
    """
    numbers_char=[0 for i in range(26)]
    size = len(tiles)
    print tiles[1]-'A'
    """
    for i in size:
        numbers_char[tiles[i]-'A']+=1
    print numbers_char
    """
Input = "AAB"
numTilePossibilities(Input)
