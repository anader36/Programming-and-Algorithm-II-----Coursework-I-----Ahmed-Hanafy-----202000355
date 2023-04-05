import hashlib
import random
import string

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

# Create a dictionary (hash table) with the passwords and hashes
rainbow_table = {}
for i in range(len(passwords)):
    hash_value = hashes[i]
    password = passwords[i]
    for j in range(chain_length):
        password = reduce(hash_value, j)
        hash_value = algorithm(password.encode('utf-8')).hexdigest()
    rainbow_table[hash_value] = password

# Print the rainbow table
print("Rainbow table:")
print("{:<10} {:<34} {:<10}".format("Password", "Last value in the chain", "Hash"))
print("-" * 70)
for hash_value, password in rainbow_table.items():
    print("{:<10} {:<34} {:<10}".format(password, reduce(hash_value, chain_length - 1), hash_value))

def find_password(rainbow_table, hash_to_find):
    if hash_to_find in rainbow_table:
        return rainbow_table[hash_to_find]
    else:
        return None

hash_to_find = input("Please enter the hash to find the original password: ")
password = find_password(rainbow_table, hash_to_find)
if password is None:
    print("Hash is not found in the rainbow table.")
else:
    last_value = reduce(hash_to_find, chain_length - 1)
    print("The Original Password for this hash is '{}': {} -- followed by the last chain value: {}".format(hash_to_find, password, last_value))
