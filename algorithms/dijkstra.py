
import heapq
import time


def dijkstra(G, source, destination):

    # Start measuring execution time
    start_time = time.perf_counter()

    # Initialize distances
    distances = {node: float("inf") for node in G.nodes}

    # Store previous nodes for path reconstruction
    previous = {}

    # Source distance is zero
    distances[source] = 0

    # Priority queue: (distance, node)
    priority_queue = [(0, source)]

    # Track explored nodes
    explored_nodes = 0

    while priority_queue:

        current_distance, current_node = heapq.heappop(
            priority_queue
        )

        # Ignore outdated queue entries
        if current_distance > distances[current_node]:
            continue

        explored_nodes += 1

        # Destination reached
        if current_node == destination:
            break

        # Explore neighboring nodes
        for neighbor, edges in G[current_node].items():

            # Handle multiple road connections
            edge_weight = min(
                data.get("length", float("inf"))
                for data in edges.values()
            )

            new_distance = current_distance + edge_weight

            # Update if a shorter route is found
            if new_distance < distances[neighbor]:

                distances[neighbor] = new_distance

                previous[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    # Reconstruct shortest path
    path = []

    if distances[destination] != float("inf"):

        current = destination

        while current != source:
            path.append(current)
            current = previous[current]

        path.append(source)
        path.reverse()

    # Calculate execution time
    execution_time = time.perf_counter() - start_time

    return {
        "path": path,
        "distance": distances[destination],
        "execution_time": execution_time,
        "explored_nodes": explored_nodes
    }
