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

    while True:
        line = str(file.readline())
        if line == '':
            break

        if not line.startswith("open"):
            continue

        current_value = int(line.split(' ')[2])
        heapq.heappushpop(heap, current_value)

    return heap[0]
