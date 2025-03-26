# How to Add a User to `user.csv`

This document explains how to safely add a new user to the `user.csv` file located at:

```
/home/flverge/Documents/42_pedago/ft_transcendence/ultimate_project/databaseapi/_docker/user.csv
```

## FOR BETTER CSV READING
Install the extension `Rainbow CSV`

## Steps to Add a User

1. Open the `user.csv` file in a text editor.
2. Add a new line at the end of the file with the following format:
	```
	first_name,last_name,username,email,password,two_fa_enabled,_two_fa_secret
	```
	- **first_name**: The user's first name.
	- **last_name**: The user's last name.
	- **username**: The unique username for the user.
	- **email**: The user's email address.
	- **password**: The user's password (ensure it is hashed if required).
	- **two_fa_enabled**: Set to `True` if two-factor authentication is enabled, otherwise `False`.
	- **_two_fa_secret**: (Optional) The secret key for two-factor authentication, required only if `two_fa_enabled` is `True`.

	Example:
	```
	Jane,Doe,jdoe,jdoe@example.com,securepassword,False
	```

3. Save the file.

4. Stop the containers.

5. Launch them with `make re` to add your users to the database.

## REMINDER

You can access to the admin-panel on this URL :

https://localhost:8443/admin/

With the following credentials

USERNAME : `admin`
PASSWORD : `admin`

## Important Notes

- The fields `username` and `email` MUST be unique, and manually checked.
- By default, you will set `two_fa_enabled` to `False`, and you'll not put any `_two_fa_secret`
- **NEVER modify an existing user** in the `user.csv` file unless you are performing a full reset using the following command: `make delete_volume re`

- Modifying users directly without resetting the database can lead to inconsistencies and potential issues.
- Always double-check the format and data before saving the file to avoid errors.

By following these guidelines, you can safely add new users to the system.