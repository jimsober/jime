# Jime
### Options
* Log Level
  * choose from DEBUG,INFO,WARNING,ERROR,CRITICAL
  * optional, default value of CRITICAL is used if omitted
* Round To options
  * minutes
  * minutes list
* Loop Seconds, 0 for no loop
  * optional, default value of 0 used if omitted
* Round Up options
  * minutes
  * percentage of minutes in current interval

### Configuration
The Round To, Loop Seconds, and Round Up options are configured in `jime.cfg`.

You may use only one Round To option (`round_to_min` or `round_to_min_list`). The values in round_to_min_list should be sorted from low to high and the highest value is followed by the lowest plus 60 (representing the lowest value of the next hour). 

You may use only one Round Up option (`round_up_min` or `round_up_per`).

#### Examples:
```
# Default configuration
log_level=CRITICAL
round_to_min=5
loop_sec=30
round_up_min=2
```
```
# This round to minutes list combines 10 and 15 minute intervals
log_level=CRITICAL
round_to_min_list=[0,10,15,20,30,40,45,50]
loop_sec=10
round_up_per=40
```
