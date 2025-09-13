# Johnson's Shortest Path Finder

This project implements Johnson's shortest path algorithm to compute the shortest distances between rooms based on a structured JSON floor plan. The main components of the project include:

## Project Structure

```
johnson-pathfinder
├── src
│   ├── johnson_pathfinder.py       # Implements Johnson's algorithm for shortest paths
│   ├── graph_builder.py             # Constructs the graph from the JSON floor plan
│   └── utils
│       └── json_loader.py           # Utility functions for loading JSON files
├── data
│   └── example_floor_plan.json      # Example floor plan in JSON format
├── tests
│   ├── test_johnson_pathfinder.py   # Unit tests for the JohnsonPathfinder class
│   └── test_graph_builder.py         # Unit tests for the GraphBuilder class
├── requirements.txt                  # Project dependencies
└── README.md                         # Project documentation
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd johnson-pathfinder
pip install -r requirements.txt
```

## Usage

To use the `JohnsonPathfinder`, you need to load the floor plan from the JSON file and create an instance of the pathfinder. Here is a basic example:

```python
from src.graph_builder import GraphBuilder
from src.johnson_pathfinder import JohnsonPathfinder

# Load the graph from the JSON floor plan
graph_builder = GraphBuilder()
graph = graph_builder.build_graph('data/example_floor_plan.json')

# Create an instance of JohnsonPathfinder
pathfinder = JohnsonPathfinder(graph)

# Find the shortest path between two rooms
result = pathfinder.find_shortest_path('rm_f01_101', 'rm_f01_102')
print(result)
```

## Testing

To run the tests for the project, use the following command:

```bash
pytest tests/
```

This will execute all unit tests and provide feedback on the functionality of the implemented classes.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.