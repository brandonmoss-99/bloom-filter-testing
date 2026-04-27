import matplotlib.pyplot as plt
import numpy as np
from bloom_filter import BloomFilter
import random

def plot(bf: BloomFilter):
    data: list[bool] = bf.get_data()

    # Get nearest square shape for size, by returning factor pair closest to the sqrt
    shape = []
    for i in range(1, int(len(data) ** 0.5) + 1):
        if len(data) % i == 0:
            print([i, len(data) // i])
            shape = [i, len(data) // i]

    print(len(data))
    print(f"Resize to {shape}")
    a = np.array(data).reshape(shape)

    plt.imshow(a)
    plt.show()




if __name__ == '__main__':
    # 0.01 = 1% FP rate
    fp_rate = 0.01
    items = 10000
    load_rate = 100

    # How many items to load into the filter
    item_load = int(items / (100/load_rate))

    bf = BloomFilter(fp_rate, items)

    for i in range(item_load + 1):
        insert_str = str(random.getrandbits(128))
        bf.insert(insert_str)
    
    # Print size
    plot(bf)