#!/usr/bin/python3
import time
from signal import pause



try: #Check if python modules for gpiozero are installed
    from gpiozero import LEDBoard
    from gpiozero.tools import random_values
except ImportError:
    exit("This script requires the gpiozero module\nInstall with: sudo apt-get install python3-gpiozero")

def randomtree (delay):
    tree = LEDBoard(*range(2,28),pwm=True)
    try:
        while True:
            for led in tree:
                led.source_delay = delay
                led.source = random_values()
            pause()
    except (KeyboardInterrupt, SystemExit):
        quit()


    
if __name__ == '__main__':
    randomtree(1)






