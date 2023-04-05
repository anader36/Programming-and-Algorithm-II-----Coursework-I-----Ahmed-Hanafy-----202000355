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

# Ask the user to choose a hashing algorithm from the following (MD5, SHA1, SHA256)
print("Choose a hashing algorithm from the following:")
print("1. MD5")
print("2. SHA1")
print("3. SHA256")
choice = input("Please enter your choice: ")
if choice == '1':
    algorithm = hashlib.md5
elif choice == '2':
    algorithm = hashlib.sha1
elif choice == '3':
    algorithm = hashlib.sha256
else:
    print("Invalid choice.")
    exit()

# Generate random passwords and hash them using the chosen algorithm
passwords = []
print("Generating passwords...")
for i in range(1000):
    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=6))
    passwords.append(password)
hashes = [algorithm(password.encode('utf-8')).hexdigest() for password in passwords]
print("Hashing passwords...")

# Define the reduction function and chain length
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

chain_length = 10000

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
print("{:<10} {:<34} {:<10}".format("Password", "Last value in the chain", "Hash"))
print("-" * 70)
def print_tree(root):
    if root:
        print_tree(root.left)
        print("{:<10} {:<34} {:<10}".format(root.value, reduce(root.key, chain_length - 1), root.key))
        print_tree(root.right)
print_tree(root)

def binary_search(root, hash_to_find):
    current_node = root
    while current_node is not None:
        if current_node.key == hash_to_find:
            return current_node.value
        elif current_node.key < hash_to_find:
            current_node = current_node.right
        else:
            current_node = current_node.left
    return None

hash_to_find = input("Please enter the hash to find the original password: ")
password = binary_search(root, hash_to_find)
if password is None:
    print("Hash is not found in the rainbow table.")
else:
    last_value = reduce(hash_to_find, chain_length - 1)
    print("The Original Password for this hash is '{}': {} -- followed by the last chain value: {}".format(hash_to_find, password, last_value))
