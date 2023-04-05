import hashlib
import random
import string

class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value

def insert(table, key, value):
    table[key] = Node(key, value)

print("Choose a hashing algorithm from the following:")
print("1. MD5")
print("2. SHA1")
print("3. SHA256")

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
    else:
        print("Invalid choice. Please enter a valid choice (1, 2, or 3).")    

passwords = []
print("Generating passwords...")
for i in range(1000):
    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=8))
    passwords.append(password)
hashes = [algorithm(password.encode('utf-8')).hexdigest() for password in passwords]
print("Hashing passwords...")

def reduce(hash_string: str, iteration: int, alphabet= string.ascii_letters + string.digits + string.punctuation, word_length: int = 8) -> str:
    if alphabet is None:
        alphabet = list(string.ascii_letters + string.digits + string.punctuation)

    value = (int(hash_string, 16) + iteration) % (2 ** 40)
    result = []
    for i in range(word_length):
        mod = value % len(alphabet)
        value //= len(alphabet)
        result.append(alphabet[mod])
    return "".join(result)

chain_length = 1000

hash_table = {}
for i in range(len(passwords)):
    password = passwords[i]
    hash_val = algorithm(password.encode('utf-8')).hexdigest()
    for j in range(chain_length):
        password = reduce(hash_val, j)
        hash_val = algorithm(password.encode('utf-8')).hexdigest()
    insert(hash_table, hash_val, password)

print("Rainbow table:")
print("{:<10} {:<34} {:<10}".format("Password", "Last value in the chain", "Hash"))
print("-" * 70)

for key in hash_table:
    node = hash_table[key]
    print("{:<10} {:<34} {:<10}".format(node.value, reduce(node.key, chain_length - 1), node.key))

hash_val_to_find = input("Enter the hash value to find the original password: ")
password_node = hash_table.get(hash_val_to_find)
if password_node is None:
    print("Hash value not found in the rainbow table.")
else:
    password = password_node.value
    last_chain_value = reduce(hash_val_to_find, chain_length - 1)
    print("The original password for this hash value is '{}': {} -- followed by the last chain value: {}".format(hash_val_to_find, password, last_chain_value))
