#! /usr/local/bin/python3

import sys
import datetime
import time
import math
from os import system

# Read configuration in jime.cfg
with open("./jime.cfg", "r") as f:
    lines = f.readlines()
for line in lines:
    if len(line.strip()) == 0 or line.startswith("#"):
        pass
    else:
        exec(line.strip())

# Validate configuration variables and initialize flags based on which variables are defined
try:
    round_to_min
    using_list = False
#    print("DEBUD: using_list is " + str(using_list))
except NameError:
    round_to_min = -1
    try:
        round_to_min_list
        using_list = True
#        print("DEBUD: using_list is " + str(using_list))
    except NameError:
        print("Either round_to_min or round_to_min_list is required. Please correct the configuration in `jime.cfg`.")
        sys.exit(1);

try:
    loop_sec
except NameError:
    loop_sec = 0
    print("loop_sec has been set to the default value of 0 (no loop). To enable loop, please update the configuration in `jime.cfg`.")

try:
    round_up_min
    using_per = False
#    print("DEBUD: using_per is " + str(using_per))
except NameError:
    round_up_min = -1
    try:
        round_up_per
        using_per = True
#        print("DEBUD: using_per is " + str(using_per))
    except NameError:
        print("Either round_up_min or round_up_per is required. Please correct the configuration in `jime.cfg`.")
        sys.exit(1);

def walk_list(now_min):
    for i in range(len(round_to_min_list)):
        if i == len(round_to_min_list)-1:
            if round_to_min_list[i] <= now_min and now_min <= round_to_min_list[0]+60:
#                print("DEBUG: now_min is " + str(now_min))
                low_rtm = round_to_min_list[i]
#                print("DEBUG: low_rtm is " + str(low_rtm))
                high_rtm = round_to_min_list[0]+60
#                print("DEBUG: high_rtm is " + str(high_rtm))
                round_to_min = high_rtm - low_rtm
#                print("DEBUG: round_to_min is " + str(round_to_min))
                break
        else:
            if round_to_min_list[i] <= now_min and now_min <= round_to_min_list[i+1]:
#                print("DEBUG: now_min is " + str(now_min))
                low_rtm = round_to_min_list[i]
#                print("DEBUG: low_rtm is " + str(low_rtm))
                high_rtm = round_to_min_list[i+1]
#                print("DEBUG: high_rtm is " + str(high_rtm))
                round_to_min = high_rtm - low_rtm
#                print("DEBUG: round_to_min is " + str(round_to_min))
                break
    return round_to_min

now_min = datetime.datetime.now().minute
if using_list:
    round_to_min = walk_list(now_min)
if using_per:
    round_up_min = round((round_up_per/100)*(round_to_min))
#    print("DEBUG: round_up_min is " + str(round_up_min))

def jime():
    dt = datetime.datetime.now()
    round_to = 60*round_to_min
    round_up = 60*round_up_min
#    print("DEBUG: using_list is " + str(using_list))
#    print("DEBUG: using_per is " + str(using_per))
#    print("DEBUG: round_to_min is " + str(round_to_min))
#    print("DEBUG: loop_sec is " + str(loop_sec))
#    if using_per:
#        print("DEBUG: round_up_per is " + str(round_up_per))
#    print("DEBUG: round_up_min is " + str(round_up_min))
#    print("DEBUG: round_to is " + str(round_to))
#    print("DEBUG: round_up is " + str(round_up))
#    print("DEBUG: dt is " + str(dt))
    seconds = (dt - dt.min).seconds
#    print("DEBUG: seconds is " + str(seconds))
    rounding = (seconds+round_up) // round_to * round_to
#    print("DEBUG: rounding = (seconds+round_up) // round_to * round_to")
#    print("DEBUG: rounding = (" + str(seconds) + "+" + str(round_up) + ") // " + str(round_to) + " * " + str(round_to))
#    print("DEBUG: rounding = " + str(seconds+round_up) + " // " + str(round_to*round_to))
#    print("DEBUG: rounding is " + str(rounding))
    t = dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)
#    print("DEBUG: t = dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)")
#    print("DEBUG: t = " + str(dt) + " + datetime.timedelta(0," + str(rounding) + "-" + str(seconds) + "," + str(-dt.microsecond) + ")")
#    print("DEBUG: t = " + str(dt) + " + datetime.timedelta(0," + str(rounding-seconds) + "," + str(-dt.microsecond) + ")")
#    print("DEBUG: t = " + str(dt) + " + " + str(datetime.timedelta(0,rounding-seconds,-dt.microsecond)))
#    print("DEBUG: t is " + str(t))
    return str(t.hour).zfill(2)+":"+str(t.minute).zfill(2)

_ = system('clear')
print("The jime is "+jime())

if loop_sec > 0:
    now_sec = datetime.datetime.now().second
#    print("DEBUG: multiple * math.ceil(number / multiple) + multiple is " + str(loop_sec * math.ceil(now_sec / loop_sec)))
#    print("DEBUG: now_sec is " + str(now_sec) + ". Sleeping for " + str(loop_sec * math.ceil(now_sec / loop_sec) + 0.1 - now_sec) + " seconds.")
    time.sleep(loop_sec * math.ceil(now_sec / loop_sec) + 0.1 - now_sec)
    now_min = datetime.datetime.now().minute
    if using_list:
        round_to_min = walk_list(now_min)
    if using_per:
        round_up_min = round((round_up_per/100)*(round_to_min))
#        print("DEBUG: round_up_min is " + str(round_up_min))

    _ = system('clear')
    print("The jime is "+jime())
    while True:
        time.sleep(loop_sec)
        now_min = datetime.datetime.now().minute
        if using_list:
            round_to_min = walk_list(now_min)
        if using_per:
            round_up_min = round((round_up_per/100)*(round_to_min))
#            print("DEBUG: round_up_min is " + str(round_up_min))

        _ = system('clear')
        print("The jime is "+jime())
