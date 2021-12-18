#!c:/python37/python
import sys
import math

def isPrime(n, lim):
    q = int(math.sqrt(lim))
    for i in range(2, q):
        if n % i == 0:
            return False
    return True

def prime(limit): 
    primenums =[] 
    for n in range(2, limit):
        if isPrime(n, limit) :
            primenums.append(n)
    for i in primenums:
        print(i, end=" ") 

if __name__ == '__main__':
    print(sys.argv)
    limit = 100
    if len( sys.argv) > 1 :
        limit = int(sys.argv[1]) 
    prime(limit) 
