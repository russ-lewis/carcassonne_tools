#! /usr/bin/python3

"""A utility for displaying Carcassonne tiles.  Provides both a function that
   can be called as part of a larger program, and also a main() function which
   allows you to browse all of the tiles.
"""

import sys
import math
SQRT_2 = math.sqrt(2)

import graphics

import carcassonne_tile



def display_tile(tile, win, center, radius):
    """display_tile()

       Draws a single tile onto the selected window, at the given location.
       If it finds any impossible situations in the tile itself, then it will
       print error messages to the screen.

       Parameters:
           tile - a CarcassonneTile object
           win  - a Graphics object (see graphics.py)
           center - an (x,y) tuple, the center of the place to draw
           radius - half the width of the tile
    """
    radius  *= math.sqrt(2) 
    center_x = center[0]
    center_y = center[1]


    # this utility is useful for all sorts of invalid tiles, which we cannot
    # otherwise draw.
    def print_err(msg):
        print(msg)
        win.text(center_x,center_y, "ERR")


    edges = []
    for i in range(4):
        edge = tile.get_edge(i)
        if edge not in ["grass","grass+road","city"]:
            print_err(f"Side {i} returns an invalid edge string '{edge}'")
            return
        edges.append(edge)

    cr = tile.has_crossroads()


    win.rectangle(center_x-radius, center_y-radius, 2*radius,2*radius, fill="white")

    # NOTE: These represent *ANGLES*, not the Caracassonne side-indices!
    E  = 0
    NE = math.pi / 4
    N  = math.pi / 2
    NW = math.pi * 3/4
    W  = math.pi
    SW = math.pi * 5/4
    S  = math.pi * 3/2
    SE = math.pi * 7/4

    for i in range(4):
        # we draw each side using the same code, by adding a rotation-specific
        # constant to all of the angles we use.  We'll draw everything using
        # a NORTH edge as our baseline; for each additional value of i, we'll
        # rotate by 90 degrees clockwise, which is -pi/2 in mathematics.
        rot = i * (-math.pi/2)

        # BUGFIX: Graphics uses a downward-pointing y axis.  So we have to
        #         make each y calculation *subtraction*

        # the simplest way to draw an edge is a triangle: either brown or
        # green (we add roads as a second pass).  However, there are two
        # exceptions: a city tile which is not adjacent to anything else
        # (draw a trapezoid, shallow, so that adjacent trapezoids don't
        # touch), or a grass section where the two adjacent sides are both
        # cities, *and* they are connected (crop your own triangle with
        # some city color).  See tiles 7,8,14 to see these weird cases.

        # points 1,2,3 represent the corners of the triangle
        x1 = center_x
        y1 = center_y

        x2 = center_x + radius * SQRT_2 * math.cos(NW+rot)
        y2 = center_y - radius * SQRT_2 * math.sin(NW+rot)

        x3 = center_x + radius * SQRT_2 * math.cos(NE+rot)
        y3 = center_y - radius * SQRT_2 * math.sin(NE+rot)

        # points 4,5 are only used in the special cases; they represent
        # the "upper" corners of the trapezoid.  If necessary, we'll do a
        # second step, which shoves these a little bit toward the edge, to
        # make the trapezoid shallow.
        x4 = center_x + (radius/2) * SQRT_2 * math.cos(NW+rot)
        y4 = center_y - (radius/2) * SQRT_2 * math.sin(NW+rot)

        x5 = center_x + (radius/2) * SQRT_2 * math.cos(NE+rot)
        y5 = center_y - (radius/2) * SQRT_2 * math.sin(NE+rot)

        # special case 1 - shallow trapezoid?
        if edges[i] == "city" and \
           tile.city_connects(i, (i+1)%4) == False and \
           tile.city_connects(i, (i+2)%4) == False and \
           tile.city_connects(i, (i+3)%4) == False:
            # we adjust the points 4,5 "north" (rotated) by a little bit
            x4 += (radius/10) * math.cos(N+rot)
            y4 -= (radius/10) * math.sin(N+rot)

            x5 += (radius/10) * math.cos(N+rot)
            y5 -= (radius/10) * math.sin(N+rot)

            trap_color = "brown"
            tri_color  = "green"

        # special case 2 - give the point of our triangle to the city?
        elif edges[i] != "city" and \
            edges[(i+1)%4] == "city" and \
            tile.city_connects( (i+1)%4, (i+3)%4 ):

            trap_color = "green"
            tri_color  = "brown"

        # ordinary case
        else:
            trap_color = None
            tri_color  = "green" if edges[i].startswith("grass") else "brown"

        win.triangle(x1,y1, x2,y2, x3,y3, fill=tri_color)

        if trap_color is not None:
            win.triangle(x2,y2, x4,y4, x5,y5, fill=trap_color)
            win.triangle(x2,y2, x5,y5, x3,y3, fill=trap_color)

    # draw the roads (if any) *LAST*, so that they will overwrite the rest of
    # the drawn elements.
    for i in range(4):
        if edges[i] == "grass+road":
            rot = i * (-math.pi/2)

            x1 = center_x
            y1 = center_y

            x2 = center_x + .75*radius * math.cos(N+rot)
            y2 = center_y - .75*radius * math.sin(N+rot)

            win.line(x1,y1, x2,y2, fill="white", width=radius/10)

    # is there a crossroads to draw?  That's a black square on top of the roads.
    if cr:
        win.rectangle(center_x-radius/10,center_y-radius/10, radius/5,radius/5, fill="black")



def get_tile_array():
    retval = [("Tile 01", carcassonne_tile.tile01),
              ("Tile 02", carcassonne_tile.tile02),
              ("Tile 03", carcassonne_tile.tile03),
              ("Tile 04", carcassonne_tile.tile04)]

    try:
        retval.append( ("Tile 05", carcassonne_tile.tile05) )
        retval.append( ("Tile 06", carcassonne_tile.tile06) )
        retval.append( ("Tile 07", carcassonne_tile.tile07) )
        retval.append( ("Tile 08", carcassonne_tile.tile08) )
        retval.append( ("Tile 09", carcassonne_tile.tile09) )
        retval.append( ("Tile 10", carcassonne_tile.tile10) )
        retval.append( ("Tile 11", carcassonne_tile.tile11) )
        retval.append( ("Tile 12", carcassonne_tile.tile12) )
        retval.append( ("Tile 13", carcassonne_tile.tile13) )
        retval.append( ("Tile 14", carcassonne_tile.tile14) )
        retval.append( ("Tile 15", carcassonne_tile.tile15) )
        retval.append( ("Tile 16", carcassonne_tile.tile16) )
    except:
        print(f"WARNING: Only {len(retval)} tiles could be found.")

    return retval



def main():
    win = graphics.graphics(400,450, "Tile Browser")

    tiles = get_tile_array()

    # I need to create this variable here, so that the helper function
    # can find it.
    cur_indx = 0

    def key_handler(win, key):
        nonlocal cur_indx

        key = key.lower()
        if key == 'q':
            sys.exit(0)
        if key == 'n':
            cur_indx += 1
            cur_indx %= len(tiles)
            draw()
        if key == 'p':
            cur_indx -= 1
            cur_indx %= len(tiles)
            draw()


    def draw():
        name = tiles[cur_indx][0]
        tile = tiles[cur_indx][1]
        win.clear()
        display_tile(tile, win, (200,200), 200)
        win.text(175,410, name)


    win.set_keyboard_action(key_handler)
    draw()
    win.mainloop()

#    while True:
#        for name,tile in tiles:



if __name__ == "__main__":
    main()

