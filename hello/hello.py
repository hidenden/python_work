import sys

def multi_string(base_sting: str, count: int) -> str:
    return base_sting * count

def hello(cnt: int) -> str:
    return multi_string("Hello ", cnt)

def world(cnt: int) -> str:
    return multi_string("World ", cnt)

def main() -> str:
    return hello(3) + world(3)


if __name__ == '__main__':
    s = main()
    print(s)
    exit(0)
