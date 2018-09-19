import tswp_lib as tswp
from os import rename

r = open("daily", "r")
w = open("daily_tmp", "w")
results = []
for line in r.readlines():
    print(line)
    if ':' in line:
        w.write(line)
        url = "https://www.ticketswap.nl/event/"+line[:line.index(":")]
        print(int(line[line.index(":")+1:-1]))
        diff = tswp.get_date_diff(int(line[line.index(":")+1:-1]))
        if diff > 0:
            with open("stats_"+line[:line.index("/")], 'a') as f:
                stats = [diff]
                stats = stats+tswp.get_event_stats(url)
                f.write(str(stats)+'\n')
                print(stats)
        else:
            with open("ERROR_"+line[:line.index("/")], 'a') as f:
                f.write('error')
    else:
        url = "https://www.ticketswap.nl/event/"+line[:-1]
        print(url)
        event_timestamp = tswp.get_event_date(url)
        print(event_timestamp)
        w.write(line[:-1]+":"+str(int(event_timestamp))+'\n')
r.close()
w.close()
rename("daily_tmp", "daily")
