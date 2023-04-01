import hashlib
import random

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

# Define a function to reduce a hash to a password
def reduce(hash_value, iteration):
    password = str(int(hash_value[:8], 16) + iteration)
    return hashlib.md5(password.encode('utf-8')).hexdigest()

# Define a function to generate a chain of hashes
def generate_chain(start_password, chain_length):
    hash_value = hashlib.md5(start_password.encode('utf-8')).hexdigest()
    for i in range(chain_length):
        password = reduce(hash_value, i)
        hash_value = hashlib.md5(password.encode('utf-8')).hexdigest()
    return hash_value

# Define a function to search for a hash in the rainbow table
def search(root, hash_value, chain_length):
    for i in range(chain_length):
        password = reduce(hash_value, i)
        hash_value = hashlib.md5(password.encode('utf-8')).hexdigest()
        node = find(root, hash_value)
        if node is not None:
            return node.value
    return None

# Define a function to find a node in the binary tree
def find(root, key):
    if root is None or root.key == key:
        return root
    if key < root.key:
        return find(root.left, key)
    else:
        return find(root.right, key)

# Generate random passwords and hash them using MD5
passwords = []
print("Generating passwords...")
for i in range(1000):
    password = ''.join(random.choices(list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'), k=6))
    passwords.append(password)
hashes = [hashlib.md5(password.encode('utf-8')).hexdigest() for password in passwords]
print("Hashing passwords...")

# Create a binary tree with the passwords and hashes
root = None
chain_length = 1000
for i in range(len(passwords)):
    start_password = passwords[i]
    end_hash = generate_chain(start_password, chain_length)
    root = insert(root, end_hash, start_password)

# Print the rainbow table
print("Rainbow table:")
print("{:<34} {:<10}".format("Hash", "Password"))
print("-" * 46)
def print_tree(root):
    if root:
        print_tree(root.left)
        print("{:<34} {:<10}".format(root.key, root.value))
        print_tree(root.right)
print_tree(root)

# Ask the user for an MD5 hash to crack
hash_to_crack = input("Enter the MD5 hash to crack: ")

# Search for the password corresponding to the hash
password = search(root, hash_to_crack, chain_length)
if password is None:
    print("Unable to crack the password.")
else:
    print("The password corresponding to the hash is:", password)
