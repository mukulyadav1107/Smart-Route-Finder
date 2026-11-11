
import streamlit as st
import osmnx as ox
import folium
import pandas as pd
import statistics
import time

from streamlit_folium import st_folium

from utils.graph_utils import find_nearest_node
from algorithms.dijkstra import dijkstra
from algorithms.astar import astar


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Smart Route Finder",
    page_icon="📍",
    layout="wide"
)


# =====================================================
# CUSTOM PAGE HEADER
# =====================================================

st.title("📍 Smart Route Finder")

st.subheader(
    "Real-World Route Optimization Using Graph Algorithms"
)

st.write(
    "Find efficient routes between real-world locations "
    "and compare Dijkstra and A* search algorithms."
)

st.divider()


# =====================================================
# SESSION STATE
# =====================================================

if "road_graph" not in st.session_state:
    st.session_state.road_graph = None

if "route_result" not in st.session_state:
    st.session_state.route_result = None

if "comparison_results" not in st.session_state:
    st.session_state.comparison_results = None


# =====================================================
# LOAD REAL-WORLD ROAD NETWORK
# =====================================================

@st.cache_resource(show_spinner=False)
def load_road_network(location):

    latitude, longitude = ox.geocode(location)

    graph = ox.graph_from_point(
        center_point=(latitude, longitude),
        dist=2000,
        network_type="drive",
        simplify=True
    )

    return graph


# =====================================================
# SIDEBAR - MAP SETTINGS
# =====================================================

st.sidebar.title("🗺️ Map Settings")

place = st.sidebar.text_input(
    "Map Area",
    value="Connaught Place, New Delhi, India"
)

if st.sidebar.button(
    "Load Road Network",
    use_container_width=True
):

    try:

        with st.spinner("Downloading real-world road network..."):

            G = load_road_network(place.strip())

            st.session_state.road_graph = G
            st.session_state.route_result = None
            st.session_state.comparison_results = None

        st.sidebar.success("Road network loaded successfully!")

    except Exception as e:

        st.sidebar.error(f"Unable to load road network: {e}")


# =====================================================
# SIDEBAR - ROUTE SETTINGS
# =====================================================

st.sidebar.divider()

st.sidebar.header("Route Settings")

algorithm_choice = st.sidebar.selectbox(
    "Select Algorithm",
    ["Dijkstra", "A* Search"]
)

source_location = st.sidebar.text_input(
    "Starting Location",
    value="Connaught Place, New Delhi, India"
)

destination_location = st.sidebar.text_input(
    "Destination",
    value="Jantar Mantar, New Delhi, India"
)


# =====================================================
# FIND SHORTEST ROUTE
# =====================================================

if st.sidebar.button(
    "Find Shortest Route",
    use_container_width=True
):

    if st.session_state.road_graph is None:

        st.sidebar.error("Please load road network first.")

    else:

        try:

            with st.spinner("Calculating shortest route..."):

                G = st.session_state.road_graph

                source = find_nearest_node(
                    G, source_location
                )

                destination = find_nearest_node(
                    G, destination_location
                )

                if algorithm_choice == "Dijkstra":

                    result = dijkstra(
                        G, source, destination
                    )

                else:

                    result = astar(
                        G, source, destination
                    )

                st.session_state.route_result = {
                    "result": result,
                    "source": source,
                    "destination": destination,
                    "algorithm": algorithm_choice
                }

        except Exception as e:

            st.session_state.route_result = None

            st.sidebar.error(f"Route error: {e}")


# =====================================================
# COMPARE DIJKSTRA AND A*
# =====================================================

if st.sidebar.button(
    "⚖️ Compare Algorithms",
    use_container_width=True
):

    if st.session_state.road_graph is None:

        st.sidebar.error("Please load road network first.")

    else:

        try:

            G = st.session_state.road_graph

            with st.spinner(
                "Running five experiments for each algorithm..."
            ):

                source = find_nearest_node(
                    G, source_location
                )

                destination = find_nearest_node(
                    G, destination_location
                )

                dijkstra_runs = []
                astar_runs = []

                dijkstra_result = None
                astar_result = None

                # Five executions of each algorithm

                for i in range(5):

                    dijkstra_result = dijkstra(
                        G, source, destination
                    )

                    astar_result = astar(
                        G, source, destination
                    )

                    dijkstra_runs.append(
                        dijkstra_result["execution_time"]
                    )

                    astar_runs.append(
                        astar_result["execution_time"]
                    )

                # Check whether routes exist

                if not dijkstra_result["path"] or not astar_result["path"]:

                    raise ValueError(
                        "A route could not be found by both algorithms."
                    )

                # Calculate average execution times

                dijkstra_avg = statistics.mean(
                    dijkstra_runs
                )

                astar_avg = statistics.mean(
                    astar_runs
                )

                # Calculate standard deviation

                dijkstra_std = statistics.stdev(
                    dijkstra_runs
                )

                astar_std = statistics.stdev(
                    astar_runs
                )

                # Save comparison data

                st.session_state.comparison_results = {

                    "Dijkstra": {
                        "distance": dijkstra_result["distance"],
                        "time": dijkstra_avg,
                        "std": dijkstra_std,
                        "nodes": dijkstra_result["explored_nodes"],
                        "path_nodes": len(dijkstra_result["path"])
                    },

                    "A* Search": {
                        "distance": astar_result["distance"],
                        "time": astar_avg,
                        "std": astar_std,
                        "nodes": astar_result["explored_nodes"],
                        "path_nodes": len(astar_result["path"])
                    }
                }

                # Display A* route on the map after comparison

                st.session_state.route_result = {
                    "result": astar_result,
                    "source": source,
                    "destination": destination,
                    "algorithm": "A* Search"
                }

            st.sidebar.success("Comparison completed!")

        except Exception as e:

            st.session_state.comparison_results = None

            st.sidebar.error(
                f"Comparison error: {e}"
            )


# =====================================================
# MAIN APPLICATION - ROAD NETWORK
# =====================================================

G = st.session_state.road_graph

if G is None:

    st.info(
        "👈 Enter a map area in the sidebar and click "
        "'Load Road Network' to begin."
    )

else:

    # Convert graph to geographical data

    nodes, edges = ox.graph_to_gdfs(G)

    center_lat = nodes.geometry.y.mean()
    center_lon = nodes.geometry.x.mean()

    # Create map

    road_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=15,
        tiles="OpenStreetMap"
    )

    # Display complete road network

    folium.GeoJson(
        edges.to_json(),
        name="Road Network",
        style_function=lambda feature: {
            "color": "blue",
            "weight": 2
        }
    ).add_to(road_map)


    # =================================================
    # DISPLAY ROUTE
    # =================================================

    route_data = st.session_state.route_result

    if route_data is not None:

        result = route_data["result"]

        source = route_data["source"]
        destination = route_data["destination"]

        if result["path"]:

            # Convert route into geographical road segments

            route_edges = ox.routing.route_to_gdf(
                G,
                result["path"],
                weight="length"
            )

            # Highlight shortest route

            folium.GeoJson(
                route_edges.to_json(),
                name="Shortest Route",
                style_function=lambda feature: {
                    "color": "red",
                    "weight": 6,
                    "opacity": 0.9
                }
            ).add_to(road_map)

            # Starting location marker

            folium.Marker(
                location=[
                    G.nodes[source]["y"],
                    G.nodes[source]["x"]
                ],
                popup="Starting Location",
                tooltip="START",
                icon=folium.Icon(color="green")
            ).add_to(road_map)

            # Destination marker

            folium.Marker(
                location=[
                    G.nodes[destination]["y"],
                    G.nodes[destination]["x"]
                ],
                popup="Destination",
                tooltip="DESTINATION",
                icon=folium.Icon(color="red")
            ).add_to(road_map)

            # Route information

            st.success("Shortest route found!")

            st.info(
                f"Algorithm Used: {route_data['algorithm']}"
            )

            st.subheader("Route Information")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total Distance",
                f"{result['distance'] / 1000:.2f} km"
            )

            col2.metric(
                "Execution Time",
                f"{result['execution_time'] * 1000:.3f} ms"
            )

            col3.metric(
                "Nodes Explored",
                result["explored_nodes"]
            )

            st.write(
                f"**Total nodes in route:** {len(result['path'])}"
            )

        else:

            st.error("No route found.")


    # =================================================
    # DISPLAY MAP
    # =================================================

    st.divider()

    st.subheader("🌍 Real-World Road Map")

    folium.LayerControl().add_to(road_map)

    st_folium(
        road_map,
        height=600,
        use_container_width=True,
        returned_objects=[]
    )


    # =================================================
    # ROAD NETWORK INFORMATION
    # =================================================

    st.divider()

    st.subheader("Road Network Information")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Locations (Nodes)",
        G.number_of_nodes()
    )

    col2.metric(
        "Total Road Connections (Edges)",
        G.number_of_edges()
    )

    col3.metric(
        "Network Type",
        "Driving"
    )


# =====================================================
# ALGORITHM COMPARISON DASHBOARD
# =====================================================

if st.session_state.comparison_results is not None:

    results = st.session_state.comparison_results

    st.divider()

    st.header("⚖️ Algorithm Performance Comparison")

    st.write(
        "Experimental comparison of Dijkstra and A* "
        "using the same real-world road network."
    )

    st.caption(
        "Each algorithm was executed five times. "
        "Execution times are reported as averages."
    )

    # -------------------------------------------------
    # COMPARISON TABLE
    # -------------------------------------------------

    st.subheader("Performance Results")

    comparison_df = pd.DataFrame(
        results
    ).T

    comparison_df.index.name = "Algorithm"

    comparison_df = comparison_df.rename(
        columns={
            "distance": "Distance (metres)",
            "time": "Average Time (seconds)",
            "std": "Time Std. Dev. (seconds)",
            "nodes": "Nodes Explored",
            "path_nodes": "Route Nodes"
        }
    )

    st.dataframe(
        comparison_df.style.format({
            "Distance (metres)": "{:.2f}",
            "Average Time (seconds)": "{:.6f}",
            "Time Std. Dev. (seconds)": "{:.6f}",
            "Nodes Explored": "{:.0f}",
            "Route Nodes": "{:.0f}"
        }),
        use_container_width=True
    )

    # -------------------------------------------------
    # KEY PERFORMANCE METRICS
    # -------------------------------------------------

    st.subheader("Key Performance Metrics")

    col1, col2 = st.columns(2)

    col1.metric(
        "Dijkstra Average Time",
        f"{results['Dijkstra']['time'] * 1000:.3f} ms"
    )

    col2.metric(
        "A* Average Time",
        f"{results['A* Search']['time'] * 1000:.3f} ms"
    )

    # Percentage reduction in explored nodes

    dijkstra_nodes = results["Dijkstra"]["nodes"]
    astar_nodes = results["A* Search"]["nodes"]

    if dijkstra_nodes > 0:

        node_reduction = (
            (dijkstra_nodes - astar_nodes)
            / dijkstra_nodes
        ) * 100

        st.metric(
            "Reduction in Nodes Explored by A*",
            f"{node_reduction:.2f}%"
        )

    # -------------------------------------------------
    # NODES EXPLORED CHART
    # -------------------------------------------------

    st.divider()

    st.subheader("1. Nodes Explored Comparison")

    nodes_chart = pd.DataFrame({
        "Nodes Explored": [
            dijkstra_nodes,
            astar_nodes
        ]
    }, index=["Dijkstra", "A* Search"])

    st.bar_chart(nodes_chart)

    # -------------------------------------------------
    # EXECUTION TIME CHART
    # -------------------------------------------------

    st.subheader("2. Average Execution Time Comparison")

    time_chart = pd.DataFrame({
        "Execution Time (ms)": [
            results["Dijkstra"]["time"] * 1000,
            results["A* Search"]["time"] * 1000
        ]
    }, index=["Dijkstra", "A* Search"])

    st.bar_chart(time_chart)

    # -------------------------------------------------
    # DISTANCE CHART
    # -------------------------------------------------

    st.subheader("3. Route Distance Comparison")

    distance_chart = pd.DataFrame({
        "Distance (km)": [
            results["Dijkstra"]["distance"] / 1000,
            results["A* Search"]["distance"] / 1000
        ]
    }, index=["Dijkstra", "A* Search"])

    st.bar_chart(distance_chart)

    # -------------------------------------------------
    # EXPERIMENTAL OBSERVATIONS
    # -------------------------------------------------

    st.divider()

    st.subheader("Experimental Observations")

    st.write(
        f"""
        - Dijkstra explored **{dijkstra_nodes} nodes**.
        - A* explored **{astar_nodes} nodes**.
        - A* explored **{node_reduction:.2f}% fewer nodes**
          than Dijkstra.
        - Dijkstra average execution time:
          **{results['Dijkstra']['time'] * 1000:.3f} ms**.
        - A* average execution time:
          **{results['A* Search']['time'] * 1000:.3f} ms**.
        """
    )

    distance_difference = abs(
        results["Dijkstra"]["distance"]
        - results["A* Search"]["distance"]
    )

    if distance_difference < 0.01:

        st.success(
            "Both algorithms found routes with matching "
            "distances within 0.01 metres."
        )

    else:

        st.warning(
            "The route distances differ. Investigate the "
            "algorithm implementations and edge weights."
        )

    # -------------------------------------------------
    # DOWNLOAD COMPARISON DATA
    # -------------------------------------------------

    st.divider()

    st.subheader("Export Experimental Results")

    csv_data = comparison_df.to_csv().encode("utf-8")

    st.download_button(
        label="Download Comparison as CSV",
        data=csv_data,
        file_name="algorithm_comparison.csv",
        mime="text/csv"
    )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Smart Route Finder | DAA Project Based Learning | "
    "Dijkstra and A* Search Algorithms"
)
