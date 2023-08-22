import MiYE
import sys


def main():
    program = MiYE.Program()
    program.start()


if __name__ == '__main__':
    with open("sys.log", "w") as log:
        sys.stderr = log
        main()
