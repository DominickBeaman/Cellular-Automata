from turtle import color, width
from PIL import Image
import random
from cell import Cell
import copy

width, height = 1080, 1920
pixelsize = 40
cellwidth, cellheight = (int)(width / pixelsize), (int)(height / pixelsize)
frames = 60
cellboard = {}

def update_cells(board):
    for pos in cellboard:
        cellboard[pos].update(.1)
    for pos in cellboard:
        cellboard[pos].update_age()


for i in range(0, cellwidth):
    for j in range(0, cellheight):
        cellboard[i, j] = Cell((i, j), .1, .25, .7, [False, False, True], None, .5, 0)

for pos in cellboard:
    cellboard[pos].store_neighbors(cellboard, cellwidth, cellheight, True)

image = Image.new('RGB', (width, height), (0,0,0))

pixels = image.load()

for f in range(0,frames):
    for x in range(0, cellwidth):
        for y in range(0, cellheight):
            color = cellboard[x,y].get_color()
            for i in range(0, pixelsize):
                for j in range(0, pixelsize):
                    pixels[x*pixelsize+i,y*pixelsize+j] = color
    image.save("out/test{:04d}.png".format(f))
    update_cells(cellboard)