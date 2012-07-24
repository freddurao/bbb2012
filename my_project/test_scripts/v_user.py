
import random
import time
import requests


class Transaction(object):
    def __init__(self):
        pass

    def run(self):
        #r = random.uniform(1, 2)
        #time.sleep(r)
        #self.custom_timers['Example_Timer'] = r
        r = requests.get('http://localhost:8000/polls/1/')
        r.raw.read()          

if __name__ == '__main__':
    trans = Transaction()
    trans.run()