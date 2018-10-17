import pigo
import time  # import just in case students need
import random

# setup logs
import logging
LOG_LEVEL = logging.INFO
LOG_FILE = "/home/pi/PnR-Final/log_robot.log"  # don't forget to make this file!
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)


class Piggy(pigo.Pigo):
    """Student project, inherits teacher Pigo class which wraps all RPi specific functions"""

    def __init__(self):
        """The robot's constructor: sets variables and runs menu loop"""
        print("I have been instantiated!")
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 83
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 30
        self.HARD_STOP_DIST = 15
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 135
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 140
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        if __name__ == "__main__":
            while True:
                self.stop()
                self.menu()

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "c": ("Calibrate", self.calibrate),
                "s": ("Check status", self.status),
                "h": ("Open House", self.open_house),
                "q": ("Quit", quit_now)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    def open_house(self):
        """reacts to distance measurements in a cute way"""
        while True:
            if self.dist() < 20:
                self.encB(5)
                self.encR(5)
                self.encL(10)
                self.encR(5)
                for x in range (5):
                    self.servo(100)
                    self.servo(60)
                self.encR(30)
            time.sleep(.1)

    # YOU DECIDE: How does your GoPiggy dance?
    def dance(self):
        """executes a series of methods that add up to a compound dance"""
        if not self.safe_to_dance():
            print("\n----NOT SAFE TO DANCE----\n")
            return

        print("\n---- LET'S DANCE ----\n")

        for x in range(3):
            self.side_to_side()
            self.bob_head()
            self.spin_around()
            self.shake_it_up()
            self.back_and_forth()
            self.spin_around()
            self.walk_back()
            self.wheelie()

    def safe_to_dance(self):
        """circles around and checks for any obstacle"""
        # check for problems
        for x in range(4):
            if not self.is_clear():
                return False
            self.encR(7) # is this 90 degrees?
        # if we find no problems:
        return True


    def side_to_side(self):
        """move left to right on a loop"""
        for x in range(3):
            self.encL(9)
            self.encR(9)

    def bob_head(self):
        """move head side to side"""
        for x in range(self.MIDPOINT - 20, self.MIDPOINT + 20,15):
            self.servo(x)

    def shake_it_up(self):
        """move in a square-like motion back and right, then forward and left"""
        for x in range(2):
            self.encB(6)
            self.encR(6)
            self.encF(6)
            self.encL(6)

    def back_and_forth(self):
        """move backwards and forwards"""
        for x in range(2):
            self.encB(6)
            self.encF(6)

    def spin_around (self):
        """spin left then spin right"""
        for x in range (2):
            self.encR(27)
            self.encR(27)
            self.stop()

    def walk_back(self):
        """walk forward then backwards at an angle"""
        for x in range(2):
            self.encF(15)
            self.encR(5)
            self.encB(8)
            self.encL(10)

    def wheelie(self):
        """have front wheels go up"""
        for x in range(3):
            self.set_speed(255, 255)
            self.encF(18)
            self.encB(60)
            self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)



    def obstacle_count(self):
        """scans and estimates the number of obstacles within sight"""
        self.wide_scan()
        found_something = False
        counter = 0
        for ang, distance in enumerate(self.scan):
            if distance and distance < 200 and not found_something:
                found_something = True
                counter += 1
                print("Object # %d found, I think" % counter)
            if distance and distance > 200 and found_something:
                found_something = False
        print("\n----I SEE %d OBJECTS----\n" % counter)

    def safety_check(self):
        """subroutine of the dance method"""
        self.servo(self.MIDPOINT)  # look straight ahead
        for loop in range(4):
            if not self.is_clear():
                print("NOT GOING TO DANCE")
                return False
            print("Check #%d" % (loop + 1))
            self.encR(8)  # figure out 90 deg
        print("Safe to dance!")
        return True

    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        while True:
            if self.is_clear():
                self.cruise()
            else:
                self.encR(10)

    def cruise(self):
        """ drive straight while path is clear """
        self.fwd()
        while self.dist() > self.SAFE_STOP_DIST:
            time.sleep(.5)
        self.stop()
####################################################
############### STATIC FUNCTIONS

def error():
    """records general, less specific error"""
    logging.error("ERROR")
    print('ERROR')


def quit_now():
    """shuts down app"""
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy


try:
    g = Piggy()
except (KeyboardInterrupt, SystemExit):
    pigo.stop_now()
except Exception as ee:
    logging.error(ee.__str__())
