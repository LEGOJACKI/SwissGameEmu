import pygame
import math

screen = pygame.display.set_mode((500, 240))

tilemap = [[2]*15]*15 #15x15 map of 16x16 tiles

def tileLoad(filename): #Assuming tilemap as
    tileset = []
    image = pygame.image.load(filename).convert()
    for i in range(0, 225):
        tileset.append(image.subsurface((0, i*16, 16, 16)))
    return tileset

def mapLoad(filename): 
    finalMap = open(filename).read().split("\n")
    for column in range(0, len(finalMap)):
        finalMap[column] = finalMap[column].split(",")
    for x in range(0, 15):
        for y in range(0, 15):
            finalMap[x][y] = int(finalMap[x][y])
    finalMap = [[finalMap[j][i] for j in range(len(finalMap))] for i in range(len(finalMap[0]))] 
    return finalMap

def mapSave(tilemap, filename):
    lines = [""] * 15
    for column in range(0, 15):
        for tile in range(0, 15):
            lines[column] += str(tilemap[tile][column]) + ","
    file = open(filename, mode='w')
    for line in range(0, len(lines)):
        if (line == 14):
            lines[line] = lines[line][0:len(lines[line])-1]
        else:
            lines[line] = lines[line][0:len(lines[line])-1] + "\n"
        file.write(lines[line])
    file.close()

def tileDrawAll(tileset, tilemap):
    for x in range(0, 15):
        for y in range(0, 15):
            screen.blit(tileset[tilemap[x][y]], (x*16, y*16))

def tileDrawDiff(tileset, diffs): #Diff is 2d array of vectors, x, y, newTileIndex
    for diff in diffs:
        screen.blit(tileset[diff[2]], (diff[0]*16, diff[1]*16))

def debugDrawTileset(tileset):
    tile = 0
    for x in range(0, 15):
        for y in range(0, 15):
            screen.blit(tileset[tile], (260+(x*16), y*16))
            tile += 1
mapName = "map1.txt"
tileset = tileLoad("tileset.png")
tilemap = mapLoad(mapName)
tileDrawAll(tileset, tilemap)
debugDrawTileset(tileset)


done = False
currentTile = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] > 260:
                currentTile = (math.floor(event.pos[1]/16) + 15*math.floor((event.pos[0]-260)/16))
                print(currentTile)
            elif event.pos[0] < 240:
                if screen.get_width() == 500:
                    point = (math.floor(event.pos[0]/16), math.floor(event.pos[1]/16))
                    tilemap[point[0]][point[1]] = currentTile
                    tileDrawDiff(tileset, [[point[0], point[1], currentTile]])
        if event.type == pygame.DROPFILE:
            mapSave(tilemap, mapName)
            mapName = event.file
            tilemap = mapLoad(mapName)
            tileDrawAll(tileset, tilemap)
    pygame.display.flip()

pygame.quit()
mapSave(tilemap, mapName)
exit()
