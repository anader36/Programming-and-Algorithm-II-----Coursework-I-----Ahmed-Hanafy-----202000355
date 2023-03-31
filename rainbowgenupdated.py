import hashlib
import random

# Define a class for the nodes in the binary tree
class Node:
    def __init__(self, key, value=None, password=None):
        self.key = key
        self.value = value
        self.password = password
        self.left = None
        self.right = None

# Define a function to insert a node into the binary tree
def insert(root, key, value, password):
    if root is None:
        return Node(key, value, password)
    if key < root.key:
        root.left = insert(root.left, key, value, password)
    elif key > root.key:
        root.right = insert(root.right, key, value, password)
    else:
        root.value = value
        root.password = password
    return root

# Define a reduction function that takes the first 6 numbers of the hash and reduces it
def reduce_hash(hash_val, iteration):
    new_val = int(hash_val[:6], 16) + iteration
    new_val_str = str(new_val).encode('utf-8')
    return hashlib.md5(new_val_str).hexdigest()

def search(root, key):
    if root is None or root.key == key:
        return root
    if root.key < key:
        return search(root.right, key)
    return search(root.left, key)

# Generate random passwords and hash them using MD5
passwords = []
print("Generating passwords...")
for i in range(1000):
    password = ''.join(random.choices(list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'), k=6))
    passwords.append(password)
hashes = [hashlib.md5(password.encode('utf-8')).hexdigest() for password in passwords]
print("Hashing passwords...")

# Define the chain length
chain_length = 100

# Create a binary tree with the passwords and hashes
root = None
for i in range(len(passwords)):
    curr_hash = hashes[i]
    curr_pwd = passwords[i]
    for j in range(chain_length):
        curr_pwd_hash = hashlib.md5(curr_pwd.encode('utf-8')).hexdigest()
        curr_pwd = reduce_hash(curr_pwd_hash, j)
        if j == chain_length-1:
            root = insert(root, curr_pwd, curr_hash, curr_pwd)

# Print the rainbow table
print("Rainbow table:")
print("{:<10} {:<20} {:<20}".format("Index", "Random Password", "Last Value"))
print("-" * 50)
def print_tree(root, index):
    if root:
        print_tree(root.left, index)
        print("{:<10} {:<20} {:<20}".format(index, root.password, root.value))
        print_tree(root.right, index+1)
print_tree(root, 0)

# Prompt the user for a password hash to crack
password_hash = input("Enter the MD5 hash of the password to crack: ")
curr_hash = password_hash
for i in range(chain_length):
    curr_pwd = reduce_hash(curr_hash, i)
    node = Node(curr_pwd)
    node = search(root, curr_pwd)
    if node is not None:
        if node.key == curr_hash:
            print("Password found:", node.password)
            break
    curr_hash = hashlib.md5(curr_pwd.encode('utf-8')).hexdigest()
else:
    print("Password not found in the rainbow table.")
