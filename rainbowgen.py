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
for i in range(len(passwords)):
    root = insert(root, hashes[i], passwords[i])

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
