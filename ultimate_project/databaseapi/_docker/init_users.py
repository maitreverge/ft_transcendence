import csv
import os
import sys

INPUT_FILE = "user.csv"
def main():

    if not os.access(INPUT_FILE, os.R_OK):
        print("Could't find the user.csv", flush=True)
        sys.exit(1)
    
    # with open('user.csv', 'r') as csv_file:
    with open(INPUT_FILE, 'r') as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            print(row)
    

if __name__ == "__main__":
    main()