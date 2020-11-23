#########################################
# Programmer: Mrs.G, Ron Varshavsky
# Date: 21/11/2015 05-06/2020
# File Name: RonVarsahvksy_tetris_classes.py
# Description: These are classes for the Tetris game.
#########################################
import pygame

BLOCKSIZE = 25 # must be the same as gridsize

#---------------------------------------#
#   load colours & block images         #
#---------------------------------------#
BLACK_CLR = (42 , 42 , 87 )
WHITE_CLR = (255, 255, 255)
BLACK     = pygame.image.load("black_block.png")#(  0,  0,  0)  
BLACK     = pygame.transform.scale(BLACK,(BLOCKSIZE,BLOCKSIZE))                     
RED       = pygame.image.load("red_block.png")#(255,  0,  0)
RED       = pygame.transform.scale(RED,(BLOCKSIZE,BLOCKSIZE))
GREEN     = pygame.image.load("green_block.png")
GREEN     = pygame.transform.scale(GREEN,(BLOCKSIZE,BLOCKSIZE))
BLUE      = pygame.image.load("blue_block.png")#(  0,  0,255)
BLUE      = pygame.transform.scale(BLUE,(BLOCKSIZE,BLOCKSIZE))                     
ORANGE    = pygame.image.load("orange_block.png")
ORANGE    = pygame.transform.scale(ORANGE,(BLOCKSIZE,BLOCKSIZE))                 
CYAN      = pygame.image.load("cyan_block.png")#(  0,183,235)
CYAN      = pygame.transform.scale(CYAN,(BLOCKSIZE,BLOCKSIZE)) 
MAGENTA   = pygame.image.load("magenta_block.png")#(255,  0,255) 
MAGENTA   = pygame.transform.scale(MAGENTA,(BLOCKSIZE,BLOCKSIZE))                   
YELLOW    = pygame.image.load("yellow_block.png")
YELLOW    = pygame.transform.scale(YELLOW,(BLOCKSIZE,BLOCKSIZE))      
WHITE     = pygame.image.load("white_block.png")#(255,255,255)
WHITE    = pygame.transform.scale(WHITE,(BLOCKSIZE,BLOCKSIZE))
GRAY      = pygame.image.load("shadow_block.png")
GRAY      = pygame.transform.scale(GRAY,(BLOCKSIZE,BLOCKSIZE))
COLOURS   = [ BLACK,  RED,  GREEN,  BLUE,  ORANGE,  CYAN,  MAGENTA,  YELLOW,  WHITE ]
CLR_names = ['black','red','green','blue','orange','cyan','magenta','yellow','white']
figures   = [  None , 'Z' ,  'S'  ,  'J' ,  'L'   ,  'I' ,   'T'   ,   'O'  , None  ]

class Block(object):                    
    """ A square - basic building block
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        self.col = col #a block has positions & a colour                 
        self.row = row                  
        self.clr = clr

    def __str__(self):                  
        return '('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def draw(self, surface, gridsize=20):                     
        x = self.col * gridsize #x & y positions        
        y = self.row * gridsize
        CLR = COLOURS[self.clr] #colour (image)
        surface.blit(CLR,(x,y)) # blit the image based on colour


    def _draw_shadow(self, surface, gridsize=20):
        x = self.col * gridsize        
        y = self.row * gridsize
        CLR = GRAY #exactly the same as draw() but always draws it gray
        surface.blit(GRAY, (x, y))

    def move_down(self):                
        self.row = self.row + 1 # move block down one row
            

#---------------------------------------#
class Cluster(object):
    """ Collection of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        self.col = col                    
        self.row = row                   
        self.clr = 0                          
        self.blocks = [Block()]*blocksNo      
        self._colOffsets = [0]*blocksNo  #@@
        self._rowOffsets = [0]*blocksNo  #@@
        # essentially an array of blocks

    def _update(self):
        for i in range(len(self.blocks)):
            blockCOL = self.col+self._colOffsets[i] #@@
            blockROW = self.row+self._rowOffsets[i] #@@
            blockCLR = self.clr
            self.blocks[i]= Block(blockCOL, blockROW, blockCLR)
            # private function to update block position

    def draw(self, surface, gridsize):                     
        for block in self.blocks:
            block.draw(surface, gridsize)
            # draw the blocks

    def collides(self, other):
        """ Compare each block from a cluster to all blocks from another cluster.
            Return True only if there is a location conflict.
        """
        for block in self.blocks:
            for obstacle in other.blocks:
                if block.col == obstacle.col and block.row == obstacle.row:
                    return True
        return False
    
    def append(self, other): 
        """ Append all blocks from another cluster to this one.
        """
###########################################################################################
# 9.  Add code here that appends the blocks of the other object to the self.blocks list.
#     Use a for loop to take each individual block from the other.blocks list 
############################################################################################
        for obs in other.blocks:
            self.blocks.append(obs)

#---------------------------------------#
class Obstacles(Cluster):
    """ Collection of tetrominoe blocks on the playing field, left from previous shapes.
        
    """        
    def __init__(self, col = 0, row = 0, blocksNo = 0):
        Cluster.__init__(self, col, row, blocksNo)      # initially the playing field is empty(no shapes are left inside the field)

    def show(self):
        print("\nObstacle: ")
        for block in self.blocks:
            print (block)

    def findFullRows(self, top, bottom, columns):
        fullRows = []
        rows = []
        for block in self.blocks:                       
            rows.append(block.row)                      # make a list with only the row numbers of all blocks
            
        for row in range(top, bottom):                  # starting from the top (row 0), and down to the bottom
            if rows.count(row) == columns:              # if the number of blocks with certain row number
                fullRows.append(row)                    # equals to the number of columns -> the row is full
        return fullRows                                 # return a list with the full rows' numbers


    def removeFullRows(self, fullRows):
        for row in fullRows:                            # for each full row, STARTING FROM THE TOP (fullRows are in order)
            for i in reversed(range(len(self.blocks))): # check all obstacle blocks in REVERSE ORDER,
                                                        # so when popping them the index doesn't go out of range !!!
                if self.blocks[i].row == row:
                    self.blocks.pop(i)                  # remove each block that is on this row
                elif self.blocks[i].row < row:
                    self.blocks[i].move_down()          # move down each block that is above this row
    def removeAllRows(self, fullRows):
        for row in fullRows:                            # for each full row, STARTING FROM THE TOP (fullRows are in order)
            for i in reversed(range(len(self.blocks))): # check all obstacle blocks in REVERSE ORDER,                                        # so when popping them the index doesn't go out of range !!!
                if self.blocks[i].row == row:
                    self.blocks.pop(i)
   
#---------------------------------------#
class Shape(Cluster):                     
    """ A tetrominoe in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate
                * figure/shape is defined by the colour
            rot - rotation             
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        Cluster.__init__(self, col, row, 4)
        self.clr = clr
        self._rot = 1
        self._colOffsets = [-1, 0, 0, 1] #@@
        self._rowOffsets = [-1,-1, 0, 0] #@@
        self._rotate() #@@
        
    def __str__(self):                  
        return figures[self.clr]+' ('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def set_to(self, other, col = 1, row = 1):
        # set one shape to exactly that of another shape
        Cluster.__init__(self, col, row, 4)
        self.clr = other.clr
        self._rot = 1
        self._colOffsets = [-1, 0, 0, 1] #@@
        self._rowOffsets = [-1,-1, 0, 0]
        self._rotate() #@@

    def _rotate(self):
        """ offsets are assigned starting from the farthest (most distant) block in reference to the anchor block """
        if self.clr == 1:    #           (default rotation)    
                             #   o             o o                o              
                             # o x               x o            x o          o x
                             # o                                o              o o
            _colOffsets = [[-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0]] #       
        elif self.clr == 2:  #
                             # o                 o o           o              
                             # o x             o x             x o             x o
                             #   o                               o           o o
            _colOffsets = [[-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0], [-1, 0, 0, 1]] #
            _rowOffsets = [[-1, 0, 0, 1], [-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0]] #
        elif self.clr == 3:  # 
                             #   o             o                o o              
                             #   x             o x o            x           o x o
                             # o o                              o               o
            _colOffsets = [[-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0], [ 1, 1, 0,-1]] #
            _rowOffsets = [[ 1, 1, 0,-1], [-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0]] #            
        elif self.clr == 4:  #  
                             # o o                o             o              
                             #   x            o x o             x           o x o
                             #   o                              o o         o
            _colOffsets = [[-1, 0, 0,0], [-1, 0, 1,1], [0, 0, 0,1], [-1, -1, 0,1]]     #
            _rowOffsets = [[-1,-1, 0, 1], [0,0,0,-1], [-1, 0, 1, 1], [1,0, 0, 0]]      # 
        elif self.clr == 5:  #   o                              o
                             #   o                              x              
                             #   x            o x o o           o          o o x o
                             #   o                              o              
            _colOffsets = [[ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0], [-2,-1, 0, 1]] #
            _rowOffsets = [[-2,-1, 0, 1], [ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0]] #           
        elif self.clr == 6:  #
                             #   o              o                o              
                             # o x            o x o              x o         o x o
                             #   o                               o             o 
            _colOffsets = [[ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0]] #
        elif self.clr == 7:  # 
                             # o o            o o               o o          o o
                             # o x            o x               o x          o x
                             # 
            _colOffsets = [[-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0]] #@@
            _rowOffsets = [[ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1]] #@@
        self._colOffsets = _colOffsets[self._rot] #@@
        self._rowOffsets = _rowOffsets[self._rot] #@@
        self._update() #@@

    def move_left(self):                
        self.col = self.col - 1                   
        self._update() #@@
        # move the spae one column left
        
    def move_right(self):               
        self.col = self.col + 1                   
        self._update() #@@
        # move the spae one column right
        
    def move_down(self):                
        self.row = self.row + 1                   
        self._update() #@@
        # move the spae one row down        
    def move_up(self):                  
        self.row = self.row - 1                   
        self._update() #@@
        # move the spae one row up

    def rotateClkwise(self):
        self._rot = (self._rot + 1)%4     # 4 possible values for rotation - 0,1,2,3
        self._rotate()
        # rotate clockwise

    def rotateCntclkwise(self):
        self._rot = (self._rot - 1)%4     # 4 possible values for rotation - 0,1,2,3
        self._rotate()
        # rotate counterclockwise

#---------------------------------------#
class Shadow(Shape):
    """ Shadow of current shape that shows where it will go to the bottom
    """
    def __init__(self, other):
        Shape.__init__(self, other.col, other.row)
        self._rot = other._rot
        self._rotate()
        self.clr = other.clr

    def reset(self,other):
        self.row = other.row
        # set shadow row to object passed into it

    def draw(self, surface, gridsize):                     
        for block in self.blocks:
            block._draw_shadow(surface, gridsize)
            # draw the shadow 

    def update(self, other):
        # set the shadow to exactly that of the object passed into it
        self.col = other.col
        self._rot = other._rot
        self._rotate()
        self.clr = other.clr

#---------------------------------------#
class Floor(Cluster):
    """ Horizontal line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._colOffsets[i] = i  #@@
        self._update() #@@        
            
#---------------------------------------#
class Wall(Cluster):
    """ Vertical line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._rowOffsets[i] = i #@@
        self._update() #@@
