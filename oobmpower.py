#!/usr/bin/env python3

"""
Quick little python script to control rpi GPIO pins that are  attached to
another slave machine's Power/Reset switches, for Out-Of-Band-Management.

Usage: oobmpower [--noprompt] [--power [--force]] [--reset]

Copyright 2018 Jacob Steele, <JSteele@JSteeleIR.com>
"""

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! You may need to re-run with sudo!")

from time import sleep
from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_bool('prompt', True, "Prompt to confirm the action")
flags.DEFINE_bool('power', None, "Press 'Power' button on the slave system")
flags.DEFINE_bool('reset', None, "Press 'Reset' button on the slave system")
flags.DEFINE_bool('force', False, "Force the power action. (Hard power-off)")

flags.mark_flags_as_mutual_exclusive(['power', 'reset'])


# Set GPIO to BCM mode.
GPIO.setmode(GPIO.BCM)

# Declare globals for the pin mappings.
POWERPIN = 23
RESETPIN = 24


def prompt():
    """
    Prompt the user to confirm the power/reset action.
    """

    yes = {'yes', 'y', 'ye'}
    print("About to press power/reset on the slave host!!! Okay? [N/y]: ", end='')
    choice = input().lower()
    return bool(choice in yes)

def main(argv):
    """
    Handle the core logic
    """
    del argv  # Unused.


    if FLAGS.power or FLAGS.reset:
        channels = [POWERPIN, RESETPIN]

        GPIO.setup(channels, GPIO.OUT)

        if not FLAGS.prompt or prompt():
            if FLAGS.power:
                print("Pressing power button...")
                GPIO.output(POWERPIN, GPIO.HIGH)
                if FLAGS.force:
                    sleep(10)
                else:
                    sleep(3)
                GPIO.output(POWERPIN, GPIO.LOW)
                print("Power button released!")
            elif FLAGS.reset:
                print("Pressing reset button...")
                GPIO.output(RESETPIN, GPIO.HIGH)
                sleep(3)
                GPIO.output(RESETPIN, GPIO.LOW)
                print("Reset button released!")
    GPIO.cleanup()


if __name__ == '__main__':
    app.run(main)
