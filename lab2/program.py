from components.utils import read_fa_from_file, read_fa_from_input
import os

if __name__ == '__main__':
    file_path = os.path.join(os.getcwd(), "lab2\\cpp_ints.in")
    fa = None
    command = int(input("1. Read FA from file.\n2. Read FA from input.\n>> "))
    if command == 1:
        fa = read_fa_from_file(file_path)
    elif command == 2:
        fa = read_fa_from_input()

    print(fa)
    menu = "\n\n1. Check sequence.\n2. Get longest prefix of sequence.\n>> "
    while True:
        line = input(menu)
        if not line:
            break

        command = int(line)
        seq = input("Enter sequence.\n>> ").strip().rstrip()
        if command == 1:
            is_accepted = fa.check_sequence(seq)
            print(f"\nIsAccepted: {is_accepted}")
        elif command == 2:
            print(fa.get_longest_prefix(seq))
        else:
            break
