"""Command-line entry point: reads an input file and runs the simulation to completion."""

import time

from .heap import heapPrint
from .simulation import Simulation


def main():
    filename = input("Please enter a filename: ")
    infile = open(filename, 'r')
    start_time = time.time()

    text = infile.read().split()  # reads the file into one string split by _
    primary_servers = text[0]  # first item is prim servers
    secondary_servers = text[1]  # second item is sec severs
    groups = []

    for i in range(2, len(text) - 3, 3):
        groups.append([text[i], text[i + 1], text[i + 2]])  # each customer has three inputs

    total_wait1 = 0.0
    total_wait2 = 0.0

    sim = Simulation(groups, primary_servers, secondary_servers)  # class instance
    sim.read_arrival(groups, 1)  # Read the first arrival and add to event queue

    heapPrint(sim.heap)  # print the first element in the queue and its respective event type, 0 for arrival
    print("Line 1 Servers Busy:", sim.q1_busy)
    print("Length of queue 1:", sim.q1.size())
    print("Line 2 Servers Busy:", sim.q2_busy)
    print("Length of queue 2:", sim.q2.size())
    print("-----------------------")

    while sim.heap[0].event_type != 3:  # when the event type hits 3 there are no events left in queue

        total_wait1 += sim.q1.size() * (sim.heap[0].event_time - sim.time)  # This formula generates average queue length
        total_wait2 += sim.q2.size() * (sim.heap[0].event_time - sim.time)

        if sim.heap[0].event_type == 0:  # if 0 then arrival event
            sim.arrive()
            if sim.count < len(groups):
                sim.read_arrival(groups, 1)
            else:
                sim.read_arrival(groups, 0)  # If there are no arrivals left to read
        elif sim.heap[0].event_type == 1:
            sim.arrive2()  # the end time for second service must be calculated before the first service finishes
            sim.first_service()
        elif sim.heap[0].event_type == 2:
            sim.second_service()  # no third service so the event can just be handled

        heapPrint(sim.heap)

        print("Line 1 Servers Busy:", sim.q1_busy)
        print("Length of queue 1:", sim.q1.size())
        print("Line 2 Servers Busy:", sim.q2_busy)
        print("Length of queue 2:", sim.q2.size())
        print("-----------------------")

    # PRINT STATEMENTS
    print("Number of People Served:", sim.total_served)
    print("Time Last Service Request Completed:", sim.time)
    print("Average Total Service Time:", format(sim.total_service_time / sim.total_served, ".3f"))
    print("\nAverage Time Spent in Queue1:", format(sim.q1_wait_time / sim.total_served, ".3f"))
    print("Average Time Spent in Queue2:", format(sim.q2_wait_time / sim.total_served, ".3f"))
    print("Average Time Spent in Queues:", format((sim.q1_wait_time / sim.total_served) + (sim.q2_wait_time / sim.total_served), ".3f"))
    print("\nAverage Length of Queue1:", format(total_wait1 / sim.time, ".3f"))
    print("Average Length of Queue2:", format(total_wait2 / sim.time, ".3f"))
    print("Average Length of Queues:", format((total_wait1 / sim.time) + (total_wait2 / sim.time), ".3f"))
    print("\nMax Length of Queue1:", sim.q_one_size)
    print("Max Length of Queue2:", sim.q_two_size)
    print("Max Length of Queues:", sim.q_one_size + sim.q_two_size, "(Together) or", max(sim.q_one_size, sim.q_two_size), "(Separate)")

    print("\nIdle Times for each primary server:\n")  # This formatting is neater than having them all on the same line

    for i in range(len(sim.idle1)):
        print("Server", sim.idle1[i].id + 1, ":", format(sim.time - sim.idle1[i].idle_time, ".3f"))

    print("\nIdle Times for each secondary server:\n")

    for i in range(len(sim.idle2)):
        print("Server", sim.idle2[i].id + 1, ":", format(sim.time - sim.idle2[i].idle_time, ".3f"))

    print("\nTime it took this program to run in seconds: ", time.time() - start_time)
