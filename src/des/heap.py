"""Binary min-heap operations over a fixed-size list of Event objects, keyed on event_time."""


def siftup(heap, i):
    while i > 0:
        p = (i - 1) // 2

        if heap[p].event_time < heap[i].event_time and heap[p].event_time != 0.0:
            return heap

        heap[i], heap[p] = heap[p], heap[i]
        i = p
        siftup(heap, i)
    return heap


def siftdown(heap, i):
    end = len(heap) - 1
    while True:
        child = i * 2 + 1
        if child > end:
            break
        if child + 1 <= end and heap[child].event_time > heap[child + 1].event_time and heap[child + 1].event_time != 0.0:
            child += 1

        if heap[i].event_time > heap[child].event_time and heap[child].event_time != 0.0:
            heap[i], heap[child] = heap[child], heap[i]
            i = child
            siftdown(heap, i)

        else:
            break
    return heap


def printf(heap, i):
    print(heap[i].event_time, heap[i].event_type)


def heapPrint(heap):
    print("-----------------------")
    printf(heap, 0)
    print("-----------------------")
