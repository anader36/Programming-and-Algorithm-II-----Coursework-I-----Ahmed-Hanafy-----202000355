# Ahmed Nader Hussein - TKH ID: 202000355
# Code Title: Final Project - Rainbow Table Generator - Hash Tables
#Importing necessary libraries
import hashlib
import random
import string

# Generate a list of 1000 random passwords
passwords = []
print("Generating passwords...")
for i in range(100):
    # Create a password by selecting 6 random characters from the combination of letters, digits, and punctuation
    password = ''.join(random.choices(list(string.ascii_letters + string.digits + string.punctuation), k=6))
    passwords.append(password)

# Create a dictionary of hash functions
hash_funcs = {"1": hashlib.md5, "2": hashlib.sha1, "3": hashlib.sha256, "4": hashlib.sha512}

# Prompt the user to select a hash function
while True:
    print("Select a hash function:")
    print("1. MD5")
    print("2. SHA-1")
    print("3. SHA-256")
    print("4. SHA-512")

    hash_choice = input("Please enter your choice of the hashing algorithm: ")
    hash_func = hash_funcs.get(hash_choice)

    # If the user enters an invalid choice, prompt them to try again
    if hash_func is None:
        print("Invalid choice, try again. Please enter a valid choice (1, 2, 3, or 4).")
    else:
        break

# Hash the passwords and create a rainbow table
print("Hashing passwords...")

# Define a function to reduce the hash values to passwords
def reduce_hash(hash_string: str, iteration: int, alphabet: str = string.printable, word_length: int = 8) -> str:
    # Reduce the hash value to a number and add the iteration count
    value = (int(hash_string, 16) + iteration) % (2 ** 40)
    result = []
    # Convert the number to a password by selecting characters from the alphabet
    for i in range(word_length):
        mod = value % len(alphabet)
        value //= len(alphabet)
        result.append(alphabet[mod])
    return "".join(result)

# Define the chain length
chain_length = 10000

# Create a hash table to store the password-hash pairs
hash_table = {}
for i in range(len(passwords)):
    # Hash the password using the selected hash function
    password = passwords[i]
    hash_val = hash_func(password.encode('utf-8')).hexdigest()

    # Generate the chain and add the last password-hash pair to the hash table
    for j in range(chain_length):
        password = reduce_hash(hash_val, j)
        hash_val = hash_func(password.encode('utf-8')).hexdigest()
    hash_table[hash_val] = password

# Print the rainbow table
print("Rainbow table:")
print("{:<20} {:<40} {:<50}".format("Password", "Last value in the chain", "Hash Value"))
print("-" * 110)

for key in hash_table:
    value = hash_table[key]
    print("{:<20} {:<40} {:<50}".format(value, reduce_hash(key, chain_length - 1), key))

print()

# Prompt the user to enter a hash value to find the corresponding password
hash_val_to_find = input("Please enter the hash to find the original password: ")

# Search the rainbow table for the hash value and print the corresponding password
password = hash_table.get(hash_val_to_find)
if password is None:
    print("Hash value is not found in the rainbow table.")
else:
    last_chain_value = reduce_hash(hash_val_to_find, chain_length - 1)
    print("The original password for this hash value is '{}': {} -- followed by the last chain value: {}".format(hash_val_to_find, password, last_chain_value))
