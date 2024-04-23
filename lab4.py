import networkx as nx
import matplotlib.pyplot as plt


def create_adjacency_matrix(num_nodes, nodes_input):
    graph = [[0] * num_nodes for _ in range(num_nodes)]
    for i, connections_with_weights in enumerate(nodes_input):
        for conn, _ in connections_with_weights:
            conn_node = int(conn.strip()) - 1
            graph[i][conn_node] = 1
    return graph


def weighted_graph_connections(num_nodes):
    nodes_input = []
    print("node paths:")
    for i in range(num_nodes):
        connections = input(f"node {i+1}: ").split(' ')
        weighted_connections = []
        for connection in connections:
            if connection == '0':
                weighted_connections.append((connection, '+'))
            else:
                weight = input(f"weight ({i+1}, {connection}): ")
                weighted_connections.append((connection, weight))
        nodes_input.append(weighted_connections)
    return nodes_input


def visualize_graph(graph):
    G = nx.Graph()
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j] != 0:
                G.add_edge(i + 1, j + 1)

    nx.draw(G, with_labels=True, node_color='skyblue',
            node_size=1500, font_size=10, font_weight='bold')
    plt.show()


def create_weighted_adjacency_matrix(num_nodes, nodes_input):
    graph = [[0] * num_nodes for _ in range(num_nodes)]
    for i, connections_with_weights in enumerate(nodes_input):
        for conn, weight in connections_with_weights:
            conn_node = int(conn.strip()) - 1
            graph[i][conn_node] = int(weight)
    return graph


def bellman_kalaba(num_nodes, nodes_input):
    matrix = [['+' for _ in range(num_nodes)] for _ in range(num_nodes)]
    for i, connections_with_weights in enumerate(nodes_input):
        for conn, weight in connections_with_weights:
            conn_node = int(conn.strip()) - 1
            matrix[i][conn_node] = weight
            if i == conn_node:
                matrix[i][conn_node] = '0'
    for i in range(num_nodes):
        matrix[i][i] = '0'
    return matrix


def calc_bellman_kalaba(matrix):
    num_nodes = len(matrix)

    v0_values = [int(row[-1]) if row[-1].isdigit() else float('inf')
                 for row in matrix]
    v_values = [v0_values]
    iteration = 1

    while True:
        v_prev = v_values[-1]
        v_curr = []

        for i in range(num_nodes):
            values_to_min = []
            for j in range(num_nodes):
                if matrix[i][j].isdigit() and v_prev[j] != float('inf') and matrix[i][j] != '0' and i != j:
                    values_to_min.append(int(matrix[i][j]) + v_prev[j])
            if values_to_min:
                min_val = min(values_to_min)
            else:
                min_val = v_prev[i]
            v_curr.append(min_val)

        if v_curr == v_prev:
            return v0_values, v_values, True

        v_values.append(v_curr)

        iteration += 1


def print_bellman_kalaba(matrix, nodes_input):
    num_nodes = len(matrix)  # Get the number of nodes from the matrix size

    # Print default square matrix
    for i, row in enumerate(matrix):
        print(f"{i + 1:2} ", end="")
        formatted_row = [f" {elem:2}" if elem != '+' and elem !=
                         float('inf') else " + " for elem in row]
        print("[" + ",".join(formatted_row) + "]")

    # Print rows V0, V1, V2 . . .
    iteration = 1
    equality_found = False
    while not equality_found:
        v0_values, v_values, equality_found = calc_bellman_kalaba(matrix)
        for v_iteration, v_formatted in enumerate(v_values):
            print(f"V{v_iteration} ", end="")
            v_formatted = [f" {str(value):2}" if value != '+' and value !=
                           float('inf') else " + " for value in v_formatted]
            print("[" + ",".join(v_formatted) + "]")
        iteration += 1
    print("Equality found. Proceeding...")

    # Find the shortest path using v_values
    current_index = 0
    searched_index = 1
    shortest_path = []
    for i in range(num_nodes):  # Loop through each node
        if matrix[current_index][searched_index].isdigit() and v_values[iteration-1][current_index] - int(matrix[current_index][searched_index]) == v_values[iteration-1][searched_index]:
            print(f"{v_values[iteration-1][current_index]} - {matrix[current_index][searched_index]} = {v_values[iteration-1][searched_index]}")
            shortest_path.append(current_index + 1)  # Append the current node to the shortest path
            if matrix[current_index][searched_index].isdigit() and v_values[iteration-1][current_index] - int(matrix[current_index][searched_index]) == 0:
                shortest_path.append(searched_index + 1)  # Append the searched node to the shortest path
                break
            current_index = searched_index  # Move to the searched node
            searched_index += 1  # Increment the searched index
        else:
            searched_index += 1

    print(f"Shortest path: {shortest_path}")

    # Print node coordinates and their corresponding weights
    print("\nNode coordinates - Weight pairs:")
    for i, connections_with_weights in enumerate(nodes_input):
        for conn, weight in connections_with_weights:
            print(f"Node {i+1} -> Node {conn}: Weight {weight}")


def ford_shortest_path(num_nodes, nodes_input, source_node):
    distances = [float('inf')] * num_nodes
    distances[source_node] = 0

    for _ in range(num_nodes - 1):
        for i, connections_with_weights in enumerate(nodes_input):
            for conn, weight in connections_with_weights:
                conn_node = int(conn.strip()) - 1
                if weight != '+' and weight.isdigit() and distances[i] != float('inf') and distances[i] + int(weight) < distances[conn_node]:
                    distances[conn_node] = distances[i] + int(weight)

    # Check for negative cycles
    for i, connections_with_weights in enumerate(nodes_input):
        for conn, weight in connections_with_weights:
            conn_node = int(conn.strip()) - 1
            if weight != '+' and weight.isdigit() and distances[i] != float('inf') and distances[i] + int(weight) < distances[conn_node]:
                print("Graph contains negative cycle")
                return None

    return distances


def find_shortest_path(distances, nodes_input, source_node, current_node):
    print("Starting find_shortest_path function")
    shortest_path = [current_node + 1]  # Initialize the shortest path with the current node
    
    print("Entering while loop")
    while current_node != source_node:
        found = False
        print(f"Current node: {current_node}")
        for i, connections_with_weights in enumerate(nodes_input):
            for conn, weight in connections_with_weights:
                conn_node = int(conn.strip()) - 1
                # Check if the weight is valid and if it contributes to the shortest path
                if weight != '+' and weight.isdigit() and distances[current_node] - int(weight) == distances[conn_node]:
                    shortest_path.append(conn_node + 1)  # Append the node to the shortest path
                    current_node = conn_node  # Move to the connected node
                    found = True
                    print(f"Found valid connection to node: {conn_node}")
                    break
            if found:
                break
        
        print("End of iteration")
        if not found:
            print("No valid connection found, breaking out of the loop")
            break
                
    print("Exiting while loop")
    
    shortest_path_with_start = [source_node + 1] + shortest_path[::-1]  # Add the start node at the beginning
    return shortest_path_with_start



def menu(num_nodes, nodes_input, source_node):
    while True:
        menu_choice = int(input(
            "\n1 | View graph\n2 | BK shortest path\n3 | Ford shortest path\n0 | EXIT\n"))
        match menu_choice:
            case 1:
                graph = create_adjacency_matrix(num_nodes, nodes_input)
                visualize_graph(graph)
            case 2:
                result_matrix = bellman_kalaba(num_nodes, nodes_input)
                print("\nBellman-Kalaba matrix:")
                print_bellman_kalaba(result_matrix, nodes_input)  # Pass nodes_input here
            case 3:
                distances = ford_shortest_path(
                    num_nodes, nodes_input, source_node)
                if distances:
                    for i, distance in enumerate(distances):
                        print(f"Shortest distance from node {source_node + 1} to node {i + 1}: {distance}")
                    target_node = int(input("Enter the target node: ")) - 1
                    shortest_path = find_shortest_path(
                        distances, nodes_input, source_node, target_node)
                    if shortest_path:
                        print("Shortest path:", shortest_path)
                    else:
                        print("No path exists from node", source_node + 1, "to node", target_node + 1)
            case 0:
                print(
                    "\n======================\n||       Exit       ||\n======================\n")
                break
            case _:
                print("Invalid choice")



num_nodes = int(input("node num: "))
nodes_input = weighted_graph_connections(num_nodes)
# source_node = int(input("Enter the source node: "))
source_node = 0
menu(num_nodes, nodes_input, source_node)
