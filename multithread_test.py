#!c:/python37/python
import threading
import multiprocessing
def sayHello(id):
    
    for i in range(0, 1000):
        id += i
    print("hello", id)

def multithread():
    listOfItems = [] 
    for i in range(0,100):
        listOfItems.append(i)
    threads = 3
    tasks = [listOfItems[i:i+threads] for i  in range(0, len(listOfItems), threads )  ]
    listOfThreads = [] 
    for task in tasks:
        for item in task:
            p = multiprocessing.Process(target=sayHello(item) )
            p.start()
            listOfThreads.append(p)
        for t in listOfThreads:
            t.join()
        print(f"length of listOfThreads: {len(listOfThreads) } ") 


if __name__ == "__main__":
    multithread() 
