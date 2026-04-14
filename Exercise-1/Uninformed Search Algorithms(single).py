from collections import deque

class Graph:
    def __init__(self):
        self.adjacency_List={}
        self.heuristic_dict ={}
        self.direct=False

    def create_Graph(self,dir):
        self.direct=dir
        n=int(input("\nEnter the number of nodes:"))
        e=int(input("\nEnter the number of edges:"))
        print("\nEnter the nodes (line by line):")
        for i in range(n):
            node=input().strip()
            self.add_Node(node)
        print("\nEnter the edges (u v cost):")
        for i in range(e):
            line = input().strip()
            parts = line.split()
            if len(parts) != 3:
                print("Invalid input")
                continue
            u, v, cost = parts[0], parts[1], float(parts[2])
            self.add_Edge(u, v, cost)
        print("\nCreated Graph")

    def add_Node(self,node):
        if  node not in self.adjacency_List:
            self.adjacency_List[node]=[]
            print(f"\nNode '{node}' added to the graph")
        else:
            print(f"\nError: Node '{node}' already exist")

    def add_Edge(self,u,v,cost):
        if u not in self.adjacency_List and v not in self.adjacency_List:
            print(f"\nError: Both node '{u}' and '{v}' does not exists")
            return
        elif u not in self.adjacency_List:
            print(f"\nError: Node '{u}' does not exist")
            return
        elif v not in self.adjacency_List:
            print(f"Error: Node '{v}' not exist")
            return
        for edge in self.adjacency_List[u]:
            if edge[0] == v:
                print(f"Error: Edge between '{u}' - '{v}' already exists")
                return
        self.adjacency_List[u].append((v, cost))
        if not self.direct:
            for edge in self.adjacency_List[v]:
                if edge[0] == u:
                    print(f"Error: Edge between '{v}' - '{u}' already exists (undirected)")
                    self.adjacency_List[u].pop()
                    return
            self.adjacency_List[v].append((u, cost))
        print(f"Edge '{u}' -> '{v}' (cost: {cost}) added")

    def delete_Node(self,node):
        if node not in self.adjacency_List:
            print(f"Error: Node '{node}' does not exist")
            return
        for adjacent_tuple in list(self.adjacency_List[node]):
            adjacent_Node = adjacent_tuple[0]
            self.delete_Edge(node, adjacent_Node)
        del self.adjacency_List[node]
        print(f"Node '{node}' deleted sucessfully")

    def delete_Edge(self,u,v):
        if u not in self.adjacency_List:
            print(f"Error: Node '{u}' does not exist")
            return
        elif v not in self.adjacency_List:
            print(f"Error: Node '{v}' does not exist")
            return
        edge_found=False
        for i in range(len(self.adjacency_List[u])):
            edg, c = self.adjacency_List[u][i]
            if edg == v:
                del self.adjacency_List[u][i]
                edge_found=True
                break
        if not edge_found:
            print(f"Error: Edge '{u}' -> '{v}' does not exist")
            return
        if not self.direct:
            edge_found=False
            for i in range(len(self.adjacency_List[v])):
                edg, c = self.adjacency_List[v][i]
                if edg == u:
                    del self.adjacency_List[v][i]
                    edge_found=True
                    break
            if not edge_found:
                print(f"Warning: Reverse edge '{v}' -> '{u}' not found (undirected graph inconsistency)")
                return
        print(f"Edge '{u}' - '{v}' removed successfully")

    def display_Graph(self):
        if not self.adjacency_List:
            print("Error: Graph is empty")
            return

        print("\nGraph Adjacency List (with costs):")
        print("-" * 40)
        for node in self.adjacency_List:
            if self.adjacency_List[node]:
                edges= ', '.join([f"{adjacent_node}({c})" for adjacent_node, c in self.adjacency_List[node]])
                print(f"{node} → [{edges}]")
            else:
                print(f"{node} → []")
        print("-" * 40)

    def display_Adjacency(self,node):
        if not  self.adjacency_List:
            print("Error: Grpah is empty")
            return
        print("-" * 40)
        if node in self.adjacency_List:
            if self.adjacency_List[node]:
                edges= ', '.join([f"{adjacent_node}({c})" for adjacent_node, c in self.adjacency_List[node]])
                print(f"{node} → [{edges}]")
            else:
                print(f"{node} → []")
        else:
            print(f"Error: Node {node} does not exist")
            return
    def bfs_LtoR(self, start, goal):
        if not self.adjacency_List:
            print("Error: Graph is empty")
            return None
        if start not in self.adjacency_List:
            print(f"Error: Node '{start}' does not exist")
            return None
        if goal not in self.adjacency_List:
            print(f"Error: Node '{goal}' does not exist")
            return None

        frontier = deque([(start, 0)])
        explored = set()
        parent = {start: None}
        i = 1

        print("\nBFS Traversal Table:")
        print("Iter No | Fringe                                             | Explored                                           | Current Cost        ")
        print("-" * 140)


        while frontier:
            fringe_list = [f"{n}({c})" for n,c in frontier]
            explored_list = list(explored)
            current, current_cost = frontier.popleft()
            iter_str = f"{i:6}  "
            fringe_str = f"{str(fringe_list):<50}"[:50]
            explored_str = f"{str(explored_list):<50}"[:50]
            cost_str = f"{current_cost:>15}"

            print(f"{iter_str}| {fringe_str} | {explored_str} | {cost_str}")

            if current in explored:
                i += 1
                continue
            explored.add(current)

            if current == goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent.get(current)
                print("-" * 140)
                return path[::-1], current_cost

            for edge in self.adjacency_List[current]:
                adjacent_Node, edge_cost = edge
                if adjacent_Node not in explored and adjacent_Node not in [n for n,c in frontier]:
                    new_cost = float(current_cost) + float(edge_cost)
                    frontier.append((adjacent_Node, new_cost))
                    parent[adjacent_Node] = current
            i += 1

        print("-" * 140)
        print("No path found")
        return None

    def bfs_RtoL(self, start, goal):
        if not self.adjacency_List:
            print("Error: Graph is empty")
            return None
        if start not in self.adjacency_List:
            print(f"Error: Node '{start}' does not exist")
            return None
        if goal not in self.adjacency_List:
            print(f"Error: Node '{goal}' does not exist")
            return None

        frontier = deque([(start, 0)])
        explored = set()
        parent = {start: None}
        i = 1

        print("\nBFS Traversal Table:")
        print("Iter No | Fringe                                             | Explored                                           | Current Cost        ")
        print("-" * 140)

        while frontier:
            fringe_list = [f"{n}({c})" for n,c in frontier]
            explored_list = list(explored)
            current, current_cost = frontier.popleft()
            iter_str = f"{i:6}  "
            fringe_str = f"{str(fringe_list):<50}"[:50]
            explored_str = f"{str(explored_list):<50}"[:50]
            cost_str = f"{current_cost:>15}"

            print(f"{iter_str}| {fringe_str} | {explored_str} | {cost_str}")

            if current in explored:
                i += 1
                continue
            explored.add(current)

            if current == goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent.get(current)
                print("-" * 140)
                return path[::-1], current_cost

            adjacent_Node_Rev = self.adjacency_List[current][::-1]
            for edge in adjacent_Node_Rev:
                adjacent_Node, edge_cost = edge
                if adjacent_Node not in explored and adjacent_Node not in [n for n,c in frontier]:
                    new_cost = float(current_cost) + float(edge_cost)
                    frontier.append((adjacent_Node, new_cost))
                    parent[adjacent_Node] = current
            i += 1

        print("-" * 140)
        print("No path found")
        return None

    def dfs_LtoR(self, start, goal):
        if not self.adjacency_List:
            print("Error: Graph is empty")
            return None
        if start not in self.adjacency_List:
            print(f"Error: Node '{start}' does not exist")
            return None
        if goal not in self.adjacency_List:
            print(f"Error: Node '{goal}' does not exist")
            return None

        stack = [(start, 0)]
        explored = set()
        parent = {start: None}
        i = 1

        print("\nDFS Traversal Table (with costs):")
        print("Iter No | Fringe                                             | Explored                                           | Current Cost        ")
        print("-" * 140)

        while stack:
            stack_list = [f"{n}({c})" for n,c in stack]
            explored_list = list(explored)
            current, current_cost = stack.pop()
            iter_str = f"{i:6}  "
            stack_str = f"{str(stack_list):<50}"[:50]
            explored_str = f"{str(explored_list):<50}"[:50]
            cost_str = f"{current_cost:>15}"
            print(f"{iter_str}| {stack_str} | {explored_str} | {cost_str}")

            if current in explored:
                i += 1
                continue
            explored.add(current)

            if current == goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent.get(current)
                print("-" * 140)
                return path[::-1], current_cost

            for edge in self.adjacency_List[current]:
                adjacent_Node, edge_cost = edge
                if adjacent_Node not in explored and adjacent_Node not in [n for n,c in stack]:
                    new_cost = float(current_cost) + float(edge_cost)
                    stack.append((adjacent_Node, new_cost))
                    parent[adjacent_Node] = current
            i += 1

        print("-" * 140)
        print("No path found")
        return None

    def dfs_RtoL(self, start, goal):
        if not self.adjacency_List:
            print("Error: Graph is empty")
            return None
        if start not in self.adjacency_List:
            print(f"Error: Node '{start}' does not exist")
            return None
        if goal not in self.adjacency_List:
            print(f"Error: Node '{goal}' does not exist")
            return None

        stack = [(start, 0)]
        explored = set()
        parent = {start: None}
        i = 1

        print("\nDFS Traversal Table (with costs):")
        print("Iter No | Fringe                                             | Explored                                           | Current Cost        ")
        print("-" * 140)

        while stack:
            stack_list = [f"{n}({c})" for n,c in stack]
            explored_list = list(explored)
            current, current_cost = stack.pop()
            iter_str = f"{i:6}  "
            stack_str = f"{str(stack_list):<50}"[:50]
            explored_str = f"{str(explored_list):<50}"[:50]
            cost_str = f"{current_cost:>15}"
            print(f"{iter_str}| {stack_str} | {explored_str} | {cost_str}")

            if current in explored:
                i += 1
                continue
            explored.add(current)

            if current == goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent.get(current)
                print("-" * 140)
                return path[::-1], current_cost
            adjacent_Node_Rev = self.adjacency_List[current][::-1]
            for edge in adjacent_Node_Rev:
                adjacent_Node, edge_cost = edge
                if adjacent_Node not in explored and adjacent_Node not in [n for n,c in stack]:
                    new_cost = float(current_cost) + float(edge_cost)
                    stack.append((adjacent_Node, new_cost))
                    parent[adjacent_Node] = current
            i += 1

        print("-" * 140)
        print("No path found")
        return None
    def ucs(self, start, goal):
        if not self.adjacency_List:
            print("Error: Graph is empty")
            return None
        if start not in self.adjacency_List:
            print(f"Error: Node '{start}' does not exist")
            return None
        if goal not in self.adjacency_List:
            print(f"Error: Node '{goal}' does not exist")
            return None

        frontier = [(start, 0)]
        explored = set()
        parent = {start: None}
        i = 1

        print("Iter No | Fringe                                             | Explored                                           | Current Cost        ")
        print("-" * 140)

        while frontier:
            fringe_list = [f"{n}({c})" for n,c in frontier]
            explored_list = list(explored)
            min_idx = 0
            for j in range(1, len(frontier)):
                if frontier[j][1] < frontier[min_idx][1]:
                    min_idx = j

            current, current_cost = frontier.pop(min_idx)
            iter_str = f"{i:6}   "
            fringe_str = f"{str(fringe_list):<50}"[:50]
            explored_str = f"{str(explored_list):<50}"[:50]
            cost_str = f"{current_cost:>15}"

            print(f"{iter_str}| {fringe_str} | {explored_str} | {cost_str}")

            if current in explored:
                i += 1
                continue
            explored.add(current)

            if current == goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = parent.get(current)
                print("-" * 140)
                return path[::-1], current_cost

            for edge in self.adjacency_List[current]:
                adjacent_Node, edge_cost = edge
                new_cost = float(current_cost) + float(edge_cost)

                if adjacent_Node not in explored:
                    for j in range(len(frontier)):
                        if frontier[j][0] == adjacent_Node:
                            if new_cost < frontier[j][1]:
                                frontier[j] = (adjacent_Node, new_cost)
                                parent[adjacent_Node] = current
                            break
                    else:
                        frontier.append((adjacent_Node, new_cost))
                        parent[adjacent_Node] = current
            i += 1

        print("-" * 140)
        print("No path found")
        return None


if __name__ =="__main__":
    gr=int(input("\nEnter directed(1) or undirected(0) graph:"))
    g=Graph()
    g.create_Graph(gr)

    print("\n1.Add Node  \n2.Add Edge  \n3.Delete Node  \n4.Delete Edge  \n5.Display Graph  \n6.Display Node Adjacency List")
    print("7.BFS(L-R)  \n8.BFS(R-L)  \n9.DFS(L-R)  \n10.DFS(R-L)  \n11.UCS  \n12.Exit")
    ch=0
    while(ch!=12):
        ch=int(input("Enter your choice:"))
        match ch:
            case 1:
                node=input("Ener the node to be added:").strip()
                g.add_Node(node)
            case 2:
                nodes=input("Enter the edge between the nodes to be added(u v c):").strip()
                u,v,c=nodes.split()
                g.add_Edge(u,v,c)
            case 3:
                node=input("Ener the node to be deleted:").strip()
                g.delete_Node(node)
            case 4:
                nodes=input("Enter the edge between the nodes to be added(u v):").strip()
                u,v=nodes.split()
                g.delete_Edge(u,v)
            case 5:
                g.display_Graph()
            case 6:
                node=input("Enter the node to view its adjacent nodes:").strip()
                g.display_Adjacency(node)
            case 7:
                src=input("Enter the source node:").strip()
                dest=input("Enter the goal node:").strip()
                result=g.bfs_LtoR(src,dest)
                if not result:
                    print("Goal not found")
                else:
                    path, cost = result
                    print(f"BFS L-R Path to {dest}: {' -> '.join(path)}, Total cost:{cost}")
            case 8:
                src=input("Enter the source node:").strip()
                dest=input("Enter the goal node:").strip()
                result=g.bfs_RtoL(src,dest)
                if not result:
                    print("Goal not found")
                else:
                    path, cost = result
                    print(f"BFS R-L Path to {dest}: {' -> '.join(path)}, Total cost:{cost}")
            case 9:
                src=input("Enter the source node:").strip()
                dest=input("Enter the goal node:").strip()
                result=g.dfs_LtoR(src,dest)
                if not result:
                    print("Goal not found")
                else:
                    path, cost = result
                    print(f"DFS L-R Path to {dest}: {' -> '.join(path)}, Total cost:{cost}")
            case 10:
                src=input("Enter the source node:").strip()
                dest=input("Enter the goal node:").strip()
                result=g.bfs_RtoL(src,dest)
                if not result:
                    print("Goal not found")
                else:
                    path, cost = result
                    print(f"DFS R-L Path to {dest}: {' -> '.join(path)}, Total cost:{cost}")
            case 11:
                src=input("Enter the source node:").strip()
                dest=input("Enter the goal node:").strip()
                result = g.ucs(src, dest)
                if not result:
                    print("Goal not found")
                else:
                    path, cost = result
                    print(f"UCS Path to {dest}: {' -> '.join(path)}, Total Cost: {cost}")
