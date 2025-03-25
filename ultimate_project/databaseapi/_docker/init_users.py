import csv
import os
import sys
import json

INPUT_FILE = "user.csv"
def main():

    if not os.access(INPUT_FILE, os.R_OK):
        print("Could't find the user.csv", flush=True)
        sys.exit(1)
    
    with open(INPUT_FILE, 'r') as csv_file:
        f = csv.DictReader(csv_file)
        
        # Process each row to convert two_fa_enabled to boolean and handle None values
        data = []
        for row in f:
            # Convert empty strings and 'None' to Python None for all fields
            for key, value in row.items():
                if value == 'None' or value == '' or value is None:
                    row[key] = None
            
            # Convert two_fa_enabled field to boolean if it's not None
            if 'two_fa_enabled' in row and row['two_fa_enabled'] is not None:
                # Handle different possible boolean string representations
                row['two_fa_enabled'] = row['two_fa_enabled'].lower() in ('true', 't', 'yes', 'y', '1')
            
            data.append(row)

        # Pretty print with proper handling of None values
        # print(json.dumps(data, indent=2, default=str))
        # print(data)
        for user in data:
            print(user)
    

if __name__ == "__main__":
    main()