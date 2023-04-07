#Importing necessary libraries
import hashlib
import random
import string

# Defining a node class for the hash table
class Node:
    def __init__(self, key, value=None):
        self.key = key  # The key to be stored
        self.value = value  # The value to be stored

# Function to insert data into the hash table
def insert(table, key, value):
    table[key] = Node(key, value)

# Asking user to choose a hashing algorithm from the following options: MD5, SHA1, SHA256, SHA512.
print("Choose a hashing algorithm from the following:")
print("1. MD5")
print("2. SHA1")
print("3. SHA256")
print("4. SHA512")

# Continuously asking for user input until a valid choice is entered
while True:
    choice = input("Please enter your choice of the hashing algorithm: ")
    if choice == '1':
        algorithm = hashlib.md5
        break
    elif choice == '2':
        algorithm = hashlib.sha1
        break
    elif choice == '3':
        algorithm = hashlib.sha256
        break
    elif choice == '4':
        algorithm = hashlib.sha512
        break
    else:
        print("Invalid choice. Please enter a valid choice (1, 2, 3, or 4).")

# Generating random passwords and hashing them using the chosen algorithm
passwords = []
print("Generating passwords...")
for i in range(100):
    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=8))
    passwords.append(password)
hashes = [algorithm(password.encode('utf-8')).hexdigest() for password in passwords]
print("Hashing passwords...")

# Define the reduction function and chain length
# Parameters:
#     hash_string (str): The input hash value.
#     iteration (int): The number of times the reduction function is applied.
#     alphabet (str): The alphabet used to generate the reduced values.
#     word_length (int): The length of the reduced values.
def reduce(hash_string: str, iteration: int, alphabet= string.ascii_letters + string.digits + string.punctuation, word_length: int = 8) -> str:
    if alphabet is None:
        alphabet = list(string.ascii_letters + string.digits + string.punctuation)

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

# Setting the chain length for the rainbow table
chain_length = 100

# Creating the rainbow table 
hash_table = {}
for i in range(len(passwords)):
    password = passwords[i]
    hash_val = algorithm(password.encode('utf-8')).hexdigest()
    for j in range(chain_length):
        password = reduce(hash_val, j)
        hash_val = algorithm(password.encode('utf-8')).hexdigest()
    insert(hash_table, hash_val, password)

# Printing the rainbow table to the console
print("Rainbow table:")
print("{:<10} {:<34} {:<10}".format("Password", "Last value in the chain", "Hash"))
print("-" * 70)
for key in hash_table:
    node = hash_table[key]
    print("{:<10} {:<34} {:<10}".format(node.value, reduce(node.key, chain_length - 1), node.key))

# Ask the user to enter a hash value to find the original password
hash_val_to_find = input("Enter the hash value to find the original password: ")
# Find the original password in the rainbow table and print it to the console
password_node = hash_table.get(hash_val_to_find)
# If the hash value is not found in the rainbow table, print a message to the console
if password_node is None:
    print("Hash value not found in the rainbow table.")
# If the hash value is found in the rainbow table, print the original password and the last chain value to the console    
else:
    password = password_node.value
    last_chain_value = reduce(hash_val_to_find, chain_length - 1)
    print("The original password for this hash value is '{}': {} -- followed by the last chain value: {}".format(hash_val_to_find, password, last_chain_value))
