import string

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

hash_value = "ff0610646da0c1b226c9529cb08a1ac1"
chain_length = 1001

for i in range(chain_length):
    password = reduce(hash_value, i)
    hash_value = password.encode("utf-8").hex()
    print(f"Iteration {i}: {password} -> {hash_value}")
