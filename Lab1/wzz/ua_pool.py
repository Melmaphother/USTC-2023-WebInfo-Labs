from fake_useragent import UserAgent
import random

def ua_pool ():
    ua=UserAgent()
    uapool = []
    rand = random.randrange(1,4,1)
    times = random.randrange(5,15,1)
    for i in range(times + 1):
        if  rand == 1 :
            uapool.append(ua.chrome)
        elif rand == 2:
            uapool.append(ua.firefox)
        elif rand == 3:
            uapool.append(ua.edge)
        else:
            uapool.append(ua.safari)
    return uapool.pop()