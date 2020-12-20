from time import sleep
from datetime import datetime
import os
import signal

try: # Check if python modules for gpiozero are installed
    from gpiozero import LEDBoard
    from gpiozero.tools import random_values
except ImportError:
    exit("This script requires the gpiozero module\nInstall with: sudo apt-get install python3-gpiozero")

# Get environment variables
DELAY = float(os.environ["DELAY"]) if "DELAY" in os.environ else 1
STARTTIME = os.environ["STARTTIME"] if "STARTTIME" in os.environ else "0000"
STOPTIME = os.environ["STOPTIME"] if "STOPTIME" in os.environ else "2359"




class GracefulKiller:
  kill_now = False
  signals = {
    signal.SIGINT: 'SIGINT',
    signal.SIGTERM: 'SIGTERM'
  }

  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self, signum, frame):
    print("\nReceived {} signal".format(self.signals[signum]))
    print("Cleaning up resources. End of the program")
    self.kill_now = True
    quit()

    
if __name__ == '__main__':
    tree = LEDBoard(*range(2,28),pwm=True)
    killer = GracefulKiller()
    while not killer.kill_now:
        now = datetime.now().strftime("%H%M")
        if now >= STARTTIME and now < STOPTIME:
            if not tree.is_active: # only switch on the tree if it was off
                for led in tree:
                    led.source_delay = DELAY
                    led.source = random_values()
            sleep(60)
        else:
            if tree.is_active:
                tree.close()
                tree = LEDBoard(*range(2,28),pwm=True)
                tree.off()
            sleep(60)
            






