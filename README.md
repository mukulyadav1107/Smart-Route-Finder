# Smart Route Finder Using Graph Algorithms

A Python-based route optimization application that compares **Dijkstra's Algorithm** and **A* Search Algorithm** to find the shortest path between two locations using real-world road networks.

## Project Overview

Smart Route Finder uses graph algorithms and OpenStreetMap road data to calculate and visualize optimal routes between locations. It also compares the performance of Dijkstra and A* based on execution time, explored nodes, and route distance.

## Features

- Real-world road network using OpenStreetMap
- Shortest-path calculation using Dijkstra's Algorithm
- Heuristic-based route search using A* Algorithm
- Interactive map visualization
- Algorithm performance comparison
- Execution time and explored-node analysis
- Route distance calculation
- CSV export of comparison results

## Technologies Used

- Python
- Streamlit
- NetworkX
- OSMnx
- Folium
- Streamlit-Folium
- Matplotlib
- Pandas

## Algorithms Implemented

### 1. Dijkstra's Algorithm
Finds the shortest path by exploring nodes based on the minimum accumulated distance.

### 2. A* Search Algorithm
Uses the accumulated path cost and a heuristic estimate to guide the search toward the destination.

## Project Structure

```text
Smart-Route-Finder/
├── algorithms/
│   ├── astar.py
│   └── dijkstra.py
├── utils/
│   └── graph_utils.py
├── app.py
├── requirements.txt
└── .gitignore
```

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/mukulyadav1107/Smart-Route-Finder.git
```

2. Navigate to the project directory:

```bash
cd Smart-Route-Finder
```

3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the environment on Windows:

```bash
venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Run the application:

```bash
streamlit run app.py
```

## Performance Comparison

The application compares both algorithms using:

- Average execution time
- Standard deviation
- Number of explored nodes
- Route distance
- Number of nodes in the selected route

## Team Members

- Mukul Yadav
- Rajat Sahu
- Lakshay Yadav
- Gaurav

## Subject

Design and Analysis of Algorithms (DAA) – Project Based Learning

---

**Project:** Smart Route Finder  
**Repository:** [GitHub](https://github.com/mukulyadav1107/Smart-Route-Finder)
