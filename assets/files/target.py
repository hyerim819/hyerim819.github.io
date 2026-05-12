def vulnerable_parser(data: bytes):
   
    if len(data) < 8:
        return "too short"

    # 조건 1
    if data[0:4] == b"FUZZ":
        # 조건 2
        if data[4] == 0x41:  # 'A'
            # 조건 3
            if data[5] == 0x42:  # 'B'
                # 조건 4
                if data[6] == 0x43:  # 'C'
                    # 조건 5
                    if data[7] == 0x21:  # '!'
                        raise RuntimeError("Crash! Secret bug triggered")

    return "ok"


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python target.py <input>")
        sys.exit(1)

    user_input = sys.argv[1].encode()
    print(vulnerable_parser(user_input))