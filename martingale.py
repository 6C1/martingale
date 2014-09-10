import math, random, sys
from operator import eq

def main():
    args = get_args()
    play(*args)

def play(n,m,v=False):
    actors = Actors(n,m)
    i = 0
    while actors.num_actors() > 1:
        i += 1
        if v or (i%500==0):
            print "T =", i/60, "hours"
            print "Round", i, "\tRemaining players:", len(actors.actors)
            print "\tMin/Max Cash:", actors.min_cash(), "\t", actors.max_cash()
        play_game(*actors.get_rand_pair(),v=v)
        actors.purge()

    pot = actors.get_rand().get_cash()
    profit = actors.get_rand().get_cash()-actors.get_rand().init_cash
    ret = profit / actors.get_rand().init_cash
    ret_per = 1.0 * ret / i

    print "\nReport:"
    print "\t", "Number of players:", n
    print "\t", "Mean Starting Cash:", m
    print "\t", "Winner's Pot:", pot
    print "\t", "Games played:", i
    print "\t\t", "Profit:", profit
    print "\t\t", "Return:", ret
    print "\t\t", "Return per minute (assuming 1 round = 1 minute):", ret_per
    print ""

def play_game(a,b,v=False):
    if v: print "\tPlayers:", a.id, "and", b.id
    bet = 1
    while a.can_afford(bet) and b.can_afford(bet):
        if play_round(a,b,bet,v):
            if v: print "\t\t\twin!"
            break
        else:
            if v: print "\t\t\tA's remaining cash:", a.get_cash()
            bet *= 2

def play_round(a,b,bet,v=False):
    result = flip()
    if v: print "\t\tFlip:", result
    a.inc_cash(result*bet)
    b.dec_cash(result*bet)
    return flip() > 0

def flip():
    return random.randrange(2)*2-1

def get_args():
    if sys.argv[1] == '--help':
        print 'Usage: python martingale.py [number of players] [avg starting cash] [verbose]'
        sys.exit()
    args = [10,100,False]
    for i in (1,2,3): 
        if i < len(sys.argv): args[i-1] = int(sys.argv[i])
    return args

class Actor():
    def __init__(self, id, init_cash):
        self.id = id
        self.init_cash = init_cash
        self.cash = self.init_cash
    def can_afford(self, n):
        return n <= self.cash
    def get_cash(self):
        return self.cash
    def dec_cash(self, k):
        self.cash -= k
    def inc_cash(self, k):
        self.cash += k

class Actors():
    def __init__(self,n,m):
        self.actors = []
        root_m = math.sqrt(m)
        for i in xrange(n):
            self.actors += [Actor(i, int(random.gauss(m,root_m)))]

    def num_actors(self):
        return len(self.actors)

    def list_cash(self):
        return map(lambda x: x.get_cash(), self.actors)
    def min_cash(self):
        l = [sys.maxint]
        l.extend(self.list_cash())
        return reduce(min,l)
    def max_cash(self):
        l = [-sys.maxint]
        l.extend(self.list_cash())
        return reduce(max,l)
    def avg_cash(self):
        return sum(self.list_cash()) / self.num_actors()

    def get_rand(self):
        return random.choice(self.actors)
    def get_rand_pair(self):
        pair = [ self.get_rand(), self.get_rand() ]
        while eq(*pair):
            pair[1] = self.get_rand()
        return pair

    def purge(self):
        self.actors = filter(lambda x: x.can_afford(1),self.actors)

if __name__ == '__main__': main()
