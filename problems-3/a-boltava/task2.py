import heapq
import math
import io


def _skip_to_first_open(file: io.IOBase):
    # skip all lines including first "open ..."
    while True:
        line = str(file.readline())
        if line == '' or line.startswith("open"):
            break


def _get_dataset_size(file: io.IOBase) -> int:
    _skip_to_first_open(file)

    dataset_size = 0
    while True:
        line = str(file.readline())
        if line == '':
            break

        if line.startswith("open"):
            dataset_size += 1

    return dataset_size


def count_decile(file: io.IOBase) -> int:
    dataset_size = _get_dataset_size(file)
    file.seek(0)

    _skip_to_first_open(file)

    # heap stores 10% of max elements of the entire data set
    heap_size = int(math.ceil(dataset_size * 0.1))
    heap = [0] * heap_size
    # a map to keep track of item repetitions
    heap_counters = {0: heap_size}
    # repetitions of current heap-min element in the entire data set
    heap_min_count = heap_size

    while True:
        line = str(file.readline())
        if line == '':
            break

        if not line.startswith("open"):
            continue

        current_value = int(line.split(' ')[2])
        print(current_value)

        heap_min = heap[0]
        if current_value > heap_min:
            last_min = heapq.heappushpop(heap, current_value)
            heap_counters[current_value] = heap_counters.get(current_value, 0) + 1
            heap_counters[last_min] = heap_counters[last_min] - 1
            if heap_counters[last_min] == 0:
                del heap_counters[last_min]
                heap_min_count = heap_counters[heap[0]]
        elif current_value == heap_min:
            heap_min_count += 1

    decile = None
    if heap_min_count > heap_size:
        # min element of 10% max elements appeared more than 10% times
        decile = heap[0] + 1
    elif heap_min_count == heap_size:
        # min element of 10% max elements appeared exactly 10% times
        decile = heap[0]
    else:
        # min element of 10% max elements appears in the heap and
        # might be below the heap as well
        diff = heap_min_count - heap_counters[heap[0]]
        if sum(heap_counters.values()) + diff > heap_size:
            current_min = heap[0]
            next_min = heapq.heappop(heap)
            while current_min != next_min:
                    next_min = heapq.heappop(heap)
            decile = next_min
        else:
            decile = heap[0]

    return decile

