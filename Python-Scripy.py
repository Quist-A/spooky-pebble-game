from z3 import *

print("Hello world")

x=7

print(x)

Z = IntSort()
B = BoolSort()
A = Array('A', Z, B)

Store(A, 0, True)

x=Select(A,0)
#print(x)


x,y = Ints('x y')
s = Solver()
s.add(x<y)
s.check()
print(s.model())

s.add(x>10)
s.check()
print(s.model())


# Create list [1, ..., 5] 
print ([ x + 1 for x in range(5) ])

# Create two lists containg 5 integer variables
X = [ Int('x%s' % (i*2)) for i in range(5) ]
Y = [ Int('y%s' % i) for i in range(5) ]
print (X)

# Create a list containing X[i]+Y[i]
X_plus_Y = [ X[i] + Y[i] for i in range(5) ]
print (X_plus_Y)

# Create a list containing X[i] > Y[i]
X_gt_Y = [ X[i] > Y[i] for i in range(5) ]
print (X_gt_Y)

print (And(X_gt_Y))

# Create a 3x3 "matrix" (list of lists) of integer variables
X = [ [ Int("x_%s_%s" % (i+1, j+1)) for j in range(5) ] 
      for i in range(3) ]
pp(X)

#solve(A[x] == x, Store(A, x, y) == A)

#(declare-const a1 (Array Int Int))


