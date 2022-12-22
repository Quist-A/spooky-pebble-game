"""
Initially copied from Z3Prover/doc

Changed by Arend-Jan Quist

"""

from z3 import *
index = 0
def fresh(round, s):
    global index
    index += 1
    return Const("!f%d_%d" % (round, index), s)

def zipp(xs, ys):
    return [p for p in zip(xs, ys)]

def bmc(init, trans, goal, fvs, xs, xns):
    s = Solver()
    timeout = 60000  # timeout in ms
    s.set('timeout',timeout)
    
    s.add(init)
    count = 0
    
    max_time = 1000
    check = [True]*max_time  # solve rounds
    
    while count < max_time:
        print("iteration ", count)
        count += 1
        p = fresh(count, BoolSort())
        s.add(Implies(p, goal))
        
        if check[count]:
            res = solve(s,p,count,timeout,check)
            print(res)
            if res == sat:
                return
		#st = s.statistics()
		#print(st)
        s.add(trans)
        ys = [fresh(count, x.sort()) for x in xs]
        nfvs = [fresh(count, x.sort()) for x in fvs]
        trans = substitute(trans, 
                           zipp(xns + xs + fvs, ys + xns + nfvs))
        goal = substitute(goal, zipp(xs, xns))
        xs, xns, fvs = xns, ys, nfvs
        
    print("BMC solver: no solution found in max_time")
    return 
    
def solve(s,p,count,timeout,check):
    res = s.check(p)
    if sat == res:
        #print (s.model())
        print(res)
        #print(s.statistics())
        #return
    if unknown == res: # run out of time
        # set new timeout
        timeout = int(timeout*1)
        s.set('timeout',timeout)
        
        # disable check for next 10 interations
        for i in range(10):
            check[count+i] = False
    return res
    

"""
if __name__ == '__main__':
    x0, x1 = Consts('x0 x1', BitVecSort(4))
    bmc(x0 == 0, x1 == x0 + 3, x0 == 10, [], [x0], [x1])
"""
