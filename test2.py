--------------------------------------------------------------
def arrive2(self,groups):
    if self.q2_busy < self.q2_servers:
        self.q2_busy+=1
        self.heap[self.q2_busy+4].event_time = self.time + self.service_time2
        self.heap[self.q2_busy+4].event_type = 2
        self.heap = siftup(self.heap, (self.q2_busy+4))
        #printf(self.heap, 1)
    else:
        self.q2.enqueue(self.service_time2)

    self.service_time2 = float(groups[self.count][2])

def second_service(self,groups):
    print("There")
    self.time = self.heap[0].event_time
    if self.q2.isEmpty():
        self.heap[0].event_time = self.heap[self.q1_busy].event_time
        self.q1_busy -= 1
    else:
        self.q1.dequeue()
        print("popped!")
        if self.q1.size() >= 1:
            self.heap[0].event_time = self.time + self.q1.items[-1]
        else:
            self.heap[0].event_time = self.time
    self.heap[0].event_type = 2
    self.heap = siftdown(self.heap, 0)
    #self.num_in_system -=1

    printf(sim.heap,0)
    printf(sim.heap,1)
    printf(sim.heap,2)
    printf(sim.heap,3)
    printf(sim.heap,4)
    print("-----------------------")
