"""Binary min-heap operations over a fixed-size list of Event objects, keyed on event_time."""


def siftup(Heap, i):
    while i > 0:
        p = (i - 1) // 2

        if Heap[p].event_time < Heap[i].event_time and Heap[p].event_time != 0.0:
            return Heap

        Heap[i], Heap[p] = Heap[p], Heap[i]
        i = p
        siftup(Heap, i)
    return Heap


def siftdown(Heap, i):
    end = len(Heap) - 1
    while True:
        child = i * 2 + 1
        if child > end:
            break
        if child + 1 <= end and Heap[child].event_time > Heap[child + 1].event_time and Heap[child + 1].event_time != 0.0:
            child += 1

        if Heap[i].event_time > Heap[child].event_time and Heap[child].event_time != 0.0:
            Heap[i], Heap[child] = Heap[child], Heap[i]
            i = child
            siftdown(Heap, i)

        else:
            break
    return Heap


def printf(heap, i):
    print(heap[i].event_time, heap[i].event_type)


def heapPrint(heap):
    print("-----------------------")
    printf(heap, 0)
    print("-----------------------")
