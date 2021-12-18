def fib(n):
    a, b = 0, 1
    while b < n:
        print(b, end=' ')
        a, b = b, a+b
    print()

def fib2(n):
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
    return result
mem={0:0, 1:1} 
def fibm(n) :
    if not n in mem:
        mem[n] = fibm(n-1)+fibm(n-2)
        print("mem [{} ] is {}  ".format(str(n),  str(mem[n]) ))
    for k, v in mem.items():
        print(f"{k}: {v}  " ) 
    return mem[n] 
    
if __name__ == '__main__':
    for n in range(1,10):
        fibm(n) 
