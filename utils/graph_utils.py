
import osmnx as ox


def find_nearest_node(G, location):

    # Convert location into latitude and longitude
    latitude, longitude = ox.geocode(location)

    # Find the nearest road-network node
    nearest_node = ox.distance.nearest_nodes(
        G,
        X=longitude,
        Y=latitude
    )

    return nearest_node


def get_road_distance(G, source, destination):

    # Get all edges between two nodes
    edges = G.get_edge_data(source, destination)

    if not edges:
        return None

    # Select the shortest available road connection
    distance = min(
        edge["length"]
        for edge in edges.values()
    )

    return distance
