from target import vulnerable_parser


def whitebox_generate_input():
    """
    코드를 직접 분석했다고 가정하고,
    크래시 조건을 만족하는 입력을 생성한다.
    """

    data = bytearray(8)

    data[0:4] = b"FUZZ"
    data[4] = 0x41  # A
    data[5] = 0x42  # B
    data[6] = 0x43  # C
    data[7] = 0x21  # !

    return bytes(data)


def whitebox_test():
    data = whitebox_generate_input()

    print("[WHITE-BOX] Generated input:", data)

    try:
        vulnerable_parser(data)
    except Exception as e:
        print("[WHITE-BOX] Crash found!")
        print("Input:", data)
        print("Error:", e)


if __name__ == "__main__":
    whitebox_test()