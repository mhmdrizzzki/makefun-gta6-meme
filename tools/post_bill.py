"""Write POST.json for the entry, from the address of the published post."""
import json
import sys


def main(argv):
    url = argv[1]
    with open("POST.json", "w") as fh:
        json.dump({"url": url}, fh, indent=2)
        fh.write("\n")
    print("POST.json ->", url)


if __name__ == "__main__":
    main(sys.argv)
