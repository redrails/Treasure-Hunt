import pygame
import sys
from math import sqrt
from time import sleep
import ctypes

pygame.init()

# Program header, setting up the canvas.

width,height = 600,800
screen = pygame.display.set_mode((width, height))
black = (0,0,0)


class astar:                                        # A* algorithm implemenetation for movement and traceing routes to treasures.                            

    def __init__(self, start, end, obsList):        # Require starting point, end point which is the treasure and obsList which is the list of rocks. 
        self.start     = start
        self.end       = end
        self.obs       = obsList
        self.pythList  = []                         # Available movements dictionary with respective coordintes that they move to. 
        self.movement  = {
                            "right": (10, 0),
                            "left" : (-10, 0),
                            "up"   : (0, -10),
                            "down" : (0, 10)
                         }

    def neighbours(self, ship):                     # Function to find the neighbours of current cell.
        self.available = []                         # The list to store our available movements. 
        for mv in self.movement:
            #print self.available
            for obs in self.obs:                    # Iterate through all of our obs
                #print self.obs
                if ship.moveCheck(self.movement[mv][0], self.movement[mv][1]).colliderect(obs[1]):  # Check if upon movement in any direction our robot will hit any obstacle, if it does we do nothing.
                    pass
                else:
                    self.available.append((self.movement[mv][0], self.movement[mv][1]))             # If it is clear with sorroundings we are abla to move our robot in all the possible directions. 

        self.av = self.available
        #print "av = ", self.av
        for coords in self.av:                                      # Iterate through the available movements.
            self.tmpMove = ship.moveCheck(coords[0], coords[1])
            self.startx  = self.tmpMove.x                           # Temporarily move the robot and get coords to see which movement is optimal. 
            self.starty  = self.tmpMove.y

            self.pyth = sqrt(((self.end.x-self.startx)**2) + ((self.end.y-self.starty)**2))                 # Optimal move chosen by using pythagoras to see the distance between movement and treasure. 
            self.pythList.append((self.movement.keys()[self.movement.values().index(coords)], self.pyth))   # Find the movement we are looking for. 
        #print self.pythList
        self.kk = []    
        for vals in self.pythList:
            self.kk.append(vals[1])
        #print self.kk
        self.minnum = min(self.kk)  										 # Sort the list using linear sort of the list and find minimum value. 
        self.movementVar = [x for x in self.pythList if x[1] == self.minnum] # Choose the min value for movement. 
        #print self.movementVar[0]
        return self.movement[self.movementVar[0][0]]                         # Return the movement we're looking for. 
        #print self.available



class Robot:                        # Robot class is the actual class to control the movement object. 

    def __init__(self, x, y):       # Constructor for the class, stores starting position. 
        self.x = x
        self.y = y
        self.robot_img = "robot.png"

    def create(self):               # Function to spawn object. 
        self.robot_img_spawn = pygame.image.load(self.robot_img)    # Load robot. 
        self.rect = self.robot_img_spawn.get_rect()                 # Get rect object of instance. 
        self.rect.x = self.x                                        # Set X position of robot. 
        self.rect.y = self.y                                        # Set Y position of robot. 

    def blitter(self):                                              # Function to bind objects with screen for update. 
        screen.blit(self.robot_img_spawn, self.rect)

    def moveR(self, x, y):                                          # Move function to move the robot. 
        self.rect = self.rect.move(x, y)
        self.blitter()

    def moveCheck(self, x, y):
        return self.rect.move(x, y)                                 # Function to take the position of the movement for checking. 
    
    def pos(self):                                                  # Function to return current position of the robot in case we need it at any time. 
        return self.rect.x, self.rect.y

class Obstacle:                                     # Parent class for our object frame. This will be used for treasures and rocks.
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

    def create(self):                               # Globally fitted create function for all our objects. 
        self.spawn_img = pygame.image.load(self.img)
        self.rect = self.spawn_img.get_rect()

class Treasure(Obstacle):                                   # The treasure class which inherits from the Obstacle class
    tL = []                                                 # List to store the treasures placed
    def __init__(self, x, y, lvl):                          # Constructor for the class, stores starting position. 
        
        self.lvl = lvl                                      # Bronze silver or gold choice of object. 
        self.imgdict = {
                            "bronze": "bronze.png",         # Dictionary for bronze, silver and gold to the correseponding picture.
                            "silver": "silver.png",
                            "gold"  : "gold.png"
                       }
        self.scoredict = {
                            "bronze": 1,                    # Dictionary for bronze silver and gold to the score you would obtain.
                            "silver": 5,
                            "gold"  :10,
                         }
        self.img = self.imgdict[lvl]                        
        Obstacle.__init__(self, x, y, self.img)             # Using Obstacle class as a parent class  
        self.score = self.scoredict[lvl]                    # Corresponding the level with our dictionary.                
        
    def spawn(self):
        self.create()                                                   # Spawn the treasure
        self.rect.x = self.x                                            # The X position of the treasure
        self.rect.y = self.y                                            # The y position of the treasure
        Treasure.tL.append((self.spawn_img, self.rect, self.lvl))       # This appends the new treasure to the list

    def delete(self):                                                   # this is to delete the object when there is a collision
        for i in range(len(Treasure.tl)):
            if Treasure.tL[i][1] == self.rect:                          # Removing the object when we're done with it. 
                Treasure.tL.remove(i)


class Rock(Obstacle):                                   # The Rock class which inherits from the Obstacle class
    oL = []                                             # List to store rocks placed
    def __init__(self, x, y):                           # Constructor for the class, stores starting position.
        self.img = "rocks.png"                          # Rock image. 
        Obstacle.__init__(self, x, y, self.img)         # Parent class being instantiated again for the inherited attribuutes. 

    def spawn(self):                                    # Spawn function to create the rocks.
        self.create()
        self.rect.x = self.x                            # Position the rocks according to user. 
        self.rect.y = self.y
        Rock.oL.append((self.spawn_img, self.rect))

def itemCount():			# Function for the GUI. 
    global bronzeCount		# Some global functions. 
    global silverCount
    global goldCount
    global font
    pygame.draw.rect(screen, (0,128,255), (400,610,200,180))				# Main rectangle for the bottom strip. 
    font = pygame.font.Font(None, 24)										# Font class initiation. 
    title = font.render("Treasures on Screen: ", 1, black)
    bronze = font.render("Bronze Treasures "+str(bronzeCount), 1, black)	# Font render for the GUI for the treasures. 
    silver = font.render("Silver Treasures    "+str(silverCount), 1, black)
    gold   = font.render("Gold Treasures       "+str(goldCount), 1, black)
    screen.blit(title, (420, 620))
    screen.blit(bronze, (420,660))
    screen.blit(silver, (420, 680))
    screen.blit(gold, (420, 700))

def timer(toggletime):					# Timer function to keep track with the running time of the robot. 
    global done
    ms = pygame.time.get_ticks()		# Pygame time get. 
    sec = ms/1000						# Seconds calculation.
    left = toggletime-sec
    time = font.render("Time remaining: "+str(left),1,black)	# Render font time for display. 
    screen.blit(time, (10,660))
    if left <= 0:					# Stop the program at  0s left. 
        done = True

def score():				# Score Function to see the score of the robot as it collects treasures.
    global currentscore
    scoreUpdate = font.render("Score "+str(currentscore), 1, black)
    pygame.draw.rect(screen, (0,128,255), (0,610,200,180))
    pygame.draw.rect(screen, (0,128,255), (205,610,190,180))
    screen.blit(scoreUpdate, (10,620))

def howtouse(): # Function to render the instruction on the UI so that there is some sort of instruction of use. 
    screen.blit(font.render("How to use",1,black), (220,620))
    screen.blit(font.render("b = Bronze Treasure",1,black), (220,640))
    screen.blit(font.render("s = Silver Treasure",1,black), (220,660))
    screen.blit(font.render("g = Gold Treasure",1,black), (220,680))
    screen.blit(font.render("r = Rock Obstacle",1,black), (220,700))
    screen.blit(font.render("Spacebar = Start",1,black), (220,720))


def update():					# Main update function to keep the screen updating otherwise nothing will animate. 
    global toggletime
    global status
    screen.fill(pygame.Color("white"))
    pygame.draw.rect(screen, (0,204,204), (0,600,600,200))
    itemCount()
    score()
    howtouse()
    if status:
        timer(toggletime) 
    else:
        screen.blit(font.render("Set Time: "+str(toggletime),1,black), (10,660))
    R1.blitter()
    for treasure in Treasure.tL:
        screen.blit(treasure[0], treasure[1])
    for rock in Rock.oL:
        screen.blit(rock[0], rock[1])
    pygame.display.flip()


def startRobot(tl):					# Robot movement function for the game when it starts. 
    a = astar(R1, tl, Rock.oL)		# Initiate A* class. 
    movement = a.neighbours(R1)
    R1.moveR(movement[0], movement[1])
    sleep(0.1) 
    update()
    # R1.moveR(a.chooseMovement)
    #a.chooseMovement()


def chooseTreasure():
    global chosen
    chosen = Treasure.tL[0][1]	# Choosing treasures in order they have been placed. 

currentscore = 0

def start():				# Starting program function. 
    global currentscore
    chooseTreasure()		# Choose a treasure. 
    Finished = False
    while not Finished:
        startRobot(chosen)	# Make the robot go to the chosen treasure. 
        p = R1.pos()		# Get robot position to see where it is. 
        if R1.moveCheck(1,1).colliderect(chosen):	# If we reach our destination then
            hitted = Treasure.tL[0][2]
            if hitted == "bronze":					# We see what type of a treasure we have hit. 
                currentscore += 1
            elif hitted == "silver":
                currentscore += 5
            elif hitted == "gold":
                currentscore += 10
            Treasure.tL.pop(0)				# Remove the hit treasure from our list.
            Finished = True
            break
    

status = False
bronzeCount,silverCount,goldCount = 0,0,0 	# Start with 0 count. 
toggletime = 0 								# Start timer from 0. 
R1 = Robot(10,10) 							# Instantiate robot. 
R1.create()
update()
move = False
treasures = []
done = False
toggletime += pygame.time.get_ticks()/1000

ctypes.windll.user32.MessageBoxA(0, "To use the UI, place your cursor somewhere on the map and use the key-bindings to spawn objects on the map. Use the spacebar to start the game.", "Instructions for use", 1)

while not done:                                 # Game loop
    for event in pygame.event.get():            # If game quits we want to exit the window. 
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()

            # ALL below code is for setting keybindings to function. I.e. B,S,G to spawn bronze, silver, gold, respectively.
            # At each keypress the program runs a function as defined below. 

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    if mouseY > 600:
                        pass
                    else:
                        Treasure(mouseX,mouseY,"bronze").spawn()
                        bronzeCount+=1
                    update()
                elif event.key == pygame.K_s:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    if mouseY > 600:
                        pass
                    else:
                        Treasure(mouseX,mouseY,"silver").spawn()
                        silverCount+=1
                    update()
                elif event.key == pygame.K_g:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    if mouseY > 600:
                        pass
                    else:
                        Treasure(mouseX,mouseY,"gold").spawn()
                        goldCount+=1
                    update()
                elif event.key == pygame.K_r:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    if mouseY > 600:
                        pass
                    else:
                        Rock(mouseX,mouseY).spawn()
                    update()
                elif event.key == pygame.K_UP:
                    toggletime += 10                    
                    update()
                elif event.key == pygame.K_DOWN:
                    toggletime -= 10
                    update()
                elif event.key == pygame.K_SPACE:
                    status = True
                    while Treasure.tL:
                        start()
                        update()
