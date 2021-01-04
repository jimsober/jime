#! /usr/local/bin/python3

import sys
import datetime
import time
from os import system

with open("/Users/jsober/projects/jime/jime.cfg", "r") as f:
    lines = f.readlines()
for line in lines:
    exec(line.strip())
    
if len(sys.argv) == 1:
    pass  #use values in jime.cfg
else:
    if len(sys.argv) not in [3, 4]:
        print("Script takes 3 arguments:")
        print("  1. round_to minutes")
        print("  2. loop seconds [0 for no loop]")
        print("  3. round_up minutes [optional, uses value in jime.cfg if not provided]")
        print()
        sys.exit(1);

    else:
        loop_fl = sys.argv[2]

    try:
        round_to_min=int(sys.argv[1])
        assert round_to_min > 0
    except ValueError:
        print("The round_to value must be an integer. Please try again.")
        sys.exit(1);
    except AssertionError:
        print("The round_to value must be greater than 0. Please try again.")
        sys.exit(1);
    try:
        loop_sec=int(sys.argv[2])
        assert loop_sec >= 0
    except ValueError:
        print("The loop seconds value must be an integer. Please try again.")
        sys.exit(1);
    except AssertionError:
        print("The loop seconds value must be greater than or equal to 0. Please try again.")
        sys.exit(1);
    if len(sys.argv) == 4:
        try:
            round_up_min=float(sys.argv[3])
            assert round_up_min >= 0
        except ValueError:
            print("The round_up value must be a number. Please try again.")
            sys.exit(1);
        except AssertionError:
            print("The round_up value must be greater than or equal to 0. Please try again.")
            sys.exit(1);
        try:
            assert round_up_min <= round_to_min
        except AssertionError:
            print("The round_up value must be less than or equal to the round_to value. Please try again.")
            sys.exit(1);

def jime(dt=None, round_to=60*round_to_min, round_up=60*round_up_min):
   if dt == None: 
       dt = datetime.datetime.now()
   seconds = (dt - dt.min).seconds
   rounding = (seconds+round_up) // round_to * round_to
   t = dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)
   return str(t.hour).zfill(2)+":"+str(t.minute).zfill(2)

_ = system('clear')
print("The jime is "+jime())

if loop_sec > 0:
    while True:
        time.sleep(loop_sec)
        _ = system('clear')
        print("The jime is "+jime())
