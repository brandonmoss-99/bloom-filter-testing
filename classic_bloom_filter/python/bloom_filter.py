import mmh3
import math

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


    def __create_data(self) -> list[bool]:
        return [False] * self.m
    

    def __generate_hash_seeds(self) -> list[int]:
        seeds = list()
        for i in range(self.k):
            seeds.append(i)
        return seeds
    

    def insert(self, data: str):
        # For each insert, run each hash with the list of seeds, 
        # and boolean OR that position in the data array to True
        for i in range(self.k):
            self._data[mmh3.hash(data, seed=self._hash_seeds[i]) % self.m] |= True
    

    def search(self, data: str) -> bool:
        # Run the search through the same hashes as to insert,
        # and check ALL locations are True before returning True
        matches = 0
        for i in range(self.k):
            if self._data[mmh3.hash(data, seed=self._hash_seeds[i]) % self.m]:
                matches += 1

        return matches == self.k  


    def clear(self):
        self._data = self.__create_data()
