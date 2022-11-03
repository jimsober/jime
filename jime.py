#! /usr/local/bin/python3

import sys
import datetime
import time
from os import system

with open("./jime.cfg", "r") as f:
    lines = f.readlines()
for line in lines:
    if len(line.strip()) == 0 or line.startswith("#"):
        pass
    else:
        exec(line.strip())

try:
    round_to_min
    using_list = False
except NameError:
    round_to_min = -1
    try:
        round_to_min_list
        using_list = True
    except NameError:
        print("Either round_to_min or round_to_min_list is required. Please correct the configuration in `jime.cfg`.")
        sys.exit(1);

try:
    loop_sec
except NameError:
    print("loop_sec is required. Please correct the configuration in `jime.cfg`.")
    sys.exit(1);

try:
    round_up_min
    using_per = False
except NameError:
    round_up_min = -1
    try:
        round_up_per
        using_per = True
    except NameError:
        print("Either round_up_min or round_up_per is required. Please correct the configuration in `jime.cfg`.")
        sys.exit(1);

if using_list:
    for i in range(len(round_to_min_list)):
        if i == len(round_to_min_list)-1:
            if round_to_min_list[i] <= datetime.datetime.now().minute and datetime.datetime.now().minute <= round_to_min_list[0]+60:
                low_rtm = round_to_min_list[i]
                high_rtm = round_to_min_list[0]+60
                round_to_min = high_rtm
                break
        else:
            if round_to_min_list[i] <= datetime.datetime.now().minute and datetime.datetime.now().minute <= round_to_min_list[i+1]:
                low_rtm = round_to_min_list[i]
                high_rtm = round_to_min_list[i+1]
                round_to_min = high_rtm
                break
    if using_per:
        round_up_min = round((round_up_per/100)*(high_rtm - low_rtm))
else:
    if using_per:
        round_up_min = round((round_up_per/100)*(round_to_min))

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
        if using_list:
            for i in range(len(round_to_min_list)):
                if i == len(round_to_min_list)-1:
                    if round_to_min_list[i] <= datetime.datetime.now().minute and datetime.datetime.now().minute <= round_to_min_list[0]+60:
                        low_rtm = round_to_min_list[i]
                        high_rtm = round_to_min_list[0]+60
                        round_to_min = high_rtm
                        break
                else:
                    if round_to_min_list[i] <= datetime.datetime.now().minute and datetime.datetime.now().minute <= round_to_min_list[i+1]:
                        low_rtm = round_to_min_list[i]
                        high_rtm = round_to_min_list[i+1]
                        round_to_min = high_rtm
                        break
            if using_per:
                round_up_min = round((round_up_per/100)*(high_rtm - low_rtm))
        else:
            if using_per:
                round_up_min = round((round_up_per/100)*(round_to_min))

        _ = system('clear')
        print("The jime is "+jime())
