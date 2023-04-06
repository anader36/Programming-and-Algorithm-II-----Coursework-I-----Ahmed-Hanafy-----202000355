#Ahmed Basem - 202000188
import random, string, hashlib, re     # Standard Libraries
import HashTable, BinaryTree       # Custom Libraries


class RainbowTable:

    # Constructor / Settings
    def _init_(self, charset, wordlist_size, word_length_range, chain_length, hash_method, ADT = "HASHTABLE"):
        
        #Wordlist Settings
        self.char_set = charset                     #list of characters to use in wordlist
        self.wordlist_size = wordlist_size          #number of words in wordlist
        self.word_length_range = word_length_range  #range of word lengths in wordlist
        self.words = self.create_wordlist()         #wordlist Container
        
        #Rainbow Table Settings
        self.chain_length = chain_length            # Chain Length for Rainbow Table
        self.hash_method = hash_method              # Hash Method for Rainbow Table
        self.ADT = ADT.upper()                      # Abstract Data Type for Rainbow Table (HashTable, BinaryTree, Array)
        
        # Abstract Data Type for Rainbow Table
        match self.ADT.upper():
            case "HASHTABLE":                       # Search Complexity : O(1) , Insertion Complexity : O(1)
                self.RainbowTable = HashTable.HashTable(wordlist_size)
            case "BINARYTREE":                      # Search Complexity : O(log n) , Insertion Complexity : O(log n)
                print("Binary Tree not implemented yet")
                exit()
            case "ARRAY":                           # Search Complexity : O(n) , Insertion Complexity : O(n)
                self.RainbowTable = []
            case _:
                print("Invalid ADT")
                exit()
        return None
        
    # Wordlist Generator
    def create_wordlist(self):
        self.words = []     # Wordlist Container
        print()
        print("Creating Wordlist...")

        for i in range(self.wordlist_size):
            # TODO: fix Range for wordlist generation
            word_len = random.randint(self.word_length_range[0], self.word_length_range[1])  # Choose a random word length within the given range
            # Generate a random string of characters using the chosen character set
            random_string = ''.join(random.choice(self.char_set) for i in range(word_len))

            # Add the random string to the list
            if random_string not in self.words:
                self.words.append(random_string)

        # Sort the wordlist
        self.words.sort()

        print("[i] -",len(self.words),"words generated")
        print("-------------------------------")
        return self.words
        
    # Hash Function
    def hash_function(self, PT_password):

        # Hash the password using the chosen hash method
        match self.hash_method.lower():
            case "sha1":
                return hashlib.sha1(PT_password.encode()).hexdigest()       
            case "sha256":
                return hashlib.sha256(PT_password.encode()).hexdigest()
            case "sha512":
                return hashlib.sha512(PT_password.encode()).hexdigest()
            case "md5":
                return hashlib.md5(PT_password.encode()).hexdigest()
            case _:
                print("Invalid Hash Method")
                exit()
            
    # Reduction Function
    def reduction_function(self, Hash):

        Val_from_Hash = int(Hash, 16)   # Convert the hash to a base 10 integer
        reduced_hash = ""               # Reduced Hash Container

        # Reduce the hash to a word of the specified length (Max word length)
        while len(reduced_hash) < self.word_length_range[1]:
            # Add the character to the reduced hash
            reduced_hash = reduced_hash + self.char_set[Val_from_Hash % len(self.char_set)]
            # Reduce the value of the hash character
            Val_from_Hash = Val_from_Hash//len(self.char_set)

        return reduced_hash
    
    # Store Chain in Rainbow Table According to ADT
    def store_Chain(self,chain):
        if self.ADT == "HASHTABLE":
            self.RainbowTable.add(chain[1],chain[0]) # [1] Chain End , [0] Chain Start
        elif self.ADT == "ARRAY":
            self.RainbowTable.append(chain)
        return None
    
    # Rainbow Table Generator
    def build_rainbow_table(self , Print = False):
        print()
        print("Building Rainbow Table...")

        # For each word in the wordlist
        for word in self.words:
            chain = ["",""]  # Chain Container
            chain[0] = word  # Add the word to the chain

            if Print: print(chain[0], end=" --> ")

            chain[1] = word    # Set the chain end to the word
            
            for i in range(self.chain_length):
                # Hash the chain end
                hashed_password = self.hash_function(chain[1])
                if Print : print(hashed_password, end = " --> ")

                # Reduce the hash
                reduced_hash = self.reduction_function(hashed_password)
                if Print: print(reduced_hash, end=" --> ")
                # Add the reduced hash to the chain
                chain[1] = reduced_hash

            if Print: print(chain[1])

            # Store the chain in the rainbow table
            self.store_Chain(chain)

        if self.ADT == "HASHTABLE":
            table = self.RainbowTable.hashtable
        elif self.ADT == "ARRAY":
            table = self.RainbowTable

        print("[i] -",len(table),"chains generated" , end = " - ")
        print(len(table)*self.chain_length,"passwords computed")
        print("[T] -",(len(table)*self.chain_length)+Wordlist_Size,"passwords available")
        print("-------------------------------")
        return self.RainbowTable
    
    # Rainbow Table Search
    def search_rainbow_table(self, hash_value):
        
        OG_hash = hash_value

        # Reduce Until Chain End Match
        chain_start = None
        counter = 0
        while chain_start == None:
            counter += 1

            # Check if chain length is exceeded
            if counter > self.chain_length:
                break

            # print("looking for: ",reduce_hash(hash_value))
            
            match self.ADT.upper():
                # Hash Table Lookup
                case "HASHTABLE":
                    chain_start = self.RainbowTable.lookup(self.reduction_function(hash_value))
            
                # Array Lookup
                case "ARRAY":
                    for chain in self.RainbowTable:
                        if chain[1] == self.reduction_function(hash_value):
                            chain_start = chain[0]
                            break
            
            # Reduce Hash
            hash_value = self.hash_function(self.reduction_function(hash_value))

        
        # Get Chain Start
        if chain_start == None:
            print("[E] - Password Not Found")
        else:
            print("[S] - Found in Chain Starting with:", chain_start)
            # Reduce Untill Hash is Found
            while self.hash_function(chain_start) != OG_hash:
                chain_start = self.reduction_function(self.hash_function(chain_start))

            print("[i] - Password Found: ", chain_start)
        # Return Password
        return chain_start

    # Print Rainbow Table
    def print_rainbow_table(self):
        if self.ADT.upper() == "HASHTABLE":
            for i in range(len(self.RainbowTable.hashtable)):
                print(i, end = " ")
                
                for j in self.RainbowTable.hashtable[i]:
                    print("-->", end = " ")
                    print(j, end = " ")
                    
                print()

        elif self.ADT.upper() == "ARRAY":
            print(["Start", "End"])
            for chain in self.RainbowTable:
                print([chain[0], chain[1]])
        return None
    
    # Validate User Input
    def ValidateHash(self, hash):
        
        match self.hash_method.lower():
            case "sha1":
                pattern = re.compile("^[a-fA-F0-9]{40}$")
            case "sha256":
                pattern = re.compile("^[a-fA-F0-9]{64}$")
            case "sha512":
                pattern = re.compile("^[a-fA-F0-9]{128}$")
            case "md5":
                pattern = re.compile("^[a-fA-F0-9]{32}$")
            
        if pattern.match(hash):
            return True
        
        return False

# Main
if _name_ == "_main_":

    print("Rainbow Table Generator Starting")
    print("-------------------------------")
    
    #Settings
    Charset = string.ascii_letters + string.digits + string.punctuation

    print()
    Setup = input("Setup (Y or N): ")
    
    if Setup.upper() == "Y":
        
        Wordlist_Size = int(input("Enter Wordlist Size (1 - 1000): "))
        Word_Length_Range = [int(input("Enter Minimum Word Length: ")), int(input("Enter Maximum Word Length: "))]
        Chain_Length = int(input("Enter Chain Length: "))
        Hash_Method = input("Enter Hash Method (sha1, 256 , 512, md5): ")
        Abstract_Data_Type = input("Enter Abstract Data Type (array , hashtable): ")
        Print_Rainbow_Table_Chains = input("Print Rainbow Table Chains (Y or N): ")
        Print_Hash_Table = input("Print Hash Table (Y or N): ")
        
        

    else:
        print("[i] - Using Default Settings")
        
        # Default Settings
        Wordlist_Size = 100
        Word_Length_Range = [5, 6]
        Chain_Length = 50
        Hash_Method = "md5"
        Abstract_Data_Type = "HASHTABLE"
        Print_Rainbow_Table_Chains = "Y"
        Print_Hash_Table = "Y"

    if Print_Rainbow_Table_Chains.upper() == "Y":
        _Print = True
    else:
        _Print = False

    # Create Rainbow Table
    print("-------------------------------")
    RT1 = RainbowTable(Charset, Wordlist_Size, Word_Length_Range, Chain_Length, Hash_Method, Abstract_Data_Type)
    RT = RT1.build_rainbow_table(Print = _Print)
    
    if Print_Hash_Table.upper() == "Y":  RT1.print_rainbow_table()
    
    while True:
        print()
        uInput = input("Enter " + Hash_Method.upper() + " Hash Value to Search for: ")
        uInput = uInput.strip()
        
        if uInput == "exit":
            break
        elif not RT1.ValidateHash(uInput):
            print("[E] - Invalid Hash Value")
            continue

        RT1.search_rainbow_table(uInput)