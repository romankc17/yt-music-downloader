import threading
import time

def foo(param):
    print(f'{param} before sleeping')
    time.sleep(10)
    print(f'{param} after sleeping')
    
for _ in range(3):   
    t1 = threading.Thread(target=foo,args='A')
    t1.start()
# t2 = threading.Thread(target=foo,args='B')

# t1.start()
# t2.start()
    