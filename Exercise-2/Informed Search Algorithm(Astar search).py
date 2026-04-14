from ex1 import Graph as gph

def get_heuristics(goal):
    if not g.adjacency_List:
        print("Error: The graph is empty")
        return
    print("\n--- Enter Heuristic Costs (h(n)) ---")
    g.heuristic_dict[goal]=0
    for node in g.adjacency_List:
        if node!=goal:
            while True:
                try:
                    val = float(input(f"Enter heuristic cost for node '{node}': "))
                    g.heuristic_dict[node] = val
                    break
                except ValueError:
                    print("Invalid input. Please enter a numerical value.")
    print("Heuristics successfully stored.\n")


def a_star(start, goal):
    if not g.adjacency_List:
        print("Error: Graph is empty")
        return None
    if start not in g.adjacency_List:
        print(f"Error: Node '{start}' does not exist")
        return None
    if goal not in g.adjacency_List:
        print(f"Error: Node '{goal}' does not exist")
        return None
    get_heuristics(goal)

    frontier = [(start, g.heuristic_dict[start])]  
    explored = set()
    parent = {start: None}
    i = 1

    print("Iter No | Fringe                                                                | Explored                                                               |f(n)=g(n)+h(n)     ")
    print("-" * 180)

    while frontier:
        min_idx = 0
        fringe_list = [f"{n}({f})" for n,f in frontier]
        explored_list = list(explored)

        for j in range(1, len(frontier)):
            current_f = frontier[j][1]  
            min_f = frontier[min_idx][1]
            if current_f < min_f:
                min_idx = j

        current, current_f = frontier.pop(min_idx)
        current_h = g.heuristic_dict[current]
        current_g = current_f - current_h  

        iter_str = f"{i:6}   "
        fringe_str = f"{str(fringe_list):<70}"[:70]
        explored_str = f"{str(explored_list):<70}"[:70]
        f_str = f"{current_f:>15}"

        print(f"{iter_str}| {fringe_str} | {explored_str} | {f_str}")

        if current in explored:
            i += 1
            continue
        explored.add(current)

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent.get(current)
            print("-" * 180)
            return path[::-1], current_g  

        for edge in g.adjacency_List[current]:
            adjacent_Node, edge_cost = edge
            tentative_g = current_g + edge_cost
            next_h = g.heuristic_dict[adjacent_Node]
            new_f = tentative_g + next_h  

            if adjacent_Node not in explored:
                for j in range(len(frontier)):
                    if frontier[j][0] == adjacent_Node:
                        if new_f < frontier[j][1]:
                            frontier[j] = (adjacent_Node, new_f)
                            parent[adjacent_Node] = current
                        break
                else:
                    frontier.append((adjacent_Node, new_f))
                    parent[adjacent_Node] = current
        i += 1

    print("-" * 180)
    print("No path found")
    return None

if __name__ =="__main__":
    gr=int(input("\nEnter directed(1) or undirected(0) graph:"))
    g=gph()
    g.create_Graph(gr)
    src=input("Enter the source node:").strip()
    dest=input("Enter the goal node:").strip()
    result = a_star(src, dest)
    if not result:
        print("Goal not found")
    else:
        path, cost = result
        print(f"A_STAR Path to {dest}: {' -> '.join(path)}, Total Cost: {cost}")
