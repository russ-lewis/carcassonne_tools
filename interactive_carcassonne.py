#! /usr/bin/python3

import sys
import random

import carcassonne_tile
import carcassonne_map

import graphics
import display_carcassonne_tiles
import display_carcassonne_map



# this is a property of the code, so it's a constant...so I'm OK making it
# a global.
TILES = display_carcassonne_tiles.get_tile_array()



class WindowState:
    def __init__(self):
        self._x = self._y = 0
        self._tile_indx = 0
        self._cur_tile = TILES[0][1]     # different than the index because it might be rotated

    def draw_highlight(self, win, x,y, color, cx,cy,rad,spac):
        this_cx = cx + x*spac
        this_cy = cy - y*spac

        top = this_cy - rad
        bot = this_cy + rad

        lft = this_cx - rad
        rgt = this_cx + rad

        wid = 2*(spac/2 - rad)

        win.line(lft,top, rgt,top, fill=color, width=wid)
        win.line(rgt,top, rgt,bot, fill=color, width=wid)
        win.line(rgt,bot, lft,bot, fill=color, width=wid)
        win.line(lft,bot, lft,top, fill=color, width=wid)

    def draw_cursor(self, win, cx,cy,rad,spac):
        self.draw_highlight(win,
                            self._x, self._y, "red",
                            cx,cy,rad,spac)
    def draw_origin(self, win, cx,cy,rad,spac):
        self.draw_highlight(win,
                            0,0, "black",
                            cx,cy,rad,spac)

    def draw_sidebar(self, win):
        display_carcassonne_tiles.display_tile(self._cur_tile, win, (700,100), 50)

        win.text(675,175, TILES[self._tile_indx][0])

        win.text(620,300, " n,p   - change tiles\n"
                          " r  - rotate tile\n"
                          "arrows - move\n"
                          "ENTER  - place tile\n"
                          " q  - quit\n"
                          " t  - test trace_road_1_dir\n"
                          " y  - test trace_road\n"
                          " u  - test trace_city\n" , size=12)

    def next(self):
        self._tile_indx += 1
        self._tile_indx %= len(TILES)
        self._cur_tile = TILES[self._tile_indx][1]
    def prev(self):
        self._tile_indx -= 1
        self._tile_indx %= len(TILES)
        self._cur_tile = TILES[self._tile_indx][1]

    def rotate(self):
        self._cur_tile = self._cur_tile.rotate()

    def randomize(self):
        self._tile_indx = random.randint(0, len(TILES)-1)
        self._cur_tile  = TILES[self._tile_indx][1]
    def random_rotate(self):
        for _ in range(random.randint(0,3)):
           self.rotate()
    def random_location(self, game):
        locations = sorted(game.find_map_border())
        chosen    = random.randint(0,len(locations)-1)
        self._x,self._y = locations[chosen]

    def up(self):
        self._y += 1
    def down(self):
        self._y -= 1
    def left(self):
        self._x -= 1
    def right(self):
        self._x += 1

    def add(self, game):
        game.add(self._x, self._y, self._cur_tile)



def redraw(win, game, win_state):
    win.clear()

    (cx,cy,rad,spac) = display_carcassonne_map.display_map(game, win, 600)

    win_state.draw_cursor(win, cx,cy,rad,spac)
    win_state.draw_origin(win, cx,cy,rad,spac)

    win_state.draw_sidebar(win)




def key_callback(win, game, win_state, event):
    if event.lower() == 'q':
        sys.exit(0)

    if event == "n":
        win_state.next()
    elif event == "p":
        win_state.prev()
    elif event == "r":
        win_state.rotate()

    elif event == "x":
        win_state.randomize()
    elif event == "X":
        win_state.randomize()
        win_state.random_rotate()
        win_state.random_location(game)

    elif event == "Up":
        win_state.up()
    elif event == "Down":
        win_state.down()
    elif event == "Left":
        win_state.left()
    elif event == "Right":
        win_state.right()

    elif event == "Return":
        win_state.add(game)
    
    elif event =="t":
        print('Side? 0 = North, 1 = East, 2 = South, 3 = West')
        side = int(input())
        print(f'Testing trace_road_one_direction for {win_state._x,win_state._y,side}...')
        x = game.trace_road_one_direction(win_state._x,win_state._y,side)
        print()
        print()
        print('Pathway :',x)

    elif event =="y":
        print('Side? 0 = North, 1 = East, 2 = South, 3 = West')
        side = int(input())
        print(f'Testing trace_road for {win_state._x,win_state._y,side}...')
        x = game.trace_road(win_state._x,win_state._y,side)
        print()
        print()
        print('Pathway :',x)

    elif event =="u":
        print('Side? 0 = North, 1 = East, 2 = South, 3 = West')
        side = int(input())
        print(f'Testing trace_city for {win_state._x,win_state._y,side}...')
        x = game.trace_city(win_state._x,win_state._y,side)
        print()
        print()
        print('City edges:',x[0])
        print()
        print()
        print('Complete City?',x[0])
        print()
        print()
        print(f'There are {len(x[1])} edges in this city')

    else:
        print(f"Unrecognized keystroke: '{event}'")
        return

    redraw(win,game,win_state)



def main():
    game      = carcassonne_map.CarcassonneMap()
    win_state = WindowState()

    win = graphics.graphics(800,600, "Place Tiles on the Carcassonne Map")
    win.set_keyboard_action( lambda ignored_,event: key_callback(win,game,win_state, event) )

    redraw(win, game, win_state)
    win.mainloop()

if __name__ == "__main__":
    main()

