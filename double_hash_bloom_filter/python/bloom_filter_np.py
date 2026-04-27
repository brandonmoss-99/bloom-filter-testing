import mmh3
import math
import numpy as np

### Switch to using NumPy rather than Python native

class BloomFilter:
    def __init__(self, fpr: float, n: int):
        self.fpr = fpr   # False positive rate. Should be between 0 and 1
        self.n = n      # Number of items
        self.m = self.get_optimal_size()      # Optimal number of bits to store
        self.k = self.get_optimal_hashes()    # Optimal number of hash functions to use
        self._data = self.__create_data()     # Bloom filter data
        self._hash_seeds = self.__generate_hash_seeds()     # The seeds to use for each hash function used
    
    
    # Override the print method to output the contents of the bloom filter as 0/1 string
    def __str__(self) -> str:
        return ''.join(map(str, list(map(int, self._data))))


    def get_optimal_size(self) -> int:
        return int(-(self.n * math.log(self.fpr))/(math.log(2) ** 2))
    

    def get_optimal_hashes(self) -> int:
        return int((self.m/self.n)*math.log(2))
    

    def get_data(self) -> np.ndarray:
        return self._data


    def __create_data(self) -> np.ndarray:
        #return [False] * self.m
        return np.full(self.m, dtype=bool, fill_value=False)
    

    def __generate_hash_seeds(self) -> list[int]:
        seeds = list()
        # Only need 2 hash seeds for the 2 'real' hash functions
        for i in range(2):
            seeds.append(i)
        return seeds
    

    def insert(self, data: str):
        # Calculate 2 hashes, and then generate the additional hash functions
        # using those 2
        h_0 = mmh3.hash(data, seed=self._hash_seeds[0], signed=False)
        h_1 = mmh3.hash(data, seed=self._hash_seeds[1], signed=False)

        # Because we multiply by h_1 to generate the remaining hashes, make sure that if the hash is 0
        # we change this to a 1, otherwise all the other hash values will multiply to become 0
        h_1 |= 1

        # Calculate the hashes
        for i in range(self.k):
            self._data[(h_0 + i * h_1) % self.m] = True
            


    def search(self, data: str) -> bool:
        # Run the search through the same hashes as to insert,
        # and check ALL locations are True before returning True
        matches = 0

        # Calculate 2 hashes, and then generate the additional hash functions
        # using those 2
        h_0 = mmh3.hash(data, seed=self._hash_seeds[0], signed=False)
        h_1 = mmh3.hash(data, seed=self._hash_seeds[1], signed=False)

        # Because we multiply by h_1 to generate the remaining hashes, make sure that if the hash is 0
        # we change this to a 1, otherwise all the other hash values will multiply to become 0
        h_1 |= 1

        # Calculate the hashes
        for i in range(self.k):
            if self._data[(h_0 + i * h_1) % self.m]:
                matches += 1

        return matches == self.k  


    def clear(self):
        self._data = self.__create_data()
