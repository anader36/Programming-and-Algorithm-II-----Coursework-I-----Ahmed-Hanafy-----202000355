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

# Define a function for the reduction step
def reduce_hash(hash_val, iteration_num):
    first_eight_chars = hash_val[:8]
    int_val = int(first_eight_chars, 16) + iteration_num
    new_hash_val = hashlib.md5(str(int_val).encode('utf-8')).hexdigest()
    return new_hash_val

# Define the chain length
chain_length = 10

# Generate random passwords and hash them using MD5
passwords = []
print("Generating passwords...")
for i in range(1000):
    password = ''.join(random.choices(list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'), k=6))
    passwords.append(password)
hashes = [hashlib.md5(password.encode('utf-8')).hexdigest() for password in passwords]
print("Hashing passwords...")

# Create a rainbow table with the passwords and hashes
root = None
for i in range(len(passwords)):
    password = passwords[i]
    hash_val = hashes[i]
    for j in range(chain_length):
        new_password = reduce_hash(hash_val, j)
        new_hash_val = hashlib.md5(new_password.encode('utf-8')).hexdigest()
        hash_val = new_hash_val
    root = insert(root, hash_val, password)

# Print the rainbow table
print("Rainbow table:")
print("{:<10} {:<34}".format("Password", "Hash"))
print("-" * 46)
def print_tree(root):
    if root:
        print_tree(root.left)
        print("{:<10} {:<34}".format(root.value, root.key))
        print_tree(root.right)
print_tree(root)

# Ask the user to input an MD5 hash to crack
hash_to_crack = input("Enter an MD5 hash to crack: ")

# Iterate through the chain to find the original password
for i in range(chain_length):
    reduced_hash = reduce_hash(hash_to_crack, i)
    node = root
    while node is not None:
        if node.key == reduced_hash:
            print("The original password is:", node.value)
            break
        elif node.key < reduced_hash:
            node = node.right
        else:
            node = node.left
    if node is not None:
        break
else:
    print("Failed to crack the hash.")
