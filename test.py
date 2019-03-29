import time
def main():
    start_time = time.time()
    #filename = input("Please enter a filename: ")
    infile = open('data.txt','r')

    text = infile.read().split()
    primary_servers = text[0]
    secondary_servers= text[1]
    groups = []

    for i in range(2,len(text)-3,3):
        groups.append([text[i],text[i+1],text[i+2]])


    sim = Simulation(groups,primary_servers,secondary_servers)
    sim.read_arrival(groups)
    for i in range(35):
        print("-----------------------")
        printf(sim.heap,0)
        printf(sim.heap,1)
        printf(sim.heap,2)
        printf(sim.heap,3)
        printf(sim.heap,4)
        printf(sim.heap,5)
        printf(sim.heap,6)
        printf(sim.heap,7)
        printf(sim.heap,8)
        printf(sim.heap,9)
        print("Line 1 Servers Busy:",sim.q1_busy)
        print("Length of queue 1:", sim.q1.size())
        print("Line 2 Servers Busy:",sim.q2_busy)
        print("Length of queue 2:", sim.q2.size())
        print("-----------------------")
        if sim.heap[0].event_type == 0:
            sim.arrive(groups)
            sim.read_arrival(groups)
        elif sim.heap[0].event_type == 1:
            sim.first_service(groups)
        elif sim.heap[0].event_type == 2:
            sim.second_service(groups)
    print("Total Served:",sim.total_served)
    print("Time it took this program to run in seconds: ",time.time()-start_time)
class Simulation:
    def __init__(self,groups,primary_servers,secondary_servers):
        self.count = 0
        self.q2_count = 0
        self.num_in_system = 0
        self.time = 0.0
        self.heap=[Event(),Event(),Event(),Event(),Event(),Event(),Event(),Event(),Event(),Event()]
        self.q1 = Queue()
        self.q2 = Queue()
        self.q1_servers = int(primary_servers)
        self.q2_servers = int(secondary_servers)
        self.q1_busy = 0
        self.q2_busy = 0
        self.service_time = float(groups[self.count][1])
        self.service_time2 = float(groups[self.q2_count][2])
        self.total_served = 0
        self.total_wait = 0.0
        self.total_service_time = 0.0

    def read_arrival(self,groups):
        self.getNextArrival(groups)
        self.heap[0] = Event()
        self.heap[0].event_time = self.next_arrival
        self.heap = siftdown(self.heap, 0)


        #self.total_wait+=self.num_in_system*(self.heap[0].event_time-self.time)

    def arrive(self,groups):
        self.time = self.heap[0].event_time
        if self.q1_busy < self.q1_servers:
            self.q1_busy+=1
            self.heap[self.q1_busy].event_time = self.time + self.service_time
            self.heap[self.q1_busy].event_type = 1
            self.heap = siftup(self.heap, self.q1_busy)

        else:
            self.q1.enqueue(self.service_time)
            print("Q1 ENQUEUED")
        self.service_time = float(groups[self.count][1])


    def arrive2(self,groups):
        self.q2_count +=1

        if self.q2_busy < self.q2_servers:
            self.q2_busy+=1
            self.heap[self.q2_busy+self.q1_servers].event_time = self.time + self.service_time2
            self.heap[self.q2_busy+self.q1_servers].event_type = 2
            self.heap = siftup(self.heap, (self.q2_busy+self.q1_servers))

        else:
            self.q2.enqueue(self.service_time2)
            print("Q2 ENQUEUED")
        self.service_time2 = float(groups[self.q2_count][2])


    def first_service(self,groups):
        self.time = self.heap[0].event_time
        self.arrive2(groups)
        if self.q1.isEmpty():
            self.heap[0].event_time = self.heap[self.q1_busy].event_time
            if self.q1_busy > 0:
                self.q1_busy -= 1
        else:
            self.q1.dequeue()
            print("Q1 DEQUEUED!")
            if self.q1.size() >= 1:
                self.heap[0].event_time = self.time + self.q1.items[-1]
            else:
                self.heap[0].event_time = self.time
        self.heap = siftdown(self.heap, 0)


    def second_service(self,groups):
        self.time = self.heap[0].event_time
        if self.q2.isEmpty():
            self.heap[0].event_time = self.heap[self.q2_busy+self.q1_servers].event_time #possibly +4
            self.q2_busy -= 1
        else:
            self.q2.dequeue()
            print("Q2 DEQUEUED!")
            if self.q2.size() >= 1:
                self.heap[0].event_time = self.time + self.q2.items[-1]
            else:
                self.heap[0].event_time = self.time
        self.heap = siftdown(self.heap, 0)
        self.num_in_system -=1
        self.total_served += 1
        print("SERVED")


    def getNextArrival(self,groups):
        self.next_arrival = float(groups[self.count][0])
        self.count+=1
        self.num_in_system+=1



class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Event:
    def __init__(self):
        self.event_time = 0.0
        self.event_type = 0



def siftup(Heap, i):
    while i > 0:
        p = (i-1)//2

        if Heap[p].event_time < Heap[i].event_time and Heap[p].event_time != 0.0:
            return Heap

        Heap[i], Heap[p] = Heap[p], Heap[i]
        i = p
        siftup(Heap,i)
    return Heap

def siftdown(Heap, i):
    end = len(Heap)-1
    while True:
        child = i * 2 + 1
        if child > end: break
    #    if Heap[child].event_time == 0.0:
            #return Heap
        if child + 1 <= end and Heap[child].event_time > Heap[child + 1].event_time:
            child += 1
        if Heap[i].event_time > Heap[child].event_time and Heap[child].event_time!=0.0:
            Heap[i], Heap[child] = Heap[child], Heap[i]
            i = child
            siftdown(Heap,i)
        else:
            break
    return Heap

def printf(heap,i):
    print(heap[i].event_time, heap[i].event_type)


main()
