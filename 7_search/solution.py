import heapq



roads = {"Arad":{"Zerind":75,"Sibiu":140,"Timisoara":118},
 "Zerind":{"Arad":75,"Oradea":71}, "Oradea":{"Zerind":71,"Sibiu":151},
 "Sibiu":{"Arad":140,"Oradea":151,"Fagaras":99,"RimnicuVilcea":80},
 "Timisoara":{"Arad":118,"Lugoj":111}, "Lugoj":{"Timisoara":111,"Mehadia":70},
 "Mehadia":{"Lugoj":70,"Drobeta":75}, "Drobeta":{"Mehadia":75,"Craiova":120},
 "Craiova":{"Drobeta":120,"RimnicuVilcea":146,"Pitesti":138},
 "RimnicuVilcea":{"Sibiu":80,"Craiova":146,"Pitesti":97},
 "Fagaras":{"Sibiu":99,"Bucharest":211},
 "Pitesti":{"RimnicuVilcea":97,"Craiova":138,"Bucharest":101},
 "Bucharest":{"Fagaras":211,"Pitesti":101,"Giurgiu":90,"Urziceni":85},
 "Giurgiu":{"Bucharest":90}, "Urziceni":{"Bucharest":85,"Hirsova":98,"Vaslui":142},
 "Hirsova":{"Urziceni":98,"Eforie":86}, "Eforie":{"Hirsova":86},
 "Vaslui":{"Urziceni":142,"Iasi":92}, "Iasi":{"Vaslui":92,"Neamt":87},
 "Neamt":{"Iasi":87}}


source = "Arad"
destination = "Bucharest"

def breadth_first_search(roads, source, destination):

    queue = [source]
    visited = {source}
    parents = {}

    while queue:
        current = queue.pop(0)

        if current == destination: break

        for neighbour in roads[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                parents[neighbour] = current
                queue.append(neighbour)


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

    print(f"Path: {path}, length: {length}")


def heapq_test():
    pq = []
    heapq.heappush(pq, (140, "Sibiu"))
    heapq.heappush(pq, (75, "Zerind"))
    heapq.heappush(pq, (118, "Timisoara"))

    while pq:
        print(heapq.heappop(pq))


def universal_cost_search(roads, source, destination):
    pq = [(0, source)]
    visited = set()
    parents = {}
    best_known = {source: 0}

    while pq:
        dist, current = heapq.heappop(pq)

        if current in visited:
            continue  # stale entry, a cheaper one already settled this city
        visited.add(current)

        if current == destination:
            return dist, parents

        for neighbour, weight in roads[current].items():
            new_dist = dist + weight
            if neighbour not in visited and (neighbour not in best_known or new_dist < best_known[neighbour]):
                # ??? update best_known
                # ??? update parents
                # ??? push onto heap
    return None, parents


def main():

    heapq_test()


if __name__ == "__main__":
    main()
