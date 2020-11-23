#########################################
# Programmer: Mrs.G, Ron Varshavsky
# Date: 04/12/2016, 05-16-2020 -> 06-07-2020
# File Name: RonVarshavsky_tetris_template3.py
# Description: This program is the final Tetris game.
#########################################
from RonVarshavsky_tetris_classes import *
from random import randint
import pygame
import time
pygame.init()

HEIGHT = 600
WIDTH  = 800
GRIDSIZE = HEIGHT//24
screen=pygame.display.set_mode((WIDTH,HEIGHT))
restart = True #so you can restart the game at the end

#---------------------------------------#
#   loading photos                      #
#---------------------------------------#
startmenu = pygame.image.load("startmenu.png")
startmenu = pygame.transform.scale(startmenu,(WIDTH,HEIGHT))
instructions = pygame.image.load("instructions.png")
instructions = pygame.transform.scale(instructions,(WIDTH,HEIGHT))
background = pygame.image.load("background.png")
background = pygame.transform.scale(background,(WIDTH,HEIGHT))
deathscreen = pygame.image.load("deathscreen.png")
deathscreen = pygame.transform.scale(deathscreen,(WIDTH,HEIGHT))
resdeathscreen = pygame.image.load("resdeathscreen.png")
resdeathscreen = pygame.transform.scale(resdeathscreen,(WIDTH,HEIGHT))
#---------------------------------------#
#   loading fonts                       #
#---------------------------------------#
fontMedium = pygame.font.SysFont("Ariel Black",60)
fontPaused = pygame.font.SysFont("Ariel Black",100)

#---------------------------------------#
#   load sound effects                  #
#---------------------------------------#
spaceSoundEffect = pygame.mixer.Sound("space_sound.wav")
spaceSoundEffect.set_volume(1) #the sound when you press space

bruhSoundEffect = pygame.mixer.Sound("bruh.wav")
bruhSoundEffect.set_volume(1) #the sound when you clear a row

#---------------------------------------#
COLUMNS = 14                            #
ROWS = 22                               # 
LEFT = 9                                # 
RIGHT = LEFT + COLUMNS                  # 
MIDDLE = LEFT + COLUMNS//2              #
TOP = 1                                 #
FLOOR = TOP + ROWS                      #
#---------------------------------------#

#---------------------------------------#
#   functions                           #
#---------------------------------------#
def start_menu():
    """
    display start menu
    """
    screen.blit(startmenu, (0,0))
    if instruct: # if you open instructions, display them
        screen.blit(instructions, (0,0))
    pygame.display.update()

def redraw_screen():
    """
    display main game screen
    """
    screen.blit(background,(0,0))
    # DRAWING GRID, USING LOOPS
    for i in range(LEFT*GRIDSIZE,RIGHT*GRIDSIZE,GRIDSIZE):
        for j in range(TOP*GRIDSIZE, FLOOR*GRIDSIZE, GRIDSIZE):
            pygame.draw.line(screen, BLACK_CLR, (LEFT*GRIDSIZE,j),(RIGHT*GRIDSIZE,j),1)
        pygame.draw.line(screen,BLACK_CLR,(i,TOP*GRIDSIZE),(i,FLOOR*GRIDSIZE),1)
    # DRAW THE SHADOW & SHAPE
    shadow.draw(screen,GRIDSIZE)
    shape.draw(screen, GRIDSIZE)

    # DISPLAY ALL THE TEXTS
    scoreText = fontMedium.render(str(score),1,BLACK_CLR)
    screen.blit(scoreText,(LEFT*GRIDSIZE-75-scoreText.get_width(),TOP*GRIDSIZE+100))
    levelText = fontMedium.render(str(level),1,BLACK_CLR)
    screen.blit(levelText,(LEFT*GRIDSIZE-75-levelText.get_width(),TOP*GRIDSIZE+275))
    timeText = fontMedium.render(str(timeDisplayed),1,BLACK_CLR)
    screen.blit(timeText,(LEFT*GRIDSIZE-75-timeText.get_width(),TOP*GRIDSIZE+450))

    #######################################
    #IF YOU WANT TO SHOW BORDER, UNCOMMENT#
    #######################################
   # floor.draw(screen, GRIDSIZE)
   # ceil.draw(screen,GRIDSIZE)
   # leftWall.draw(screen, GRIDSIZE)
   # rightWall.draw(screen, GRIDSIZE)

    # DRAW OBSTACLES
    obstacles.draw(screen,GRIDSIZE)

    # DRAW ALL OF YOUR "next shapes"
    for i in range(len(nextShapes)):
        nextShapes[i].draw(screen,GRIDSIZE)
    
    pygame.display.update() 

def pause_menu():
    """
    display pause menu
    """
    # OVERLAY "PAUSED" TEXT WITH A RECTANGLE
    pausedText = fontPaused.render("PAUSED",1,BLACK_CLR)
    pygame.draw.rect(screen, WHITE_CLR, (WIDTH/2-pausedText.get_width()/2-10, HEIGHT/2-pausedText.get_height()/2-10, pausedText.get_width()+21, pausedText.get_height()+10), 0)
    pygame.draw.rect(screen, BLACK_CLR, (WIDTH/2-pausedText.get_width()/2-10, HEIGHT/2-pausedText.get_height()/2-10, pausedText.get_width()+21, pausedText.get_height()+10), 1)
    screen.blit(pausedText,(WIDTH/2-pausedText.get_width()/2,HEIGHT/2-pausedText.get_height()/2))
    pygame.display.update()

def lose_screen():
    """
    display lose screen
    """
    # SHOW THE LOSE SCREEN IMAGE, DISPLAY FINAL SCORE, IF MOUSING OVER
    #   RESTART GAME BUTTON, TURN IT GREEN
    screen.blit(deathscreen,(0,0))
    finalScore = fontPaused.render(str(score),1,WHITE_CLR)
    if pygame.mouse.get_pos()[0] >= 192 and pygame.mouse.get_pos()[0] <= 591 and pygame.mouse.get_pos()[1] >=393 and pygame.mouse.get_pos()[1] <=430:
        screen.blit(resdeathscreen,(0,0))
        if pygame.mouse.get_pressed() == (1, 0, 0):
            lost = False
    screen.blit(finalScore,(WIDTH/2-finalScore.get_width()/2,HEIGHT/2+20))
    pygame.display.update()
        
#---------------------------------------#
#   main program                        #
#---------------------------------------#    
shapeNo = randint(1,7)      
shape = Shape(MIDDLE-1,TOP+1,shapeNo)
floor = Floor(LEFT,FLOOR,COLUMNS)
ceil = Floor(LEFT,TOP-1,COLUMNS)
leftWall = Wall(LEFT-1, TOP, ROWS)
rightWall = Wall(RIGHT, TOP, ROWS)
obstacles = Obstacles(LEFT, FLOOR)

while restart: # so that you can restart the game. when you choose to exit it is false
    # MAKE THREE SHAPE OBJECTS FOR THE 'NEXT SHAPES'
    nextShapes = [Shape(RIGHT+4, TOP+5, randint(1,7)), Shape(RIGHT+4, TOP+8, randint(1,7)), Shape(RIGHT+4, TOP+11, randint(1,7))]
    # REMOVE ALL ROWS (FOR WHEN YOU RESTART, SO YOU DON'T AUTOMATICALLY LOSE)
    obstacles.removeAllRows([22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8,7, 6, 5, 4, 3, 2, 1, 0]) # get rid of all rows
    # score, make shadow object, set level to one, instructions not open, not first of two tetris'
    score = 0
    shadow = Shadow(shape)
    level = 1
    instruct = False
    firstTetris = False

    # variables for displaying, all true because they will stop at whichever is currently active
    #   except paused, which is active inside of inPlay so it is false by default
    startMenu = True
    inPlay = True
    paused = False
    lost = True

    # start playing the first song
    pygame.mixer.music.load("wet_hands.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops = -1)

    currentTime = 0; #VARIABLE FOR TIME LOGIC
    time_delay = 0.75; #SECONDS BETWEEN MOVING SHAPE DOWN
    timeDisplayed = 0 # VARIABLE FOR DISPLAYING TIME IN TIMER
    timeStarted = 0 # VARIABLE FOR WHEN EVERYTHING FINISHES LOADING (SO TIME DOESN'T START COUNTING TOO EARLY)

    while startMenu:
        # while you're on the start menu, display the start menu
        start_menu()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #if you click the 'x', close out of everything to quit
                    startMenu = False
                    inPlay = False
                    lost = False
                    restart = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        #if you press space, go to next screen (inPlay)
                        startMenu = False
                    if event.key == pygame.K_i:
                        # if you press i, invert instruct so it displays/hides instructions
                        if instruct:
                            instruct = False
                        else:
                            instruct = True

    # once you're on the next screen, load a new song
    pygame.mixer.music.load("revenge.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops = -1)

    # only now start counting time
    timeStarted = time.clock()
    while inPlay:
        # while on in play screen
        # make sure you're not currently paused
        if not paused:
            # change level based on your score
            if score >= 1000:
                level = 3
            elif score >= 500:
                level = 2
            # change the time delay between the shape dropping based on level
            if level == 2:
                time_delay = 0.4
            elif level == 3:
                time_delay = 0.2

            # display the time based on when you started the game
            timeDisplayed = round(time.clock()-timeStarted)

            # find full rows                
            fullRows = obstacles.findFullRows(TOP, FLOOR, COLUMNS) # finds the full rows and removes their blocks from the obstacles 
            # multiplier for score is 100 by default
            mult = 100
            # if the full rows is greater than zero
            if len(fullRows)>0:
                # play the removing rows sound effect
                bruhSoundEffect.play()
                # if you get a tetris (4 rows removed at once)
                if len(fullRows)>=4: #> as a fallback in case there is a glitch
                    # set the multiplier to 200
                    mult = 200
                    # if you're doing the second tetris in a row, make the multiplier 300 to get 1200 points
                    if firstTetris == True:
                        multi = 300
                    firstTetris = True
                if len(fullRows)<4: # if you don't get 4 rows, make the first tetris false
                    firstTetris = False
                # add your rows * multiplier to the score
                score+=len(fullRows)*mult

            # remove any rows that are full
            obstacles.removeFullRows(fullRows)

            # if you're colliding with the ceiling, game over bucko
            if shape.collides(ceil) or obstacles.collides(ceil): #GAME OVER!
                inPlay = False

            # if you collide with the floor or an obstacle
            if shape.collides(floor) or  shape.collides(obstacles):
                # move up & append shape to the obstacles
                shape.move_up()
                obstacles.append(shape)
                # set the shape to whatever the next shape was displayed
                shape.set_to(nextShapes[0], MIDDLE-1,TOP+1)
                # move all the shapes one up in the list, and make the last item a new random shape
                for i in range(len(nextShapes)-1):
                    nextShapes[i].set_to(nextShapes[i+1], RIGHT+4, TOP+3*i+5)
                nextShapes[len(nextShapes)-1] = Shape(RIGHT+4, TOP+11, randint(1,7))

            # update and reset the shadow ( done twice to prevent bugs )
                shadow.update(shape)
                shadow.reset(shape)
            shadow.update(shape)
            shadow.reset(shape)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # exit everything if you click the 'x'
                    inPlay = False
                    lost = False
                    restart = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        # if you press up, rotate, but rotate back if you're colliding with anything
                        shape.rotateClkwise()
                        if shape.collides(rightWall) or shape.collides(leftWall) or shape.collides(ceil) or shape.collides(obstacles):
                            shape.rotateCntclkwise()
                    if event.key == pygame.K_LEFT:
                        # when you press left, move left but undo if you collide into something
                        shape.move_left()
                        if shape.collides(obstacles) or shape.collides(leftWall):
                            shape.move_right()
                    if event.key == pygame.K_RIGHT:
                        #when you press right, move right but undo if you collide into something
                        shape.move_right()
                        if shape.collides(obstacles) or shape.collides(rightWall):
                            shape.move_left()
                    if event.key == pygame.K_DOWN:
                        #when you press down, move the shape down
                        shape.move_down()
                    if event.key == pygame.K_ESCAPE:
                        # if you press escape, pause the game & pause the music
                        paused = True
                        pygame.mixer.music.pause()
                    if shape.collides(floor)or shape.collides(obstacles):
                        # if you pressed down && ended up colliding into the floor/obstacle, move it back up
                        #   make a new shape as well
                        shape.move_up()
                        obstacles.append(shape)
                        shapeNo = randint(1,7)
                        shape = Shape(MIDDLE-1,TOP+1,shapeNo)
                    #update shadow once again
                    shadow.update(shape)
                    shadow.reset(shape)
                        

                    if event.key == pygame.K_SPACE:
                        # if you press space, go down immediately, and make the sound
                        while not shape.collides(floor) and not shape.collides(obstacles):
                            shape.move_down()
                            currentTime-=5; # done to make it instantly fall: otherwise it clips into the ground
                        shape.move_up()
                        spaceSoundEffect.play()
                        
            while not shadow.collides(obstacles) and not shadow.collides(floor):
                shadow.move_down()
                # shadow logic so that it goes to the very top of object/floor
            shadow.move_up()        # WHEN IT COLLIDES WITH FLOOR, MOVE IT UP ONCE   
            redraw_screen() #redraw screen
            if(time.clock() - time_delay > currentTime):
                # only move it down every time_delay seconds
                currentTime = time.clock()
                shape.move_down()
        else:
            # if you're paused, keep the screen drawn by overlay the pause menu
            redraw_screen()
            pause_menu()

            #stop counting time, so that it doesn't go up
            timePaused = time.clock()-timeDisplayed # save current time state
            timeStarted = timePaused # change started time so clock doesn't go up while paused

            for event in pygame.event.get():
                if event.type == pygame.QUIT:         
                    inPlay = False
                    lost = False
                    restart = False
                    # still exit everything
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # if you press escape while paused, unpause and play music
                        paused = False
                        pygame.mixer.music.unpause()
        pygame.time.delay(30) # ~33fps, so it's smooth

    # play song for when you lose (it's this to torture you for losing)
    pygame.mixer.music.load("eye_of_the_spider.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops = -1)

    while lost:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #still close everything
                    lost = False
                    restart = False
        if pygame.mouse.get_pos()[0] >= 192 and pygame.mouse.get_pos()[0] <= 591 and pygame.mouse.get_pos()[1] >=393 and pygame.mouse.get_pos()[1] <=430:
            if pygame.mouse.get_pressed() == (1, 0, 0):
                #if you press on the back to menu button, go back to menu
                lost = False

        #draw lose screen
        lose_screen()
        pygame.time.delay(30)
    
pygame.quit()
    
    
