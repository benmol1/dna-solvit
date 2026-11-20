weights = [
    4,
    11,
    25,
    14,
    29,
    29,
    8,
    29,
    1,
    3,
    16,
    1,
    11,
    14,
    10,
    28,
    9,
    25,
    18,
    28,
    21,
    25,
    29,
    5,
    15,
]
values = [
    59,
    45,
    22,
    40,
    1,
    53,
    3,
    32,
    2,
    46,
    35,
    24,
    35,
    23,
    7,
    2,
    41,
    40,
    10,
    21,
    25,
    6,
    21,
    12,
    52,
]
CAPACITY = 100

order = sorted(range(25), key=lambda i: values[i] / weights[i], reverse=True)


def knapsack_greedy(weights, values, capacity):
    """Pack the bag in descending order of value density. No swaps."""
    total_w = total_v = item_count = 0
    for i in order:
        if total_w + weights[i] <= capacity:
            total_w += weights[i]
            total_v += values[i]
            item_count += 1
    return (total_v, total_w, item_count)


def knapsack_dp(weights, values, capacity):
    """Return the best total value achievable within capacity."""
    best = [0] * (capacity + 1)  # best[c] = ???
    ...
    return best[capacity]


def random_subset_test():
    import random

    weights = [
        4,
        11,
        25,
        14,
        29,
        29,
        8,
        29,
        1,
        3,
        16,
        1,
        11,
        14,
        10,
        28,
        9,
        25,
        18,
        28,
        21,
        25,
        29,
        5,
        15,
    ]

    trials = 100_000
    ok = sum(
        sum(w for w in weights if random.random() < 0.5) <= 100 for _ in range(trials)
    )
    print(ok / trials)


def main():
    # greedy = knapsack_greedy(weights, values, CAPACITY)
    # print(f"total_value: {greedy[0]}, total_weight: {greedy[1]}, item_count: {greedy[2]}")

    random_subset_test()


if __name__ == "__main__":
    main()
