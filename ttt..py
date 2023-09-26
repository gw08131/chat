import threading
global total
total = 0
def sum(low, high):
    global total
    for i in range(low, high):
        total += i
    print("Subthread", total)
 
t = threading.Thread(target=sum, args=(1, 100000))
t.start()
for _ in range(30):
    print("Main Thread", total)