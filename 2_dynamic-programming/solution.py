import functools
import time

import matplotlib.pyplot as plt
import numpy as np


def format_elapsed_time(elapsed_seconds: float) -> str:
    if elapsed_seconds < 1e-3:
        return f"{elapsed_seconds * 1e6:.1f} µs"
    if elapsed_seconds < 1:
        return f"{elapsed_seconds * 1e3:.1f} ms"
    return f"{elapsed_seconds:.2f} s"


def plot_scaling(series, log_log_fit=False):
    """series: dict mapping a label to (ns, times) pairs."""

    plt.figure()
    title_parts = []

    for label, (ns, times) in series.items():
        [line] = plt.loglog(ns, times, "o", label=f"{label} (measured)")
        color = line.get_color()

        if log_log_fit:
            # Skip the first point - its overhead-dominated timing skews the fit
            log_n = np.log(ns[1:])
            log_t = np.log(times[1:])

            gradient, intercept = np.polyfit(log_n, log_t, 1)
            fit_line = np.exp(intercept) * np.array(ns) ** gradient
            plt.loglog(
                ns,
                fit_line,
                "-",
                color=color,
                label=f"{label} fit: slope={gradient:.2f}",
            )
            title_parts.append(f"{label}: {gradient:.2f}")

    plt.xlabel("n")
    plt.ylabel("time (s)")
    plt.legend()
    plt.grid(True, which="major", alpha=0.5)
    plt.grid(True, which="minor", alpha=0.2)

    if title_parts:
        plt.title("Scaling exponents — " + ", ".join(title_parts))

    plt.show()


def make_edit_distance(cached: bool = False):
    def edit_distance(a, b):
        if len(a) == 0:
            distance = len(b)
        elif len(b) == 0:
            distance = len(a)
        elif a[-1] == b[-1]:
            return edit_distance(a[:-1], b[:-1])
        else:
            return 1 + min(
                edit_distance(a[:-1], b[:-1]),
                edit_distance(a[:-1], b),
                edit_distance(a, b[:-1]),
            )
        return distance

    if cached:
        edit_distance = functools.cache(edit_distance)
    return edit_distance


edit_distance_naive = make_edit_distance()
edit_distance_cached = make_edit_distance(cached=True)


def create_distance_lookup(a, b):
    lookup = np.empty((len(a) + 1, len(b) + 1), dtype=int)

    # Populate the lookup row by row
    for ii in range(lookup.shape[0]):
        for jj in range(lookup.shape[1]):
            # Baseline case if either string is empty
            if ii == 0:
                lookup[ii, jj] = jj
            elif jj == 0:
                lookup[ii, jj] = ii

            # The result if the final character mataches
            elif a[ii - 1] == b[jj - 1]:
                lookup[ii, jj] = lookup[ii - 1, jj - 1]

            # Add, delete or swap
            else:
                lookup[ii, jj] = 1 + min(
                    lookup[ii - 1, jj - 1], lookup[ii - 1, jj], lookup[ii, jj - 1]
                )

    return lookup


def edit_distance_bottom_up(a, b):
    lookup = create_distance_lookup(a, b)
    edit_distance = lookup[-1, -1]

    return edit_distance, lookup


def backtrack_edit_script(a, b, lookup):
    ii, jj = len(a), len(b)
    operations = []  # discovered tail-first: last character of the alignment first

    while not (ii == 0 and jj == 0):
        # Base case edges where ii == 0 or jj == 0
        if ii == 0:
            operations.append(("insert", b[jj - 1]))
            jj -= 1
            continue
        if jj == 0:
            operations.append(("delete", a[ii - 1]))
            ii -= 1
            continue

        # Free diagonal move when the characters already match
        if a[ii - 1] == b[jj - 1]:
            operations.append(("match", a[ii - 1]))
            ii -= 1
            jj -= 1
            continue

        # Otherwise step to whichever neighbor is cheapest
        diag, up, left = lookup[ii - 1, jj - 1], lookup[ii - 1, jj], lookup[ii, jj - 1]
        best = min(diag, up, left)

        if best == diag:
            operations.append(("sub", a[ii - 1], b[jj - 1]))
            ii -= 1
            jj -= 1
        elif best == up:
            operations.append(("delete", a[ii - 1]))
            ii -= 1
        else:
            operations.append(("insert", b[jj - 1]))
            jj -= 1

    operations.reverse()  # now in left-to-right position order

    # Replay the ops in order on a fresh copy of `a`, tracking a running
    # position, so each snapshot reflects the edits applied so far in order.
    edits = []
    words = []
    word = a
    pos = 0

    for operation in operations:
        op_type = operation[0]

        if op_type == "match":
            pos += 1
            continue

        if op_type == "sub":
            _, old, new = operation
            word = word[:pos] + new + word[pos + 1 :]
            edits.append(f"-{old}/+{new}")
            pos += 1
        elif op_type == "delete":
            _, old = operation
            word = word[:pos] + word[pos + 1 :]
            edits.append(f"-{old}")
        elif op_type == "insert":
            _, new = operation
            word = word[:pos] + new + word[pos:]
            edits.append(f"+{new}")
            pos += 1

        words.append(word)

    return edits, words


def basic_test():
    word_a = "intention"
    word_b = "execution"

    start = time.perf_counter()
    result = edit_distance_cached(word_a, word_b)
    elapsed = time.perf_counter() - start

    print(
        f"A: {word_a}, B: {word_b}, distance: {result} | time: {format_elapsed_time(elapsed)} "
    )


def compare_methods(methods: dict[str, callable], n_range):
    """methods: label -> function(a, b) -> distance (int)."""

    series = {}

    for label, method in methods.items():
        ns = []
        times = []

        for n in n_range:
            a = "x" * n
            b = "y" * n

            start = time.perf_counter()
            method(a, b)
            elapsed = time.perf_counter() - start
            ns.append(n)
            times.append(elapsed)

        series[label] = (ns, times)

    plot_scaling(series, log_log_fit=True)


def bottom_up():

    a = "cats"
    b = "rag"

    result, lookup = edit_distance_bottom_up(a, b)

    print(f"a: {a}, b: {b}, distance: {result}")
    print(lookup)

    edits, words = backtrack_edit_script(a, b, lookup)
    print(edits, f"| number of edits: {len(edits)}")
    print(words)


def timed_cached(a, b):
    edit_distance_cached.cache_clear()
    return edit_distance_cached(a, b)


def timed_bottom_up(a, b):
    return edit_distance_bottom_up(a, b)[0]


def main():

    bottom_up()

    # compare_methods(
    #     {
    #         # "naive": edit_distance_naive,
    #         "cached": timed_cached,
    #         "bottom-up": timed_bottom_up,
    #     },
    #     n_range=range(1, 200, 20),
    # )


if __name__ == "__main__":
    main()
