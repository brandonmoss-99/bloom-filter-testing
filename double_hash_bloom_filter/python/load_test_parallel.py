from bloom_filter_np import BloomFilter
import random
import multiprocessing
import time
from functools import partial
import matplotlib.pyplot as plt

def task(bf: BloomFilter, test_search_count: int, item_load: int):
    # Load the filter up with n items
    insert_total_ns = 0
    for i in range(item_load + 1):
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

    avg_item_insert_time = insert_total_ns/item_load
    avg_item_search_time = search_total_ns/test_search_count

    return (((fp_searches/test_search_count)*100), avg_item_insert_time, avg_item_search_time)


if __name__ == '__main__':
    # 0.01 = 1% FP rate
    fp_rate = 0.01
    items = 5000
    test_search_count = 5000
    test_runs = 20
    load_rates = [i for i in range(10, 101, 10)] # % of filter's capacity to fill with items

    test_results = dict()

    print(f"Want to handle {items} items with false positive rate ~{fp_rate * 100}%")


    # Run the tests in parallel over each CPU core
    with multiprocessing.Pool() as pool:
        for load in load_rates:
            load_results = list()
            # Generate the Bloom Filter objects for each task to use
            test_iter = [BloomFilter(fp_rate, items)]*test_runs

            # How many items to load into the filter
            item_load = int(items / (100/load))

            print(f"Running {load}% filled workload over {multiprocessing.cpu_count()} CPUs")
            # Partial generates a new function of the specified one with pre-filled arguments, 
            # allows passing in extra arguments to the function to run
            for result in pool.map(partial(task, test_search_count=test_search_count, item_load = item_load), test_iter):
                load_results.append(result)
        
            test_results[load] = load_results

    # Visualise

    # Get average (of averages) for each load to plot
    plot_stats = dict()
    for load in load_rates:
        fp_avg = round(sum(i for i, _, _ in test_results[load])/len(test_results[load]),3)
        insert_avg = round(sum(i for _, i, _ in test_results[load])/len(test_results[load]),3)
        search_avg = round(sum(i for _, _, i in test_results[load])/len(test_results[load]),3)

        load_stat = [fp_avg, insert_avg, search_avg]
        plot_stats[load] = load_stat
    

    x = load_rates
    fp_y = [plot_stats[load][0] for load in load_rates]
    insert_y = [plot_stats[load][1] for load in load_rates]
    search_y = [plot_stats[load][2] for load in load_rates]


    plt.bar(x, fp_y, color='blue', width=1)
    plt.axhline(y=fp_rate * 100, color='r', linestyle='--')
    plt.title(f'Bloom filter load vs FP rate for capacity: {items}, FP target {fp_rate * 100}%')
    plt.xlabel('Bloom filter item load (%)')
    plt.ylabel('False positive rate (%)')
    plt.show()
