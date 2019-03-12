from typing import Dict, List, Any

adjList = {"a": ["c", "f"], "b": ["c"], "c": ["a", "b", "e"], "d": ["e", "f"], "e": ["c", "d"], "f": ["a", "d"]}


class DFS:

    def __init__(self, graph_adj_list: Dict[Any, List[Any]]):
        self.graph = graph_adj_list

    def iterative_visitation_order(self, start_node: Any = None, debug: bool = False) -> List[Any]:
        start_node = list(self.graph.keys())[0] if start_node is None or \
                                                   start_node not in self.graph.keys() else start_node
        stack = [start_node]
        visited = []

        if debug:
            print("Depth first traversal of graph starting from vertex {}".format(start_node))
            print("Stack initialised as {}".format(stack))
            print("Visited initialised as empty array {}".format(visited))

        while stack:
            vertex = stack.pop()
            if debug:
                print("\n---\n\nPop {} from the stack, leaving {}".format(vertex, stack))

            if vertex in visited:
                if debug:
                    print("Vertex {} already in visited, so skip to next in stack".format(vertex))
                continue

            visited.append(vertex)
            if debug:
                print("Add vertex {} to visited, resulting in {}".format(vertex, visited))

            for neighbour in sorted(self.graph[vertex], reverse=True):
                stack.append(neighbour)
            if debug:
                print("Push all neighbours of vertex {} to stack in reverse order, resulting in {}".format(
                    vertex, stack))

        if debug:
            print("\n---\n\nStack is now empty, so return the final visited array")
        return visited


print(DFS(adjList).iterative_visitation_order("b", True))
