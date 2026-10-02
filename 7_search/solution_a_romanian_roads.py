import heapq

roads: dict[str, dict[str, int]] = {
    "Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
    "Zerind": {"Arad": 75, "Oradea": 71},
    "Oradea": {"Zerind": 71, "Sibiu": 151},
    "Sibiu": {"Arad": 140, "Oradea": 151, "Fagaras": 99, "RimnicuVilcea": 80},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Drobeta": 75},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Craiova": {"Drobeta": 120, "RimnicuVilcea": 146, "Pitesti": 138},
    "RimnicuVilcea": {"Sibiu": 80, "Craiova": 146, "Pitesti": 97},
    "Fagaras": {"Sibiu": 99, "Bucharest": 211},
    "Pitesti": {"RimnicuVilcea": 97, "Craiova": 138, "Bucharest": 101},
    "Bucharest": {"Fagaras": 211, "Pitesti": 101, "Giurgiu": 90, "Urziceni": 85},
    "Giurgiu": {"Bucharest": 90},
    "Urziceni": {"Bucharest": 85, "Hirsova": 98, "Vaslui": 142},
    "Hirsova": {"Urziceni": 98, "Eforie": 86},
    "Eforie": {"Hirsova": 86},
    "Vaslui": {"Urziceni": 142, "Iasi": 92},
    "Iasi": {"Vaslui": 92, "Neamt": 87},
    "Neamt": {"Iasi": 87},
}


source = "Arad"
destination = "Bucharest"


def breadth_first_search(
    roads: dict[str, dict[str, int]], source: str, destination: str
) -> None:
    """Find a route from source to destination by fewest hops (BFS) and print it with its total distance."""

    queue = [source]
    visited = {source}
    parents = {}

    while queue:
        current = queue.pop(0)

        if current == destination:
            break

        for neighbour in roads[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                parents[neighbour] = current
                queue.append(neighbour)

    return get_path_from_parents(roads, source, destination, parents)


def get_path_from_parents(roads, source, destination, parents):
    hop_dest = destination
    hop_source = ""
    path = []
    length = 0

    while hop_source != source:
        path.append(hop_dest)
        hop_source = parents[hop_dest]
        length += roads[hop_source][hop_dest]
        hop_dest = hop_source

    path.append(source)
    path.reverse()
    return path, length


def heapq_test() -> None:
    """Demonstrate that heapq.heappop always returns the smallest (priority, item) tuple pushed so far."""

    pq = []
    heapq.heappush(pq, (140, "Sibiu"))
    heapq.heappush(pq, (75, "Zerind"))
    heapq.heappush(pq, (118, "Timisoara"))

    while pq:
        print(heapq.heappop(pq))


def universal_cost_search(
    roads: dict[str, dict[str, int]], source: str, destination: str
) -> tuple[int | None, dict[str, str]]:
    """Find the cheapest route from source to destination (uniform-cost search) and return (cost, parents)."""

    # Initialise queue
    pq = [(0, source)]

    # Initialise the set of visited cities, the parents dictionary and the best-known distance dictionary
    visited = set()
    parents = {}
    best_known = {source: 0}

    # Loop over the queue, each time visiting the cheapest (shortest-distance) queue member
    while pq:
        current_distance, current_city = heapq.heappop(pq)

        # If the current city has already been visited then skip this item in the queue
        # (as a cheaper path to this city will have already been found)
        if current_city in visited:
            continue
        else:
            visited.add(current_city)

        # If this is the destination city then exit the loop
        if current_city == destination:
            break

        # For each neighbour of the current city, compute the total distance via current_city.
        for neighbour, marginal_distance in roads[current_city].items():
            interim_total_distance = current_distance + marginal_distance

            # If we haven't visited the neighbour yet and we don't already have a cheaper path, record this as the best-known path so far
            if neighbour not in visited and (
                neighbour not in best_known
                or interim_total_distance < best_known[neighbour]
            ):
                # update best_known
                best_known[neighbour] = interim_total_distance
                # update parents
                parents[neighbour] = current_city
                # push onto heap
                heapq.heappush(pq, (interim_total_distance, neighbour))

    return get_path_from_parents(roads, source, destination, parents)


def main() -> None:
    path, length = universal_cost_search(roads, source, destination)
    print(f"Path: {path} | Length: {length}")


if __name__ == "__main__":
    main()
