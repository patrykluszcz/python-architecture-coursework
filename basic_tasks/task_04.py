import math
from multiprocessing import Pool, cpu_count

def f(x):
    return math.cos(x) + math.log(x + 1) ** 2


def compute_range(args):
    start, end, step = args
    results = []
    x = start
    while x < end:
        results.append((x, f(x)))
        x += step
    return results


def main():
    start = 1
    end = 1_000_0
    step = 0.01

    num_processes = cpu_count()

    chunk_size = (end - start) / num_processes
    tasks = []

    for i in range(num_processes):
        chunk_start = start + i * chunk_size
        chunk_end = chunk_start + chunk_size
        tasks.append((chunk_start, chunk_end, step))

    with Pool(num_processes) as pool:
        results = pool.map(compute_range, tasks)

    all_results = [item for sublist in results for item in sublist]

    print(f"Computed {len(all_results)} values")
    print("First 5 results:")
    for r in all_results[:5]:
        print(r)

if __name__ == "__main__":
    main()
