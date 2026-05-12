# graybox_fuzzer.py

import random
import string


def instrumented_target(data: bytes):

    coverage = set()

    coverage.add("start")

    if len(data) < 8:
        coverage.add("too_short")
        return coverage, None

    coverage.add("len_ok")

    if data[0:4] == b"FUZZ":
        coverage.add("magic_FUZZ")

        if data[4] == 0x41:
            coverage.add("byte_4_A")

            if data[5] == 0x42:
                coverage.add("byte_5_B")

                if data[6] == 0x43:
                    coverage.add("byte_6_C")

                    if data[7] == 0x21:
                        coverage.add("byte_7_exclamation")
                        raise RuntimeError("Crash! Secret bug triggered")

    return coverage, None


def mutate(data: bytes):
    """
    기존 입력을 조금 변형한다.
    """

    if not data:
        data = b"A"

    data = bytearray(data)

    mutation_type = random.choice(["flip", "insert", "delete"])

    if mutation_type == "flip":
        index = random.randrange(len(data))
        data[index] = random.randint(32, 126)

    elif mutation_type == "insert":
        index = random.randrange(len(data) + 1)
        data.insert(index, random.randint(32, 126))

    elif mutation_type == "delete" and len(data) > 1:
        index = random.randrange(len(data))
        del data[index]

    return bytes(data)


def graybox_fuzz(iterations=100000):
    corpus = [
        b"",
        b"A",
        b"FUZZ",
        b"TESTDATA",
    ]

    global_coverage = set()

    for i in range(iterations):
        seed = random.choice(corpus)
        data = mutate(seed)

        try:
            coverage, _ = instrumented_target(data)
        except Exception as e:
            print("[GRAY-BOX] Crash found!")
            print("Iteration:", i)
            print("Input:", data)
            print("Error:", e)
            return

        new_coverage = coverage - global_coverage

        if new_coverage:
            print("[GRAY-BOX] New coverage:", new_coverage, "Input:", data)
            global_coverage.update(new_coverage)
            corpus.append(data)

    print("[GRAY-BOX] No crash found")
    print("Final coverage:", global_coverage)


if __name__ == "__main__":
    graybox_fuzz()