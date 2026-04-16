from bloom_filter import BloomFilter
import random
import multiprocessing
import time
from functools import partial

def task(bf: BloomFilter, test_search_count: int):
    # Load the filter up with n items
    insert_total_ns = 0
    for i in range(bf.n):
        insert_tic = time.perf_counter_ns()
        insert_str = str(random.getrandbits(128))
        bf.insert(insert_str)
        insert_toc = time.perf_counter_ns()
        insert_total_ns += insert_toc - insert_tic
    
    # Now run a number of searches for random values to check the fp rate
    fp_searches = 0
    search_total_ns = 0
    for i in range(test_search_count):
        search_tic = time.perf_counter_ns()
        search_str = str(random.getrandbits(128))
        if bf.search(search_str):
            fp_searches += 1
        search_toc = time.perf_counter_ns()
        search_total_ns += search_toc - search_tic
    
    # Clear the bloom filter once the task is done, so Python doesn't try and
    # re-use the already populated filter for the next task and skew results
    bf.clear()

    avg_item_insert_time = insert_total_ns/bf.n
    avg_item_search_time = search_total_ns/test_search_count

    return (((fp_searches/test_search_count)*100), avg_item_insert_time, avg_item_search_time)


if __name__ == '__main__':
    # 0.01 = 1% FP rate
    fp_rate = 0.001
    items = 50000
    test_search_count = 5000
    test_runs = 100

    test_results = list()

    print(f"Want to handle {items} items with false positive rate ~{fp_rate * 100}%")

    # Generate the Bloom Filter objects for each task to use
    test_iter = [BloomFilter(fp_rate, items)]*test_runs

    # Run the tests in parallel over each CPU core
    with multiprocessing.Pool() as pool:
        print(f"Running workload over {multiprocessing.cpu_count()} CPUs")
        # Partial generates a new function of the specified one with pre-filled arguments, 
        # allows passing in extra arguments to the function to run
        for result in pool.map(partial(task, test_search_count=test_search_count), test_iter):
            test_results.append(result)

    # Output stats
    print(f"Avg FP rate over {test_runs} runs of {test_search_count} searches: {round(sum(i for i, _, _ in test_results)/len(test_results),3)}%. Target: ~{fp_rate * 100}%")
    print(f"Avg of the avg per-item insert time over {test_runs} runs of inserting {items} items through {test_iter[0].k} hash functions: {round(sum(i for _, i, _ in test_results)/len(test_results),3)}ns ({round(1_000_000_000/(sum(i for _, i, _ in test_results)/len(test_results)), 3)} inserts/s)")
    print(f"Avg of the avg per-item search time over {test_runs} runs of searching for {test_search_count} items through {test_iter[0].k} hash functions: {round(sum(i for _, _, i in test_results)/len(test_results),3)}ns ({round(1_000_000_000/(sum(i for _, _, i in test_results)/len(test_results)), 3)} searches/s)")
