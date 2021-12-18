#!/usr/bin/env python

def fib(n):
    if (n == 0 or n == 1):
        return 1
    else:
        return fib(n -1) + fib(n-2)  
    
def printname(name) :
    print ("Hello ", name)


if __name__ == '__main__':
    printname("dinakar")
    print( fib(100)) 
