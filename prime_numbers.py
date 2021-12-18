from itertools import count
import math
def is_prime(n):
    m = int(math.sqrt(n))+ 2 
    for i in range(2, m):
        if n % i == 0:
            return False
    else:
        return True

def prime_numbers():
    for i in count(1):
        if is_prime(i):
            yield i

if __name__ == '__main__':
    maxprime = int(input("Enter a number :") )
    icount = 1;
    for prime in prime_numbers():
        if prime < maxprime:
            print(prime, end=' ')
            if icount % 10 == 0:
                print("\n")
            icount += 1
        else:
            break
