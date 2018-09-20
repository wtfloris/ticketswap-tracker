import tswp_lib as tswp
from os import rename
import sys

path = "/etc/tswp_metric/"

if sys.argv[1] == "daily":
    r = open(path+"daily", "r")
    w = open(path+"daily_tmp", "w")
if sys.argv[1] == "hourly":
    r = open(path+"hourly", "r")
    w = open(path+"hourly_tmp", "w")

results = []
for line in r.readlines():
    print("Processing "+line[:line.index("/")])
    if ':' in line:
        url = "https://www.ticketswap.nl/event/"+line[:line.index(":")]
        print(int(line[line.index(":")+1:-1]))
        diff = tswp.get_date_diff(int(line[line.index(":")+1:-1]))
        if diff < 48 and sys.argv[1] == "daily":
            with open(path+"hourly", "w") as hourly_wr:
                hourly_wr.write(line)
                print("Event in less than 48 hours, moving to hourly")
        if diff > 0:
            if diff > 47 and sys.argv[1] == "daily":
                w.write(line)
            if diff < 48 and sys.argv[1] == "hourly":
                w.write(line)
            with open(path+"stats_"+line[:line.index("/")], 'a') as f:
                print(str(diff)+" hours left until the event starts")
                stats = [diff]
                stats = stats+tswp.get_event_stats(url)
                f.write(str(stats)+'\n')
                print(stats)
        else:
            with open(path+"ERROR_"+line[:line.index("/")], 'a') as f:
                f.write('error')
    else:
        url = "https://www.ticketswap.nl/event/"+line[:-1]
        event_timestamp = tswp.get_event_date(url)
        w.write(line[:-1]+":"+str(int(event_timestamp))+'\n')
r.close()
w.close()
if sys.argv[1] == "daily":
    rename(path+"daily_tmp", path+"daily")
if sys.argv[1] == "hourly":
    rename(path+"hourly_tmp", path+"hourly")

