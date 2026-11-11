
import heapq
import time
import math


def haversine_distance(G, node1, node2):

    # Get geographical coordinates
    lat1 = math.radians(G.nodes[node1]["y"])
    lon1 = math.radians(G.nodes[node1]["x"])

    lat2 = math.radians(G.nodes[node2]["y"])
    lon2 = math.radians(G.nodes[node2]["x"])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    earth_radius = 6371000

    return earth_radius * c


def astar(G, source, destination):

    start_time = time.perf_counter()

    # Initial distances
    g_score = {
        node: float("inf")
        for node in G.nodes
    }

    g_score[source] = 0

    # Previous nodes for path reconstruction
    previous = {}

    # Priority queue: (f_score, g_score, node)
    priority_queue = [
        (
            haversine_distance(G, source, destination),
            0,
            source
        )
    ]

    explored_nodes = 0

    while priority_queue:

        f_score, current_distance, current_node = (
            heapq.heappop(priority_queue)
        )

        # Skip outdated entries
        if current_distance > g_score[current_node]:
            continue

        explored_nodes += 1

        # Destination reached
        if current_node == destination:
            break

        # Explore neighbors
        for neighbor, edges in G[current_node].items():

            # Find minimum parallel-edge distance
            edge_weight = min(
                data.get("length", float("inf"))
                for data in edges.values()
            )

            tentative_g = current_distance + edge_weight

            if tentative_g < g_score[neighbor]:

                g_score[neighbor] = tentative_g

                previous[neighbor] = current_node

                h_score = haversine_distance(
                    G,
                    neighbor,
                    destination
                )

                new_f_score = tentative_g + h_score

                heapq.heappush(
                    priority_queue,
                    (
                        new_f_score,
                        tentative_g,
                        neighbor
                    )
                )

    # Reconstruct path
    path = []

    if g_score[destination] != float("inf"):

        current = destination

        while current != source:
            path.append(current)
            current = previous[current]

        path.append(source)
        path.reverse()

    execution_time = time.perf_counter() - start_time

    return {
        "path": path,
        "distance": g_score[destination],
        "execution_time": execution_time,
        "explored_nodes": explored_nodes
    }
