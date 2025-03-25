import csv
import os
import sys
from django.contrib.auth import get_user_model


INPUT_FILE = "user.csv"

def create_user(current_user):
    first_name = current_user["first_name"]
    last_name = current_user["last_name"]
    username = current_user["username"]
    email = current_user["email"]
    password = current_user["password"]
    two_fa_enabled = current_user["two_fa_enabled"]
    _two_fa_secret = current_user["_two_fa_secret"]
    
    User = get_user_model()
    
    if username == "admin":
        User.objects.create_superuser(username=username, email=email, password=password, first_name=first_name, last_name=last_name, two_fa_enabled=two_fa_enabled, _two_fa_secret=_two_fa_secret)
    else:
        User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, two_fa_enabled=two_fa_enabled, _two_fa_secret=_two_fa_secret)
    
    print(f"User {username} created", flush=True)

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

        for user in data:
            User_obj = get_user_model()

            # If the current user does not exists in the data set, create
            if not User_obj.objects.filter(username=user["username"]).exists():
                create_user(user)
            # print(user["username"])
            # print()
        
            # User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    

if __name__ == "__main__":
    main()