import random
import hashlib

# Define the password length
password_length = 6

# Define the character set to be used for generating the passwords
character_set = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Define the number of passwords to generate
num_passwords = 1000

# Generate the passwords and save them to a file
with open('passwords.txt', 'w') as f:
    for i in range(num_passwords):
        password = ''.join(random.choice(character_set) for _ in range(password_length))
        f.write(password + '\n')

# Hash the user input using MD5
user_input = input("Enter a password to hash: ")
md5_hash = hashlib.md5(user_input.encode()).hexdigest()
print('MD5 hash:', md5_hash)
