from typing import Dict, List
import math
import os
import sys


supported_encodings = [
    "cp855",
    "cp866",
    "cp1251",
    "iso8859_5",
    "koi8_r"
]


def count_bytes_frequencies(byte_stream) -> Dict[int, float]:
    frequencies = {}
    border_byte = 127
    non_ascii_bytes_count = 0
    reading_chunk = 1024

    def count_bytes(bytes_array) -> int:
        counter = 0
        for byte in bytes_array:
            if byte > border_byte:
                frequencies[byte] = frequencies.get(byte, 0) + 1
                counter += 1
        return counter

    while True:
        input_bytes = byte_stream.read(reading_chunk)
        if not input_bytes: break
        non_ascii_bytes_count += count_bytes(input_bytes)

    if non_ascii_bytes_count > 0:
        for key in frequencies.keys():
            frequencies[key] = frequencies[key] / non_ascii_bytes_count

    return frequencies


def open_file_binary(file_path):
    if not os.path.exists(file_path):
        raise ValueError("File {} doesn't exist".format(file_path))
    if not os.path.isfile(file_path):
        raise ValueError("File {} is not a file".format(file_path))
    return open(file_path, 'rb')


def rmse(estimated_frequencies: Dict[int, float], true_freqs: Dict[str, float], encoding: str)-> float:
    error = 0
    for int_byte in estimated_frequencies:
        utf_8_char = bytes([int_byte]).decode(encoding=encoding).lower()
        true_freq = 0 if utf_8_char not in true_freqs else true_freqs[utf_8_char]
        error += (estimated_frequencies[int_byte] - true_freq) ** 2
    error = math.sqrt(error) / len(estimated_frequencies)

    return error


def choose_encoding(frequencies: Dict[int, float], true_freqs: Dict[str, float], encodings: List[str]) -> str:
    errors = {}

    for encoding in encodings:
        errors[encoding] = rmse(frequencies, true_freqs, encoding)

    return min(errors.keys(), key=errors.get)


def print_file_with_encoding(path: str, encoding: str) -> None:
    with open(file=path, mode='r', encoding=encoding) as file:
        reading_chunk = 1024
        print(file.read(reading_chunk))


def read_true_frequencies(path: str) -> Dict[str, float]:
    true_freqs = {}
    delimiter = ','
    with open(path) as file:
        for line in file:
            l = [item.strip() for item in line.split(delimiter)]
            true_freqs[l[0].strip("\"").lower()] = float(l[1])

    return true_freqs


def main(file_path: str):
    file = None
    true_freqs_file_path = "frequencies.csv"
    try:
        file = open_file_binary(file_path)
        true_freqs = read_true_frequencies(true_freqs_file_path)
        estimated_frequencies = count_bytes_frequencies(file)
        suggested_encoding = choose_encoding(estimated_frequencies, true_freqs, supported_encodings)
        print("Chosen encoding: {}".format(suggested_encoding))
        print_file_with_encoding(file_path, suggested_encoding)
    except Exception as e:
        print("Error:", e)

    finally:
        if file is not None:
            file.close()


def print_help(program_name):
    print("Usage: python3 {} path".format(program_name))
    print("path - path to file, which should be processed")


if __name__ == "__main__":
    MIN_ARGS_COUNT = 2
    if len(sys.argv) < MIN_ARGS_COUNT:
        print_help(sys.argv[0])
    else:
        main(sys.argv[1])
