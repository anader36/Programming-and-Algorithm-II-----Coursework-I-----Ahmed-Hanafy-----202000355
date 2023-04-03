import hashlib
import random
import string

# Define a hash table class
class HashTable:
    def __init__(self):
        self.table = {}

    # Define a method to insert a key-value pair into the hash table
    def insert(self, key, value):
        self.table[key] = value

    # Define a method to get a value from the hash table given a key
    def get(self, key):
        if key in self.table:
            return self.table[key]
        else:
            return None

# Generate random passwords and hash them using MD5
passwords = []
print("Generating passwords...")
for i in range(1000):
    password = ''.join(random.choices(list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'), k=6))
    passwords.append(password)
hashes = [hashlib.md5(password.encode('utf-8')).hexdigest() for password in passwords]
print("Hashing passwords...")

# Define the reduction function and chain length
def reduce(hash_string: str, iteration: int, alphabet=None, word_length: int = 6) -> str:
    if alphabet is None:
        alphabet = list(string.ascii_letters)

    # Shifting input hash value by iteration and modulo by 2^40.
    value = (int(hash_string, 16) + iteration) % (2 ** 40)
    result = []
    for i in range(word_length):
        # Getting modulo by alphabet length. Result number will be between 0 and len(alphabet).
        mod = value % len(alphabet)
        # Dividing value by alphabet length.
        value //= len(alphabet)
        # Getting symbol from input alphabet by calculated value in range from 0 to len(alphabet).
        result.append(alphabet[mod])
    # Generating word from calculated symbols list.
    return "".join(result)

chain_length = 10000

# Create a hash table with the passwords and hashes
hash_table = HashTable()
for i in range(len(passwords)):
    hash_value = hashes[i]
    password = passwords[i]
    for j in range(chain_length):
        password = reduce(hash_value, j)
        hash_value = hashlib.md5(password.encode('utf-8')).hexdigest()
    hash_table.insert(hash_value, password)

# Print the rainbow table
print("Rainbow table:")
print("{:<10} {:<34} {:<10}".format("Password", "Last value in the chain", "Hash"))
print("-" * 70)
for key, value in hash_table.table.items():
    print("{:<10} {:<34} {:<10}".format(value, reduce(key, chain_length - 1), key))

# Define a function to search for the original password
def search(hash_value):
    # Reverse through the reduction function to find the password
    password = None
    for i in range(chain_length-1, -1, -1):
        password = reduce(hash_value, i)
        # Check if we've already computed this password before
        if hash_table.get(hashlib.md5(password.encode('utf-8')).hexdigest()) is not None:
            return (password, reduce(hash_value, chain_length-1))
    return None

# Ask the user for a hash value to search for
while True:
    hash_value = input("Enter a hash value to search for (or 'quit' to exit): ")
    if hash_value == 'quit':
        break
    elif len(hash_value) != 32:
        print("Invalid hash value. Hash value must be a 32-character hexadecimal string.")
        continue
    else:
        # Search for the original password
        result = search(hash_value)

        # Print the result for the user
        if result is not None:
            print("Password:", result[0])
            print("Last value in the chain:", result[1])
        else:
            print("Password not found in the rainbow table.")