"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

Cole Breen (ctb93) Luke Kulm (lbk73)
December 9, 2021
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GSprite):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    #DEFENSE LINE ATTRIBUTE HERE                                                         ------------------------------

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setX(self,movement):
        """
        Sets value of x to x + movement.

        Parameter movement: The amount to modify x by.
        Precondition: movement is of type int or float. Can be negative or positive.
        """
        self.x= self.x + movement

    def getX(self):
        """
        Returns the x value of the Ship.
        """
        return self.x

    def getY(self):
        """
        Returns the y value of the Ship.
        """
        return self.y

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self,left_edge):
        """
        Initializes a Ship (a subclass of GSprite) with the given paremeter.

        This method uses parent class's initializer. The value of paremeter
        left_edge defines the attribute left of the ship. The bottom of the ship
        is defined to be constant SHIP_BOTTOM. The width of the ship is defined
        to be SHIP_WIDTH. The height of the ship is defined to be SHIP_HEIGHT.
        The image source is set to be ship-strip.png' with a format of (2,4).

        Paremeter left_edge: The left edge of the ship.
        Precondition: left_edge is of type int or float.
        """
        super().__init__(bottom=SHIP_BOTTOM, left=left_edge, width=SHIP_WIDTH,\
        height=SHIP_HEIGHT, source='ship-strip.png', format=(2,4))
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS

    #PLEASE NOTE, we used setX to move the ship...

    def collides(self,bolt):
        """
        Returns True if bolt is not a player bolt and it collides with the ship.

        This method returns False if bolt did not collide with the ship.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if not bolt.isPlayerBolt():
            if self.contains((bolt.x+bolt.width,bolt.y+bolt.height)): #top right
                return True
            elif self.contains((bolt.x-bolt.width,bolt.y+bolt.height)): #top left
                return True
            elif self.contains((bolt.x+bolt.width,bolt.y-bolt.height)): #bottom right
                return True
            elif self.contains((bolt.x-bolt.width,bolt.y-bolt.height)): #bottom left
                return True
        return False

    # COROUTINE METHOD TO ANIMATE THE SHIP

    def animate_explosion(self):
        """
        The explosion animation coroutine.

        This has a yield expression that recieves the dt (and does not yield
        anything back to the parent). Using dt, it calculates the total time
        elapsed (time_elapsed) since initial method call. Using time_elapsed,
        it determines the sprite sheet image that should be displayed using
        DEATH_SPEED and the total number of explosion images. It does this by
        modifying the inherited attribute frame. The variable animating controls
        the operation of this method.
        """
        time_elapsed = 0
        animating = True

        while animating:
            dt = (yield)
            time_elapsed += dt
            x = (time_elapsed/DEATH_SPEED)*7
            y = int(x)
            self.frame = y

            if time_elapsed > DEATH_SPEED:
                animating = False

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Returns the x value of the Alien.
        """
        return self.x

    def setX(self, new):
        """
        Sets value of x to new.

        Parameter new: The new x value of the alien.
        Precondition: new is of type int or float
        """
        self.x = new

    def getY(self):
        """
        Returns the y value of the Alien.
        """
        return self.y

    def setY(self, new):
        """
        Sets value of y to new.

        Parameter new: The new y value of the alien.
        Precondition: new is of type int or float
        """
        self.y = new

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, left_edge, top_edge, isource):
        """
        Initializes an alien (a subclass of GImage) with the given paremeters.

        This method uses parent class's initializer. The value of paremeter
        left_edge defines the attribute left of the alien. The value of paremeter
        top_edge defines the attribute top of the alien. The value of isource defines
        the image source of the alien. The width of the alien is defined
        to be ALIEN_WIDTH. The height of the alien is defined to be ALIEN_HEIGHT.

        Paremeter left_edge: The left edge of the alien.
        Precondition: left_edge is of type int or float.

        Paremeter top_edge: The top edge of the alien.
        Precondition: top_edge is of type int or float.

        Paremeter isource: The image source of the alien.
        Precondition: isource is a valid source code that is stored in the tuple
                      ALIEN_IMAGES, which is stored in consts.py.
        """
        super().__init__(left=left_edge, top=top_edge, width=ALIEN_WIDTH, \
        height=ALIEN_HEIGHT, source=isource)

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player or no
        collision occured.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if bolt.isPlayerBolt():
            if self.contains((bolt.x+bolt.width,bolt.y+bolt.height)): #top right
                return True
            elif self.contains((bolt.x-bolt.width,bolt.y+bolt.height)): #top left
                return True
            elif self.contains((bolt.x+bolt.width,bolt.y-bolt.height)): #bottom right
                return True
            elif self.contains((bolt.x-bolt.width,bolt.y-bolt.height)): #bottom left
                return True
        return False

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, xcord, ycord, velocity):
        """
        Initilizes a bolt (a subclass of GRectangle) with the given paremeters.
        This method uses parent class's initializer. The value of parameter
        xcord defines the attribute x of the bolt. The value of paremeter
        ycord defines the attribute y of the bolt. The value of velocity defines
        the attribute _velocity of the bolt.

        Paremeter xcord: The x coordinate of the bolt.
        Precondition: xcord is of type int or float.

        Paremeter ycord: The y coordinate of the bolt.
        Precondition: ycord is of type int or float.

        Paremeter velocity: The velocity of the bolt.
        Precondition: velocity is of type int or float
        """
        super().__init__(x=xcord, y=ycord, width=BOLT_WIDTH, \
        height=BOLT_HEIGHT, fillcolor='red')
        self._velocity = velocity

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def bolt_move(self):
        """
        Modifies the attribute y by _velocity.
        """
        self.y = self.y + self._velocity

    def isPlayerBolt(self):
        """
        Returns True if bolt is player bolt. Returns False otherwise.
        """
        if self._velocity > 0:
            return True
        return False

    def bolt_remove(self):
        """
        Returns True if bolt velocity is positive and bolt bottom is greater than
        GAME_HEIGHT. Also returns True if bolt velocity is negative and bolt top
        is less than 0. Returns False otherwise.
        """
        if self._velocity > 0:
            if self.bottom > GAME_HEIGHT:
                return True
        if self._velocity < 0:
            if self.bottom < 0:
                return True
        return False

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
