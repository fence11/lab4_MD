import networkx as nx
import matplotlib.pyplot as plt


def create_adjacency_matrix(num_nodes, nodes_input):
    graph = [[0] * num_nodes for _ in range(num_nodes)]
    for i, connections_with_weights in enumerate(nodes_input):
        for conn, _ in connections_with_weights:
            conn_node = int(conn.strip()) - 1
            graph[i][conn_node] = 1
    return graph


def create_incidence_matrix(nodes_input):
    graph = []
    for i, connections_with_weights in enumerate(nodes_input):
        for conn, _ in connections_with_weights:
            conn_node = int(conn.strip()) - 1
            graph.append((i + 1, conn_node + 1))
    return graph


def create_incidence_list(num_nodes, nodes_input):
    graph = [[0] * num_nodes for _ in range(num_nodes)]
    for i, connections_with_weights in enumerate(nodes_input):
        for conn, _ in connections_with_weights:
            conn_node = int(conn.strip()) - 1
            graph[i][conn_node] = 1
    return graph


def print_adjacency_matrix(graph):
    print("   | ", end='')
    for i in range(len(graph)):
        print(f" x{i+1} |", end='')
    print()

    for i, row in enumerate(graph):
        print(f"x{i+1} | ", end='')
        for val in row:
            print(f" {val}  |", end='')
        print()


def print_incidence_matrix(graph, num_nodes):
    print("       | ", end='')
    for i in range(num_nodes):
        print(f" x{i+1} |", end='')
    print()

    for pair in graph:
        print(f"{pair} | ", end='')
        for i in range(1, num_nodes + 1):
            if i == pair[0] == pair[1]:
                print("  2 |", end='')
            elif i == pair[0]:
                print(" -1 |", end='')
            elif i == pair[1]:
                print("  1 |", end='')
            else:
                print("  0 |", end='')
        print()


def print_incidence_list(graph):
    for i, row in enumerate(graph):
        connections = []
        for x, val in enumerate(row):
            # print(f"{x} && {val}") # col_header - 1 && row value
            if val == 1:
                connections.append(str(x + 1))
        connections_str = ' '.join(connections)
        print(f"{i + 1} | {connections_str} 0")


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


def BellmanKalaba(num_nodes, nodes_input):
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


def print_bellman_kalaba(matrix):
    num_nodes = len(matrix[0]) - 1  # exclude v(0)

    # print default square matrix
    for i, row in enumerate(matrix):
        print(f"{i + 1:2} ", end="")
        formatted_row = [f" {elem:2}" if elem != '+' and elem !=
                         float('inf') else " + " for elem in row]
        print("[" + ",".join(formatted_row) + "]")

    # print rows V0, V1, V2 . . .
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


def menu(num_nodes, nodes_input):
    while True:
        menu_choice = int(input(
            "\n1 | Adjacency matrix\n2 | Incidence matrix\n3 | Incidence list\n4 | View graph\n5 | BK shortest path\n0 | EXIT\n"))
        match menu_choice:
            case 1:
                graph = create_adjacency_matrix(num_nodes, nodes_input)
                print("\nadjacency matrix:")
                print_adjacency_matrix(graph)
            case 2:
                graph = create_incidence_matrix(nodes_input)
                print("\nincidence matrix:")
                print_incidence_matrix(graph, num_nodes)
            case 3:
                graph = create_incidence_list(num_nodes, nodes_input)
                print("\nincidence list:")
                print_incidence_list(graph)
            case 4:
                graph = create_adjacency_matrix(num_nodes, nodes_input)
                visualize_graph(graph)
            case 5:
                result_matrix = BellmanKalaba(num_nodes, nodes_input)
                print("\nBellman-Kalaba matrix:")
                print_bellman_kalaba(result_matrix)
            case 0:
                print(
                    "\n======================\n||       Exit       ||\n======================\n")
                break
            case _:
                print("Invalid choice")


num_nodes = int(input("node num: "))
nodes_input = weighted_graph_connections(num_nodes)

menu(num_nodes, nodes_input)
