"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

Cole Breen (ctb93) Luke Kulm (lbk73)
December 9, 2021
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen, initially empty
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left, initially set to SHIP_LIVES
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step" that
    #                  initially starts at 0
    # Invariant: _time is a float >= 0
    #
    # Attribute _direction: the direction the aliens are traveling, initialy
    #                       equal to 'right'
    # Invariant: _direction is a string, either 'right' or 'left'
    #
    # Attribute _bolt_rate: the rate at which the bolt fires
    # Invariant: _bolt_rate is a random int between 1 and the constant BOLT_RATE
    #
    # Attribute _alien_steps: the number of steps the aliens have taken since
    #            the last bolt fired from the aliens
    # Invariant: _bolt_steps is an int >=0 and <=BOLT_RATE that starts at 0
    #
    # Attribute _animator: A coroutine for performing an animation, initially
    #                       equal to None
    # Invariant: _animator is a generator based coroutine or None
    #
    # Attribute _ship_hurt:  the hurt status of the ship, initially set to None
    # Invariant: _ship_hurt is either None or 'hurt'
    #
    # Attribute _reset: the reset status of the ship, initially set to False
    # Invarient: _reset is a boolean either True or False
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getReset(self):
        """
        Returns the value of the attribute self._reset
        """
        if self._reset == True:
            return True

    def getLives(self):
        """
        Returns the value of the attrubute self._lives
        """
        return self._lives

    def setNewShip(self):
        """
        Sets a new ship as a default ship using the ship initializer
        _ship_init()
        """
        self._ship_init()

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes a new Wave object.

        This __init__ method starts the game by initializing a Ship, aliens,
        and a defense line. It also initializes all other attributes.

        This function uses helper methods for initialization of the ship,
        aliens, and defense line to initialize each for the start of the game.
        """
        self._alien_init()
        self._ship_init()
        self._dline_init()
        self._time = 0
        self._direction = 'right'
        self._bolts = []
        self._bolt_rate = random.randint(1,BOLT_RATE)
        self._alien_steps = 0
        self._animator = None
        self._ship_hurt = None
        self._lives = SHIP_LIVES

    def _alien_init(self):
        """
        Helper method for initializer that creates the aliens and stores them
        inside of attribute self._aliens.

        This method creates a wave of Alien objects, that are ALIEN_H_SEP and
        ALIEN_V_SEP apart from each other. The left edge of the wave is
        ALIEN_H_SEP from the left edge of the window, and the top edge of the
        wave is ALIEN_CEILING from the top of the window. There are ALIEN_ROWS
        rows and ALIENS_IN_ROW aliens per row. The wave of aliens is stored as
        a 2-d list of Alien objects in self._aliens.
        """
        self._aliens = None
        for x in range(ALIEN_ROWS):
            row = []
            left_edge = ALIEN_H_SEP
            top_edge = GAME_HEIGHT-ALIEN_CEILING-x*(ALIEN_V_SEP+ALIEN_HEIGHT)
            imgval = (ALIEN_ROWS)-(x)
            if imgval%6 == 1 or imgval%6 == 2:
                image = ALIEN_IMAGES[0]
            if imgval%6 == 3 or imgval%6 == 4:
                image = ALIEN_IMAGES[1]
            if imgval%6 == 5 or imgval%6 == 0:
                image = ALIEN_IMAGES[2]
            for y in range(ALIENS_IN_ROW):
                newalien = Alien(left_edge,top_edge,image)
                row = row + [newalien]
                left_edge = left_edge + ALIEN_WIDTH + ALIEN_H_SEP
            if self._aliens == None:
                self._aliens = [row]
            elif self._aliens != None:
                self._aliens = self._aliens + [row]

    def _ship_init(self):
        """
        Helper method for initializer that creates a Ship object.

        Sets self._reset to False and creates a new Ship object, storing it
        inside of self._ship.
        """
        self._ship = None
        self._reset = False
        self._ship = Ship(GAME_WIDTH/2-SHIP_WIDTH/2)

    def _dline_init(self):
        """
        Initializes a black defense.
        The black defense line initialized is line of height of 2 and a width of
        GAME_WIDTH using a constructor of class GPath and setting it to
        attribute self._dline. The line also tells the player how far the aliens
        can move until the player loses the game.
        """
        self._dline = (GPath(linewidth=2,
        points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE], linecolor = [0,0,0,1]))

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,state,dt):
        """
        Animates the Ship, Aliens, and Bolts

        This is the method that updates the bolts, aliens, and ship, moving
        them, deleting them, and performing any other operations like explosion
        courotine.

        Parameter input: user input
        Precondition: input is an instance of GInput

        Parameter state: The current state of the game
        Precondition: state is a one of the variables STATE_INACTIVE,
        STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, or
        STATE_COMPLETE

        Parameter dt: amount of time since last frame
        Precondition: dt is a float
        """
        if self._animator is None:
            self.left_right_ship(input,state)
        self.alien_move(dt)
        self.bolt_update(input,state)
        if self._bolt_rate == self._alien_steps:
            alien = self.pick_alien(self.nonempty())
            self.alien_bolt(alien)
            self._bolt_rate = random.randint(1,BOLT_RATE)
            self._alien_steps = 0
        self.collide_aliens()
        if self._animator is None:
            self.collide_ship()
        if not self._animator is None:
            try:
                self._animator.send(dt)
            except:
                self._animator = None
                self._ship_hurt = None
                self._ship = None
                self._bolts = []
                self._reset = True
                self._lives -= 1
        elif self._ship_hurt == 'hurt':
            self._animator = self._ship.animate_explosion()
            next(self._animator)

    def left_right_ship(self,input,state):
        """
        If the state is active then moves the ship to the left a SHIP_MOVEMENT
        amount if the player presses the left key, and moves the ship to the
        right a SHIP_MOVEMENT amount if the player presses the right key.

        Parameter input: user input
        Precondition: input is an instance of GInput

        Parameter state: The current state of the game
        Precondition: state is a one of the variables STATE_INACTIVE,
        STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, or
        STATE_COMPLETE
        """
        if state == STATE_ACTIVE:
            if self._ship != None and input.is_key_down('left') \
            and self.restrict_ship('Left'):
                self._ship.setX(-SHIP_MOVEMENT)              #move left
            if self._ship != None and input.is_key_down('right') \
            and self.restrict_ship('Right'):
                self._ship.setX(SHIP_MOVEMENT)

    def restrict_ship(self, dir):
        """
        Method that returns True if the ship is moving left on the screen
        or right and False if neither is True.

        Parameter dir: The direction of movement.
        Precondition: is a string either 'Left' or 'Right' or neither.
        """
        if self._ship != None and dir == 'Left' \
        and (self._ship.getX()-SHIP_WIDTH/2-SHIP_MOVEMENT)<0:
            return False
        if self._ship != None and dir == 'Right' \
        and (self._ship.getX()+SHIP_WIDTH/2+SHIP_MOVEMENT)> GAME_WIDTH:
            return False
        else:
            return True

    def bolt_update(self,input,state):
        """
        Method that adds bolt if player presses key to add bolt and removes
        bolts if they are outside of the window.

        Parameter input: user input
        Precondition: input is an instance of GInput

        Parameter state: state is a one of the variables STATE_INACTIVE,
        STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, or
        STATE_COMPLETE
        """
        if self._ship != None and state == STATE_ACTIVE \
        and input.is_key_down('up') and self._animator is None:
            no_bolt = True
            for bolt in self._bolts:
                if bolt.isPlayerBolt():            #comment out for machine gun
                    no_bolt = False
            if no_bolt == True:
                self._bolts.append(Bolt(self._ship.getX(),self._ship.getY()+\
                SHIP_HEIGHT/2,BOLT_SPEED))
        copy = self._bolts[:]
        for bolt in self._bolts:
            bolt.bolt_move()
            if bolt.bolt_remove():
                copy.remove(bolt)
        self._bolts = copy

    def alien_bolt(self, alien):
        """
        Creates a bolt object (alien bolt) and appends it to self._bolts

        This method uses the aliens position and ALIEN_HEIGHT to determine the
        bolts starting position and the velocity is -BOLT_SPEED because the bolt
        is moving down.

        Parameter alien: the alien that the bolt will be drawn under
        Precondition: alien is a valid instance of alien from self._aliens
        """
        self._bolts.append(Bolt(self._aliens[alien[0]][alien[1]].getX(), \
        self._aliens[alien[0]][alien[1]].getY()-ALIEN_HEIGHT/2,-BOLT_SPEED))

    def alien_move(self,dt):
        """
        Method that moves the aliens left or right depending on the attribute
        self._direction.

        Parameter dt: amount of time since last frame
        Precondition: dt is a float
        """
        if self._time < ALIEN_SPEED:
            self._time += dt
        if self._time >= ALIEN_SPEED:
            if(self._direction == 'right'):
                self.move_aliens_right()
                self._alien_steps += 1
            elif(self._direction == 'left'):
                self.move_aliens_left()
                self._alien_steps += 1
            self._time = 0

    def move_aliens_right(self):
        """
        Method that moves the aliens right and moves them down when they get to
        the right edge.

        Invokes the method rightmost() to determine if the right most alien is too
        close to the right edge of the window. If so, it moves the aliens down
        and sets self._direction to 'left'. Otherwise the aliens are moved right
        by ALIEN_H_WALK.
        """
        if self.rightmost().getX() + ALIEN_WIDTH/2 + ALIEN_H_SEP > GAME_WIDTH:
            for xval in range(len(self._aliens)):
                for yval in range(len(self._aliens[xval])):
                    if self._aliens[xval][yval] != None:
                        self._aliens[xval][yval].\
                        setY(self._aliens[xval][yval].getY()-ALIEN_H_WALK)
            self._direction = 'left'
            return None
        for xval in range(len(self._aliens)):
            for yval in range(len(self._aliens[xval])):
                if self._aliens[xval][yval] != None:
                    self._aliens[xval][yval]\
                    .setX(self._aliens[xval][yval].getX()+ALIEN_H_WALK)

    def move_aliens_left(self):
        """
        Method that moves the aliens left and moves them down when they get to
        the left edge.

        Invokes the method leftmost() to determine if the left most alien is too
        close to the left edge of the window. If so, it moves the aliens down
        and sets self._direction to 'right'. Otherwise the aliens are moved left
        by ALIEN_H_WALK.
        """
        if self.leftmost().getX() - ALIEN_WIDTH/2 - ALIEN_H_SEP < 0:
            for xval in range(len(self._aliens)):
                for yval in range(len(self._aliens[xval])):
                    if self._aliens[xval][yval] != None:
                        self._aliens[xval][yval]\
                        .setY(self._aliens[xval][yval].getY()-ALIEN_H_WALK)
            self._direction = 'right'
            return None
        for xval in range(len(self._aliens)):
            for yval in range(len(self._aliens[xval])):
                if self._aliens[xval][yval] != None:
                    self._aliens[xval][yval]\
                    .setX(self._aliens[xval][yval].getX()-ALIEN_H_WALK)

    def nonempty(self):
        """
        Returns a list of indices representing columns that are nonempty.

        This method loops over self._aliens and determines which columns are
        nonempty. This collumn is then added to the accumulator nonempties.
        At the end, the accumulator nonempties is returned.
        """
        nonempties = []
        for x in range(ALIENS_IN_ROW):
            empty = True
            for y in range(ALIEN_ROWS):
                if self._aliens[y][x] != None:
                    empty = False
            if empty == False:
                nonempties = nonempties + [x]
        return nonempties

    def pick_alien(self,indices):
        """
        Returns a 2-element tuple with the index representation of an alien.

        This method invokes the random module's choice function to determine a
        random collumn index from the provided indices. Using that index, it
        determines the alien that is lowest and returns the index representation
        inside of a tuple.

        Parameter indices: Indices representing the non-empty collums of self._aliens
        Precondition: indices is a nonempty list of ints
        """
        index = random.choice(indices)
        row = None
        rowtest = ALIEN_ROWS-1
        while row == None:
            if self._aliens[rowtest][index] != None:
                row = rowtest
            if self._aliens[rowtest][index] == None:
                rowtest -= 1
        return (row,index)

    def leftmost(self):
        """
        Returns the leftmost Alien object that is closest to the bottom of the
        window (nonempty) in self._aliens.

        This method invokes the wave's nonempty() method to find the index of
        the left-most non-empty collumn. It then uses a while loop to determine
        which alien is lowest.
        """
        left = self.nonempty()[0]
        row = None
        rowtest = ALIEN_ROWS-1
        while row == None:
            if self._aliens[rowtest][left] != None:
                row = rowtest
            if self._aliens[rowtest][left] == None:
                rowtest -= 1
        return self._aliens[row][left]

    def rightmost(self):
        """
        Returns the rightmost Alien object that is closest to the bottom of the
        window (nonempty) in self._aliens.

        This function invokes the wave's nonempty() method to find the index of
        the rightmost non-empty collumn. It then uses a while loop to determine
        which alien is lowest.
        """
        right = self.nonempty()[-1]
        row = None
        rowtest = ALIEN_ROWS-1
        while row == None:
            if self._aliens[rowtest][right] != None:
                row = rowtest
            if self._aliens[rowtest][right] == None:
                rowtest -= 1
        return self._aliens[row][right]

    def lose(self):
        """
        Returns False if you have not lost and True if you have lost the game.

        Local variable lose, initialy set to False, tracks whether any aliens
        are below the self._dline. Loops over self._aliens and if any Aliens are
        below the self._dline, lose is set to True. If self._lives == 0, returns
        True. If lose == True, returns True. Otherwise, it returns lose (which
        will be False).
        """
        lose = False
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[0])):
                if self._aliens[len(self._aliens)-x-1][y] != None:
                    if self._aliens[len(self._aliens)-x\
                    -1][y].getY()-ALIEN_HEIGHT/2 < DEFENSE_LINE:
                        lose = True
        if self._lives == 0:
            return True
        if lose == True:
            return True
        return lose

    def win(self):
        """
        Returns True if player has won. Otherwise, returns False.

        Loops over self._aliens and determines if any of the indices are not
        equal to None. If there is an index that does not equal None, False is
        returned. If after looping through self._aliens, and all of the indices
        are determined to be None, True is returned indicating that you won.
        """
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[0])):
                if self._aliens[x][y] != None:
                    return False
        return True

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the wave's objects to the view.

        Loops through self._aliens and draws an alien to the view for every
        index that does not equal None. If self._ship does not equal None, it
        draws a ship to the view. It draws the self._dline to the view. Finally,
        it loops of the bolts in self._bolts and draws them to the view.

        Paremter view: The view to draw the obects to.
        Precondition: view is an instance of GView
        """
        for x in range(ALIEN_ROWS):
            for y in range(ALIENS_IN_ROW):
                if self._aliens[x][y] != None:
                    self._aliens[x][y].draw(view)
        if self._ship != None:
            self._ship.draw(view)
        self._dline.draw(view)
        for bolt in self._bolts:
            bolt.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def collide_aliens(self):
        """
        Determines whether a ship bolt collided with any of the aliens using the
        Alien class's collides() method.

        Local variable del_index determines the deletion index, and is -1
        initially, inidcating no deletion index. If any of the bolts in self._bolts
        hit an alien, as determined by Alien's collides() method, the index of
        the alien hit in self._aliens is set to None. del_index is set to the
        index of the bolt that collided with the Alien. Finally, if a bolt
        struck an Alien (del_index != -1), the index of that bolt is removed
        from self._bolts.
        """
        del_index = -1
        for bolt_index in range(len(self._bolts)):
            for x in range(ALIEN_ROWS):
                for y in range(ALIENS_IN_ROW):
                    if self._aliens[x][y] != None \
                    and self._aliens[x][y].collides(self._bolts[bolt_index]):
                        self._aliens[x][y] = None
                        del_index = bolt_index
        if del_index != -1:
            del self._bolts[del_index]

    def collide_ship(self):
        """
        Determines whether an alien bolt collided with the ship using the Ship
        class's collides() method.

        Local variable del_index determines the deletion index, and is -1
        initially, inidcating no deletion index. If any of the bolts in self._bolts
        hit the ship, as determined by Ship's collides() method, the attribute
        self._ship_hurt is set to 'hurt' and del_index is set to the index of
        the bolt that collided with the ship. Finally, if a bolt struck the ship,
        the index of that bolt is removed from self._bolts.
        """
        del_index = -1
        for bolt_index in range(len(self._bolts)):
            if self._ship != None \
            and self._ship.collides(self._bolts[bolt_index]):
                self._ship_hurt = 'hurt'
                del_index = bolt_index
        if del_index != -1:
            del self._bolts[del_index]
