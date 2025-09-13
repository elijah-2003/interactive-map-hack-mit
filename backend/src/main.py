from johnson_pathfinder import JohnsonPathfinder
import graph_builder
from utils.json_loader import load_json

if __name__ == "__main__":
    # Load example data
    data = load_json("/Users/fabianruiz/git/interactive-map-hack-mit/backend/data/example_floor_plan.json")

    # Build graph
    graph_builder = graph_builder.GraphBuilder(data)
    graph = graph_builder.build_graph()

    # Run Johnson's pathfinder
    pathfinder = JohnsonPathfinder(graph)
    result = pathfinder.find_shortest_path("rm_f01_101", "jn_f01_t01")
    print(result)