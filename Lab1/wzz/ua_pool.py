from fake_useragent import UserAgent
import random

class uapool:
    count = 0
    uapool = []
    def add_ua_to_pool(times):
        rand = random.randrange(1,4,1)
        for i in range(times + 1):
            if  rand == 1 :
                self.uapool.append(ua.chrome)
            elif rand == 2:
                self.uapool.append(ua.firefox)
            elif rand == 3:
                self.uapool.append(ua.edge)
            else:
                uapool.append(ua.safari)

    def __init__ ():
        ua=UserAgent()
        times = random.randrange(5,15,1)
        add_ua_to_pool(times)
        self.count = times
        
    def pop():
        if self.count >= 1:
            self.count -= 1
        else:
            add_ua_to_pool(10)
            self.count += 9
        return self.uapool.pop()

