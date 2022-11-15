#! /usr/local/bin/python3

import sys
import logging
import datetime
import time
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
    clear_screen
except NameError:
    clear_screen = True
    logging.warning("clear_screen has been set to the default value of True. To change clear_screen, please update the configuration in `jime.cfg`.")
try:
    log_level
except NameError:
    log_level = "CRITICAL"
    logging.warning("log_level has been set to the default value of CRITICAL. To change log_level, please update the configuration in `jime.cfg`.")
cmd = "logging.basicConfig(stream=sys.stderr, level=logging." + log_level + ")"
exec(cmd)

try:
    round_to_min
    using_list = False
    logging.debug("using_list is " + str(using_list))
except NameError:
    round_to_min = -1
    try:
        round_to_min_list
        using_list = True
        logging.debug("using_list is " + str(using_list))
    except NameError:
        logging.critical("Either round_to_min or round_to_min_list is required. Please correct the configuration in `jime.cfg`.")
        sys.exit(1);

try:
    loop_sec
except NameError:
    loop_sec = 0
    logging.warning("loop_sec has been set to the default value of 0 (no loop). To enable loop, please update the configuration in `jime.cfg`.")

try:
    round_up_min
    using_per = False
    logging.debug("using_per is " + str(using_per))
except NameError:
    round_up_min = -1
    try:
        round_up_per
        using_per = True
        logging.debug("using_per is " + str(using_per))
        logging.debug("round_up_per is " + str(round_up_per))
    except NameError:
        logging.critical("Either round_up_min or round_up_per is required. Please correct the configuration in `jime.cfg`.")
        sys.exit(1);

def walk_list(now_min):
    for i in range(len(round_to_min_list)):
        if i == len(round_to_min_list)-1:
            if round_to_min_list[i] <= now_min and now_min <= round_to_min_list[0]+60:
                logging.debug("now_min is " + str(now_min))
                low_rtm = round_to_min_list[i]
                logging.debug("low_rtm is " + str(low_rtm))
                high_rtm = round_to_min_list[0]+60
                logging.debug("high_rtm is " + str(high_rtm))
                round_to_min = high_rtm - low_rtm
                break
        else:
            if round_to_min_list[i] <= now_min and now_min <= round_to_min_list[i+1]:
                logging.debug("now_min is " + str(now_min))
                low_rtm = round_to_min_list[i]
                logging.debug("low_rtm is " + str(low_rtm))
                high_rtm = round_to_min_list[i+1]
                logging.debug("high_rtm is " + str(high_rtm))
                round_to_min = high_rtm - low_rtm
                break
    return round_to_min

now_min = datetime.datetime.now().minute
if using_list:
    round_to_min = walk_list(now_min)
if using_per:
    round_up_min = round((round_up_per/100)*(round_to_min))
    logging.debug("round_up_min is " + str(round_up_min))

def jime():
    logging.debug("using_list is " + str(using_list))
    logging.debug("using_per is " + str(using_per))
    logging.debug("round_to_min is " + str(round_to_min))
    logging.debug("loop_sec is " + str(loop_sec))
    if using_per:
        logging.debug("round_up_per is " + str(round_up_per))
    logging.debug("round_up_min is " + str(round_up_min))
    dt = datetime.datetime.now()
    logging.debug("dt is " + str(dt))
    round_to = 60*round_to_min
    logging.debug("round_to is " + str(round_to))
    round_up = 60*round_up_min
    logging.debug("round_up is " + str(round_up))
    seconds = (dt - dt.min).seconds
    logging.debug("seconds is " + str(seconds))
    rounding = (seconds+round_up) // round_to * round_to
    logging.debug("(seconds+round_up) // round_to * round_to = rounding is " + str(rounding))
    t = dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)
    logging.debug("dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond) = t is " + str(t))
    return str(t.hour).zfill(2)+":"+str(t.minute).zfill(2)

if clear_screen:
    _ = system('clear')
print("The jime is "+jime())

if loop_sec > 0:
    now_sec = datetime.datetime.now().second
    logging.debug("multiple * round(number / multiple) + multiple = next multiple is " + str(loop_sec * round(now_sec / loop_sec) + loop_sec))
    logging.debug("now_sec is " + str(now_sec) + ".")
    logging.debug("Sleeping for " + str(loop_sec * round(now_sec / loop_sec) + loop_sec + 0.01 - now_sec) + " seconds.")
    time.sleep(loop_sec * round(now_sec / loop_sec) + loop_sec + 0.01 - now_sec)
    now_min = datetime.datetime.now().minute
    if using_list:
        round_to_min = walk_list(now_min)
    if using_per:
        round_up_min = round((round_up_per/100)*(round_to_min))
        logging.debug("round_up_min is " + str(round_up_min))

    if clear_screen:
        _ = system('clear')
    print("The jime is "+jime())
    while True:
        now_sec = datetime.datetime.now().second
        logging.debug("multiple * round(number / multiple) + multiple = next multiple is " + str(loop_sec * round(now_sec / loop_sec) + loop_sec))
        logging.debug("now_sec is " + str(now_sec) + ".")
        logging.debug("Sleeping for " + str(loop_sec * round(now_sec / loop_sec) + loop_sec + 0.01 - now_sec) + " seconds.")
        time.sleep(loop_sec * round(now_sec / loop_sec) + loop_sec + 0.01 - now_sec)
        now_min = datetime.datetime.now().minute
        if using_list:
            round_to_min = walk_list(now_min)
        if using_per:
            round_up_min = round((round_up_per/100)*(round_to_min))
            logging.debug("round_up_min is " + str(round_up_min))

        if clear_screen:
            _ = system('clear')
        print("The jime is "+jime())
