#!/usr/bin/env python
import argparse
import hashlib
import os
import functools

def main():
    parser = argparse.ArgumentParser(prog="dedup")
    parser.add_argument("directory")

    args = parser.parse_args()

    dedup = {}
    duplicates = {}

    # put a list of all the files with same hashes as value of key hash
    # get all the lists of size > 1, with list[0] being the first found file in duplicate list
    # (so size 1 means no duplicates)
    for file in os.listdir(args.directory):
        path = f"{args.directory}/{file}"
        if not os.path.isfile(path):
            continue # ignore not files

        with open(path, "rb") as f:
            hash = hashlib.sha256(f.read()).hexdigest()

            if hash in dedup:
                duplicates[hash].append(path)
            else:
                dedup[hash] = path
                duplicates[hash] = [path]

    duplicates = [v for k,v in duplicates.items() if len(v) > 1]

    if len(duplicates) > 0:
        print("Duplicates Found!")
        print()
    for duplicate in duplicates:
        confirmation_bool = False

        while not confirmation_bool:
            keep = None

            while keep not in duplicate:
                keep = input("Please select a file from below to KEEP. THE OTHERS LISTED WILL BE *DELETED*. You can also enter 'q' to quit or 's' to skip\n\n" + ", ".join(map(lambda d: f"'{d}'", duplicate)) + "\n")

                if keep.lower() == 'q':
                    exit(0)
                if keep.lower() == 's':
                    break
                if keep not in duplicate:
                    print(f"'{keep}' is not an exact match for any provided duplicate!")
            if keep == 's':
                break

            delete = list(filter(lambda d: d != keep, duplicate))
            
            print()
            print("You have chosen the following to delete:")
            print()
            print(", ".join(map(lambda d: f"'{d}'", delete)))
            print()

            confirmation = input("Is this correct? [Y/n]")
            if confirmation == None or confirmation == '':
                confirmation = 'y'
            
            if confirmation.lower() == 'y':
                confirmation_bool = True
            else:
                confirmation_bool = False

            if confirmation_bool:
                for to_delete in delete:
                    os.remove(to_delete)

        


    
if __name__ == "__main__":
    main()