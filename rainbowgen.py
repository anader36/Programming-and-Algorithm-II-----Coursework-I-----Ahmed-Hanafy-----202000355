import hashlib
import random
import string

# Define a class for the nodes in the binary tree
class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

# Define a function to insert a node into the binary tree
def insert(root, key, value):
    if root is None:
        return Node(key, value)
    if key < root.key:
        root.left = insert(root.left, key, value)
    elif key > root.key:
        root.right = insert(root.right, key, value)
    else:
        root.value = value
    return root

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

chain_length = 1000

# Create a binary tree with the passwords and hashes
root = None
for i in range(len(passwords)):
    hash_value = hashes[i]
    password = passwords[i]
    for j in range(chain_length):
        password = reduce(hash_value, j)
        hash_value = hashlib.md5(password.encode('utf-8')).hexdigest()
    root = insert(root, hash_value, password)

# Print the rainbow table
print("Rainbow table:")
print("{:<10} {:<34} {:<10}".format("Password", "Last value in the chain", "Hash"))
print("-" * 70)
def print_tree(root):
    if root:
        print_tree(root.left)
        print("{:<10} {:<34} {:<10}".format(root.value, reduce(root.key, chain_length-1), root.key))
        print_tree(root.right)
print_tree(root)

# Define a function to search for the original password
def search(hash_value):
    # Reverse through the reduction function to find the password
    password = None
    for i in range(chain_length-1, -1, -1):
        password = reduce(hash_value, i)
        # Check if we've already computed this password before
        if root is not None and find(root, hashlib.md5(password.encode('utf-8')).hexdigest()) is not None:
            return (password, reduce(hash_value, chain_length-1))
    return None

# Define a function to find a node in the binary tree
def find(root, key):
    if root is None:
        return None
    if key < root.key:
        return find(root.left, key)
    elif key > root.key:
        return find(root.right, key)
    else:
        return root

# Ask the user for a hash value to search for
hash_value = input("Enter a hash value to search for: ")

# Search for the original password
result = search(hash_value)

# Print the result for the user
if result is not None:
    print("Password:", result[0])
    print("Last value in the chain:", result[1])
else:
    print("Password not found in the rainbow table.")