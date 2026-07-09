"""Core event-driven simulation of a two-stage (tandem) queueing system."""

import copy

from .event import Event
from .heap import siftdown, siftup
from .queue import Queue
from .server import Server


class Simulation:
    def __init__(self, groups, primary_servers, secondary_servers):
        self.count = 0  # num of arrivals so far
        self.num_in_system = 0  # keeps track of how many are being served/ are in a queue
        self.time = 0.0
        self.heap = [Event() for _ in range(21)]  # Fixed array of maximum 21 events, (10 servers + 10 servers + 1 arrival)
        self.q1 = Queue()
        self.q2 = Queue()
        self.q1_servers = int(primary_servers)
        self.q2_servers = int(secondary_servers)
        self.q1_busy = 0
        self.q2_busy = 0
        self.n_busy = 0

        self.idle1 = [Server() for _ in range(self.q1_servers)]  # Fixed array to keep track of primary servers
        for i in range(len(self.idle1)):
            self.idle1[i].id = i

        self.idle2 = [Server() for _ in range(self.q2_servers)]  # Fixed array to keep track of secondary servers
        for i in range(len(self.idle2)):
            self.idle2[i].id = i

        self.total_served = 0
        self.q1_wait_time = 0.0  # Variables for statistics
        self.q2_wait_time = 0.0
        self.total_service_time = 0.0
        self.q_one_size = 0
        self.q_two_size = 0
        self.id_count1 = 0
        self.id_count2 = 0

    def read_arrival(self, groups, x):
        if x == 1:
            self.time = self.heap[0].event_time  # Time goes to the top of the heap's time
            self.getNextArrival(groups)  # Reads the next arrival, service times
            self.heap[0] = Event()
            self.handle_arrival()  # Sets the top of the heap to the new service times
            self.heap = siftdown(self.heap, 0)  # Sifts the heap down
        else:
            self.time = self.heap[0].event_time  # This only happens when there are no arrivals left to read
            self.heap[0] = Event()
            self.heap[0].event_time = 100000  # Holds the spot of the arrival after there are none left
            self.heap[0].event_type = 3  # Kills the loop when this is at the top
            self.heap = siftdown(self.heap, 0)

    def arrive(self):
        self.time = self.heap[0].event_time  # Time goes to the top of the heap's time
        if self.q1_busy < self.q1_servers:  # If there is a server available

            self.q1_busy += 1
            self.n_busy += 1

            while self.idle1[self.id_count1].isBusy():  # While the primary server of position i is busy
                self.id_count1 += 1  # increment the position to look for the next free server

            self.heap[self.n_busy].server = self.idle1[self.id_count1]  # Assigns free server to customer
            self.heap[self.n_busy].server.busy = True  # server is now busy
            self.heap[self.n_busy].server.start = self.time  # Server starts working at current time

            self.heap[self.n_busy].arrive = self.heap[0].arrive  # passes the intial arrival time to the next available position in the heap
            self.heap[self.n_busy].event_time = self.time + self.heap[0].primary  # the new event time is the time when the customer will finish being served
            self.heap[self.n_busy].secondary = self.heap[0].secondary  # passes the secondary service time as needed to calculate in the future
            self.heap[self.n_busy].event_type = 1  # This event is now a primary service event

            self.heap = siftup(self.heap, self.n_busy)  # siftup

        else:
            self.heap[0].queue_t = self.time  # Else no servers are available so we enqueue at current time
            cop1 = copy.copy(self.heap[0])  # Have to make a copy otherwise it would be passed as reference
            self.q1.enqueue(cop1)
            print("Q1 ENQUEUED")
            if self.q1.size() > self.q_one_size:
                self.q_one_size = self.q1.size()  # if the queue is the biggest its ever been, set the max size to that

    def arrive2(self):
        self.time = self.heap[0].event_time  # Time goes to the top of the heap's time
        if self.q2_busy < self.q2_servers:  # If there is a server available

            self.q2_busy += 1
            self.n_busy += 1

            while self.idle2[self.id_count2].isBusy():  # While the secondary server of position i is busy
                self.id_count2 += 1  # increment the position to look for the next free server

            self.heap[self.n_busy].server = self.idle2[self.id_count2]  # Assigns free server to customer
            self.heap[self.n_busy].server.busy = True  # Server is now busy
            self.heap[self.n_busy].server.start = self.time  # Server starts working at current time

            self.heap[self.n_busy].arrive = self.heap[0].arrive  # passes the intial arrival time to the next available position in the heap
            self.heap[self.n_busy].event_time = self.time + self.heap[0].secondary  # the new event time is the time when the customer will finish being served(secondary)
            self.heap[self.n_busy].event_type = 2  # This event is now a secondary service type

            self.heap = siftup(self.heap, self.n_busy)
        else:
            self.heap[0].queue_t = self.time
            cop2 = copy.copy(self.heap[0])  # Else we enqueue for q2
            self.q2.enqueue(cop2)
            print("Q2 ENQUEUED")
            if self.q2.size() > self.q_two_size:
                self.q_two_size = self.q2.size()

    def first_service(self):
        self.time = self.heap[0].event_time  # Time is set by the event time at the top of the heap
        if self.q1.isEmpty():  # If the queue is empty

            self.service_handler()  # We set all the Event elements of heap[0] to those of heap[n_busy]
                                     # and we set all the elements of heap[n_busy] to 0

            self.idle1[0], self.idle1[self.q1_busy - 1] = self.idle1[self.q1_busy - 1], self.idle1[0]  # swaps the servers to keep them consistantly busy
            self.id_count1 = 0

            self.q1_busy -= 1
            self.n_busy -= 1

        else:
            print("Q1 DEQUEUED!")
            self.q1_wait_time += self.time - self.q1.items[-1].queue_t  # the [-1] grabs the element from the last item in the queue before its dequeued
            self.heap[0].arrive = self.q1.items[-1].arrive
            self.heap[0].secondary = self.q1.items[-1].secondary
            self.heap[0].event_time = self.time + self.q1.dequeue().primary  # else we dequeue with the event time becoming
                                                                              # the enqueued service time plus the current time

        self.heap = siftdown(self.heap, 0)  # We siftdown again

    def second_service(self):
        self.time = self.heap[0].event_time  # Time is set by the event time at the top of the heap
        self.total_service_time += self.time - self.heap[0].arrive  # for statistics
        if self.q2.isEmpty():
            # If the queue is empty

            self.service_handler()  # handle in the same way as we did the first service

            self.idle2[0], self.idle2[self.q2_busy - 1] = self.idle2[self.q2_busy - 1], self.idle2[0]  # swap secondary servers
            self.id_count2 = 0

            self.q2_busy -= 1
            self.n_busy -= 1
        else:
            print("Q2 DEQUEUED!")
            self.q2_wait_time += self.time - self.q2.items[-1].queue_t
            self.heap[0].arrive = self.q2.items[-1].arrive
            self.heap[0].event_time = self.time + self.q2.dequeue().secondary  # Dequeue in the same way

        self.heap = siftdown(self.heap, 0)
        self.num_in_system -= 1  # stats
        self.total_served += 1
        print("SERVED")

    def getNextArrival(self, groups):
        self.next_arrival = float(groups[self.count][0])
        self.primary_service = float(groups[self.count][1])  # Reads the next arrival
        self.secondary_service = float(groups[self.count][2])
        self.num_in_system += 1
        self.count += 1

    def handle_arrival(self):
        self.heap[0].arrive = self.next_arrival
        self.heap[0].primary = self.primary_service  # sets the top of the heap as the new arrival
        self.heap[0].secondary = self.secondary_service
        self.heap[0].event_time = self.next_arrival
        self.heap[0].event_type = 0

    def service_handler(self):
        self.heap[0].event_time = self.heap[self.n_busy].event_time
        self.heap[0].event_type = self.heap[self.n_busy].event_type
        self.heap[0].arrive = self.heap[self.n_busy].arrive
        self.heap[0].primary = self.heap[self.n_busy].primary
        self.heap[0].secondary = self.heap[self.n_busy].secondary  # All the busy work of handling the event
        self.heap[self.n_busy].event_time = 0.0
        self.heap[self.n_busy].event_type = 0
        self.heap[self.n_busy].arrive = 0.0
        self.heap[self.n_busy].primary = 0.0
        self.heap[self.n_busy].secondary = 0.0
        self.heap[0].server.end = self.time
        self.heap[0].server.idle_time += self.heap[0].server.end - self.heap[0].server.start
        self.heap[0].server.busy = False
        self.heap[0].start = 0.0
        self.heap[0].end = 0.0
        self.heap[0].server = self.heap[self.n_busy].server
