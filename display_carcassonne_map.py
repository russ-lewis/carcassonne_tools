#! /usr/bin/python3

"""A utility for displaying a Carcassonne map.  Provides a function that can be
   can be called as part of a larger program.
"""

import sys
import math

import graphics

import carcassonne_map
import carcassonne_tile

import display_carcassonne_tiles



def display_map(game, win, size):
    """display_map()

       Draws an entire Carcassonne map onto the selected window, at the given
       location.  It will never draw tiles larger than 100x100, but if the map
       is very large, it will scale the tiles smaller than that, so that things
       will fit.

       Parameters:
           tile - a CarcassonneTile object
           win  - a Graphics object (see graphics.py)
           size - the width and height of the draw area, in pixels

       Returns:
           a tuple (cx,cy, rad, spac):
               cx,cy - the pixel location of the center of the (0,0) tile
               rad   - the radius of the tiles as drawn
               spac  - the spacing between the tiles, a tiny bit more than the radius
    """

    min_x = max_x = min_y = max_y = 0
    for (x,y) in game.get_all_coords():
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y

    wid_tiles = max_x-min_x+1
    hei_tiles = max_y-min_y+1

    spac = min(100, size/max(wid_tiles,hei_tiles))
    rad  = spac/2 * .99

    cx = spac * (-min_x+.5)
    cy = spac * ( max_y+.5)

    # if the map is small, then the cx,cy above can put us up on the top-left corner,
    # that's not desirable.
    if cx + spac*(max_x) < size:
        cx = size/2 - spac*(max_x+min_x)/2
    if cy + spac*(max_y) < size:
        cy = size/2 + spac*(max_y+min_y)/2

    for (x,y) in game.get_all_coords():
        this_cx = cx + spac*x
        this_cy = cy - spac*y
        tile = game.get(x,y)
        display_carcassonne_tiles.display_tile(tile, win, (this_cx,this_cy), rad)

    return (cx,cy,rad,spac)



def display_map_in_new_window(game):
    win = graphics.graphics(600,600, "Map Display")
    display_map(game,win, 600)
    win.mainloop()



def main():
    game = carcassonne_map.CarcassonneMap()
    game.add( 1,0, carcassonne_tile.tile03)
    game.add(-1,0, carcassonne_tile.tile04)
    game.add( 1,1, carcassonne_tile.tile03)
    game.add(-1,1, carcassonne_tile.tile05)
    game.add( 0,1, carcassonne_tile.tile11.rotate().rotate().rotate())

    display_map_in_new_window(game)



if __name__ == "__main__":
    main()

