# Ahmed Nader Hussein - TKH ID: 202000355
# Code Title: Final Project - Rainbow Table Generator - Binary Tree
#Importing necessary libraries
import hashlib
import random
import string

# Define a class for the nodes in the binary tree
class Node:
    def __init__(self, key, value=None):
        self.key = key  # The key to be stored
        self.value = value # The value to be stored
        self.left = None # The left child of the node
        self.right = None # The right child of the node

# Define a function to insert a node into the binary tree
# Parameters:
#     root (Node): The root node of the binary tree.
#     key (int): The key value for the new node.
#     value (str): The value to be stored in the new node.
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

# Asking user to choose a hashing algorithm from the following options: MD5, SHA1, SHA256, SHA512
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

# Generate random passwords and hash them using the chosen algorithm 
passwords = []
print("Generating passwords...")
for i in range(100):
    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=6))
    passwords.append(password)
hashes = [algorithm(password.encode('utf-8')).hexdigest() for password in passwords]
print("Hashing passwords...")

# Define the reduction function and chain length
# Parameters:
#     hash_string (str): The input hash value.
#     iteration (int): The number of times the reduction function is applied.
#     alphabet (str): The alphabet used to generate the reduced values.
#     word_length (int): The length of the reduced values.
def reduce(hash_string: str, iteration: int, alphabet= string.ascii_letters + string.digits + string.punctuation, word_length: int = 6) -> str:
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

# Define the chain length for the rainbow table
chain_length = 1000

# Create a binary tree with the passwords and hashes
root = None
for i in range(len(passwords)):
    hash_value = hashes[i]
    password = passwords[i]
    for j in range(chain_length):
        password = reduce(hash_value, j)
        hash_value = algorithm(password.encode('utf-8')).hexdigest()
    root = insert(root, hash_value, password)

# Print the rainbow table
print("Rainbow table:")
print("{:<10} {:<34} {:<10}".format("Password", "Last value in the chain", "Hash Value"))
print("-" * 70)
def print_tree(root):
    if root:
        print_tree(root.left)
        print("{:<10} {:<34} {:<10}".format(root.value, reduce(root.key, chain_length - 1), root.key))
        print_tree(root.right)
print_tree(root)

# Define a function to search for a hash in the binary tree
# Parameters:
#     root (Node): The root node of the binary tree.
#     hash_to_find (str): The hash value to be searched for.
def binary_search(root, hash_to_find):
    current_node = root
    # Traverse through the binary tree to find the hash value
    while current_node is not None:
    # If the hash value is found in the current node, return the corresponding password
        if current_node.key == hash_to_find:
            return current_node.value
    # If the hash value is greater than the key in the current node, move to the right subtree
        elif current_node.key < hash_to_find:
            current_node = current_node.right
    # If the hash value is less than the key in the current node, move to the left subtree
        else:
            current_node = current_node.left
    # If the hash value is not found in the binary tree, return None
    return None

# Ask the user to enter a hash value to find the original password
hash_to_find = input("Please enter the hash to find the original password: ")
# Search for the password corresponding to the given hash value in the binary tree
password = binary_search(root, hash_to_find)
# If the password is not found, print a message indicating that the hash value is not in the rainbow table
if password is None:
    print("Hash is not found in the rainbow table.")
# If the password is found, calculate the last value in the chain for the given hash value and print the password and the last value
else:
    last_value = reduce(hash_to_find, chain_length - 1)
    print("The Original Password for this hash is '{}': {} -- followed by the last chain value: {}".format(hash_to_find, password, last_value))
