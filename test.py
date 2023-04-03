import hashlib
import random
import string

def generate_password():
    return ''.join(random.choices(list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'), k=6))

def generate_hash_chain(password, chain_length):
    hash_value = hashlib.md5(password.encode('utf-8')).hexdigest()
    chain = [(hash_value, password)]
    for i in range(chain_length):
        password = reduce(hash_value, i)
        hash_value = hashlib.md5(password.encode('utf-8')).hexdigest()
        chain.append((hash_value, password))
    return chain

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

# Test the reduction function
alphabet = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
for i in range(10):
    hash_value = hashlib.md5(generate_password().encode('utf-8')).hexdigest()
    chain = generate_hash_chain(hash_value, 100)
    for j in range(len(chain)):
        recovered_password = reduce(chain[j][0], j, alphabet)
        if recovered_password != chain[j][1]:
            print("Error: Failed to recover password for hash chain", i)
            break
    else:
        print("Successfully recovered password for hash chain", i)
