def file_length(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def main():
    f = open("results_python.txt", "a")
    f.write(str(file_length("access.log")))
    f.close()


if __name__ == "__main__":
    main()
