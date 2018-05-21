import sys


def get_statistics(file):
    # skip all lines including first "open ..."
    while True:
        line = file.readline()
        if line == '' or line.startswith("open"):
            break

    items_count = 0
    plain_sum = 0
    squares_sum = 0

    while True:
        line = str(file.readline())
        if line == '':
            break

        if not line.startswith("open"):
            continue

        usec = int(line.split(' ')[2])
        plain_sum += usec
        squares_sum += usec ** 2
        items_count += 1

    mean = 0
    variance = 0

    if items_count > 0:
        EX = plain_sum / items_count
        EX2 = squares_sum / items_count
        mean = EX
        variance = EX2 - EX ** 2

    return mean, variance


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        try:
            file = open(file_name, "r")
            mean, variance = get_statistics(file)
            print("Mean: " + str(mean))
            print("Variance: " + str(variance))
        except Exception as e:
            print(e, file=sys.stderr)

    else:
        print("Usage: python {0} path".format(sys.argv[0]))
        print("path - path to file to get statistics from")