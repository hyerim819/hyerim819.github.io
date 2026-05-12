import random
import string
from target import vulnerable_parser


def random_input(max_len=16):
    length = random.randint(1, max_len)
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(random.choice(alphabet) for _ in range(length)).encode()


def blackbox_fuzz(iterations=100000):
    for i in range(iterations):
        data = random_input()

        try:
            vulnerable_parser(data)
        except Exception as e:
            print("[BLACK-BOX] Crash found!")
            print("Iteration:", i)
            print("Input:", data)
            print("Error:", e)
            return

    print("[BLACK-BOX] No crash found")


if __name__ == "__main__":
    blackbox_fuzz()