import sys
import timeit
import string
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import heapq
from collections import defaultdict

matrix = [[0, 1, 1, 0, 1],
         [1, 0, 1, 0, 0],
         [1, 1, 0, 1, 1],
         [0, 0, 1, 0, 0],
         [1, 0, 1, 0, 0]]

def build_graph(adjacency_matrix):
    # Инициализация пустого словаря для представления графа
    graph = {}
    # Определение количества вершин в графе на основе размера матрицы смежности
    num_vertices = len(adjacency_matrix)
    # Задание латинского алфавита для обозначения вершин
    latin_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Создание списка букв для обозначения вершин графа
    letters = [c for c in latin_alphabet]
    # Добавление дополнительных комбинаций букв для больших графов
    for i in range(1, num_vertices // len(latin_alphabet) + 1):
        letters += [f"{c}{chr(i + ord('A'))}" for c in latin_alphabet]

    # Создание графа на основе матрицы смежности
    for i in range(num_vertices):
        # Добавление вершины в граф
        graph[letters[i]] = {}
        for j in range(num_vertices):
            # Добавление ребра между вершинами, если существует связь в матрице смежности
            if adjacency_matrix[i][j] != 0:
                graph[letters[i]][letters[j]] = adjacency_matrix[i][j]

    return graph

print(build_graph(matrix))
def dijkstra_with_adjacency_matrix(adjacency_matrix, start, end):
    # Построение графа на основе матрицы смежности
    graph = build_graph(adjacency_matrix)
    # Инициализация словаря для хранения расстояний от начальной вершины до остальных
    distances = {vertex: sys.maxsize for vertex in graph}
    # Установка расстояния до начальной вершины как 0
    distances[start] = 0
    # Создание множества для хранения непосещенных вершин
    unvisited = set(graph)

    # Пока есть непосещенные вершины
    while unvisited:
        # Выбор текущей вершины с наименьшим расстоянием
        current_vertex = min(unvisited, key=lambda vertex: distances[vertex])
        # Удаление текущей вершины из множества непосещенных
        unvisited.remove(current_vertex)

        # Перебор соседей текущей вершины
        for neighbor, weight in graph[current_vertex].items():
            # Проверка, является ли сосед непосещенной вершиной
            if neighbor in unvisited:
                # Вычисление нового расстояния до соседа через текущую вершину
                new_distance = distances[current_vertex] + weight
                # Обновление расстояния до соседа, если новое расстояние меньше текущего
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance

    # Возвращение расстояния до конечной вершины
    return distances[end]

print(dijkstra_with_adjacency_matrix(matrix, "A", "C"))
def dijkstra_with_binary_heap(adjacency_matrix, start, end):
    graph = build_graph(adjacency_matrix)
    distances = {vertex: sys.maxsize for vertex in graph}
    distances[start] = 0
    heap = [(0, start)]

    while heap:
        current_distance, current_vertex = heapq.heappop(heap)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(heap, (distance, neighbor))

    return distances[end]

class FibonacciHeapNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.marked = False
        self.parent = None
        self.child = None
        self.left = self
        self.right = self

class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.num_nodes = 0

    def insert(self, key):
        new_node = FibonacciHeapNode(key)
        if self.min_node:
            new_node.left = self.min_node
            new_node.right = self.min_node.right
            self.min_node.right = new_node
            new_node.right.left = new_node
            if key < self.min_node.key:
                self.min_node = new_node
        else:
            self.min_node = new_node
        self.num_nodes += 1
        return new_node

    def merge(self, other_heap):
        if not self.min_node:
            self.min_node = other_heap.min_node
        elif other_heap.min_node:
            self.min_node.right.left = other_heap.min_node.left
            other_heap.min_node.left.right = self.min_node.right
            self.min_node.right = other_heap.min_node
            other_heap.min_node.left = self.min_node
            if other_heap.min_node.key < self.min_node.key:
                self.min_node = other_heap.min_node
        self.num_nodes += other_heap.num_nodes

    def remove_min(self):
        if not self.min_node:
            return None
        min_node = self.min_node
        if min_node.child:
            children = [min_node.child]
            current = min_node.child.right
            while current != min_node.child:
                children.append(current)
                current = current.right
            for child in children:
                self.min_node.left.right = child
                child.left = self.min_node.left
                self.min_node.left = child
                child.right = self.min_node
                child.parent = None
        min_node.left.right = min_node.right
        min_node.right.left = min_node.left
        if min_node == min_node.right:
            self.min_node = None
        else:
            self.min_node = min_node.right
            self.consolidate()
        self.num_nodes -= 1
        return min_node

    def consolidate(self):
        root_list = [None] * self.num_nodes
        nodes = [self.min_node]
        current = self.min_node.right
        while current != self.min_node:
            nodes.append(current)
            current = current.right
        for node in nodes:
            degree = node.degree
            while root_list[degree]:
                other = root_list[degree]
                if node.key > other.key:
                    node, other = other, node
                self.link(other, node)
                root_list[degree] = None
                degree += 1
            root_list[degree] = node
        self.min_node = None
        for root in root_list:
            if root:
                if not self.min_node:
                    self.min_node = root
                else:
                    root.left.right = root.right
                    root.right.left = root.left
                    root.left = self.min_node
                    root.right = self.min_node.right
                    self.min_node.right = root
                    root.right.left = root
                    if root.key < self.min_node.key:
                        self.min_node = root

    def link(self, y, x):
        y.left.right = y.right
        y.right.left = y.left
        y.parent = x
        if not x.child:
            x.child = y
            y.right = y
            y.left = y
        else:
            y.left = x.child
            y.right = x.child.right
            x.child.right = y
            y.right.left = y
        x.degree += 1
        y.marked = False

def dijkstra_with_fibonacci_heap(adjacency_matrix, start, end):
    graph = build_graph(adjacency_matrix)
    distances = defaultdict(lambda: float('inf'))
    distances[start] = 0
    heap = FibonacciHeap()
    node_map = {}

    for vertex, distance in distances.items():
        node = heap.insert((distance, vertex))
        node_map[vertex] = node

    while heap.num_nodes > 0:
        min_node = heap.remove_min()
        current_vertex = min_node.key[1]
        current_distance = min_node.key[0]

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                node = node_map[neighbor]
                heap.remove_min()
                node.key = (distance, neighbor)
                heap.insert(node.key)

    return distances[end]

def generate_random_adjacency_matrix(num_vertices, num_edges):
    matrix = [[0] * num_vertices for _ in range(num_vertices)]
    edges = set()
    while len(edges) < num_edges:
        v1, v2 = random.sample(range(num_vertices), 2)
        if (v1, v2) not in edges and (v2, v1) not in edges:
            weight = random.randint(1, 10)
            matrix[v1][v2] = weight
            edges.add((v1, v2))
    return matrix

def measure_performance():
    vertices_range = range(10, 1010, 100)
    edges_range = range(10, 1010, 100)
    time_by_vertices_adjacency_matrix = []
    time_by_edges_adjacency_matrix = []
    time_by_vertices_binary_heap = []
    time_by_edges_binary_heap = []
    time_by_vertices_fibonacci_heap = []
    time_by_edges_fibonacci_heap = []

    # Замер времени в зависимости от количества узлов
    for num_vertices in vertices_range:
        matrix = generate_random_adjacency_matrix(num_vertices, num_vertices)
        start_time = timeit.default_timer()
        dijkstra_with_adjacency_matrix(matrix, 'A', 'J')
        dijkstra_with_binary_heap(matrix, 'A', 'J')
        # dijkstra_with_fibonacci_heap(matrix, 'A', 'D')
        time_by_vertices_adjacency_matrix.append((timeit.default_timer() - start_time) * 1000)
        time_by_vertices_binary_heap.append((timeit.default_timer() - start_time) * 1000)
        # time_by_vertices_fibonacci_heap.append((timeit.default_timer() - start_time) * 1000)

    # Замер времени в зависимости от количества рёбер
    for num_edges in edges_range:
        matrix = generate_random_adjacency_matrix(1000, num_edges)
        start_time = timeit.default_timer()
        dijkstra_with_adjacency_matrix(matrix, 'A', 'J')
        dijkstra_with_binary_heap(matrix, 'A', 'J')
        # dijkstra_with_adjacency_matrix(matrix, 'A', 'D')
        time_by_edges_adjacency_matrix.append((timeit.default_timer() - start_time) * 1000)
        time_by_edges_binary_heap.append((timeit.default_timer() - start_time) * 1000)
        # time_by_edges_fibonacci_heap.append((timeit.default_timer() - start_time) * 1000)

    # Создание таблицы с результатами
    df_vertices_adjacency_matrix = pd.DataFrame({'Количество узлов': list(vertices_range), 'Время (мс)': time_by_vertices_adjacency_matrix})
    df_edges_adjacency_matrix = pd.DataFrame({'Количество рёбер': list(edges_range), 'Время (мс)': time_by_edges_adjacency_matrix})
    df_vertices_binary_heap = pd.DataFrame(
        {'Количество узлов': list(vertices_range), 'Время (мс)': time_by_vertices_binary_heap})
    df_edges_binary_heap = pd.DataFrame({'Количество рёбер': list(edges_range), 'Время (мс)': time_by_edges_binary_heap})
    # df_vertices_fibonacci_heap = pd.DataFrame({'Количество узлов': list(vertices_range), 'Время (мс)': time_by_vertices_fibonacci_heap})
    # df_edges_fibonacci_heap = pd.DataFrame({'Количество рёбер': list(edges_range), 'Время (мс)': time_by_edges_fibonacci_heap})

    # Вывод таблиц
    print("Зависимость времени от количества узлов для обычной реализации алгоритма Дейкстры:")
    print(df_vertices_adjacency_matrix.to_string(index=False))
    print("\nЗависимость времени от количества рёбер для обычной реализации алгоритма Дейкстры:")
    print(df_edges_adjacency_matrix.to_string(index=False))
    # print("Зависимость времени от количества узлов для алгоритма Дейкстры с бинарной кучей:")
    # print(df_vertices_binary_heap.to_string(index=False))
    # print("\nЗависимость времени от количества рёбер для алгоритма Дейкстры с бинарной кучей:")
    # print(df_edges_binary_heap.to_string(index=False))
    # print("Зависимость времени от количества узлов для алгоритма Дейкстры с кучей Фиббоначи:")
    # print(df_vertices_fibonacci_heap.to_string(index=False))
    # print("\nЗависимость времени от количества рёбер алгоритма Дейкстры с кучей Фибблначи:")
    # print(df_edges_fibonacci_heap.to_string(index=False))

measure_performance()


#
# def generate_random_graph(num_vertices, num_edges):
#     adjacency_matrix = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]
#     edges = [(i, j) for i in range(num_vertices) for j in range(i+1, num_vertices)]
#     random.shuffle(edges)
#     for i in range(min(num_edges, len(edges))):
#         weight = random.randint(1, 10)
#         u, v = edges[i]
#         adjacency_matrix[u][v] = weight
#         adjacency_matrix[v][u] = weight
#     return adjacency_matrix
#
# def measure_time_adjacency_matrix(num_vertices, num_edges):
#     adjacency_matrix = generate_random_graph(num_vertices, num_edges)
#     start_time = timeit.default_timer()
#     dijkstra_with_adjacency_matrix(adjacency_matrix, "A", "D")
#     end_time = timeit.default_timer()
#     return end_time - start_time
#
# def measure_time_binary_heap(num_vertices, num_edges):
#     adjacency_matrix = generate_random_graph(num_vertices, num_edges)
#     start_time = timeit.default_timer()
#     dijkstra_with_binary_heap(adjacency_matrix, "A", "D")
#     end_time = timeit.default_timer()
#     return end_time - start_time
#
# def measure_time_fibonacci_heap(num_vertices, num_edges):
#     adjacency_matrix = generate_random_graph(num_vertices, num_edges)
#     start_time = timeit.default_timer()
#     dijkstra_with_fibonacci_heap(adjacency_matrix, "A", "D")
#     end_time = timeit.default_timer()
#     return end_time - start_time
# def plot_graph(x_values, y_values, x_label, y_label, title):
#     plt.figure(figsize=(10, 6))
#     plt.plot(x_values, y_values, marker='o')
#     plt.xlabel(x_label)
#     plt.ylabel(y_label)
#     plt.title(title)
#     plt.grid(True)
#     plt.savefig(title + '.png')
#
# def main():
#     vertices_range = range(10, 1010, 200)
#     edges_range = range(10, 1010, 200)
#     time_vs_vertices_adjacency_matrix = [measure_time_adjacency_matrix(num_vertices, 1000) for num_vertices in vertices_range]
#     time_vs_edges_adjacency_matrix = [measure_time_adjacency_matrix(1000, num_edges) for num_edges in edges_range]
#     plot_graph(vertices_range, time_vs_vertices_adjacency_matrix, 'Количество узлов', 'Время (секунды)', 'Зависимость времени от количества узлов')
#     plot_graph(edges_range, time_vs_edges_adjacency_matrix, 'Количество рёбер', 'Время (секунды)', 'Зависимость времени от количества рёбер')
#
#     time_vs_vertices_binary_heap = [measure_time_adjacency_matrix(num_vertices, 1000) for num_vertices in
#                                          vertices_range]
#     time_vs_edges_binary_heap = [measure_time_binary_heap(1000, num_edges) for num_edges in edges_range]
#     plot_graph(vertices_range, time_vs_vertices_binary_heap, 'Количество узлов', 'Время (секунды)',
#                'Зависимость времени от количества узлов')
#     plot_graph(edges_range, time_vs_edges_binary_heap, 'Количество рёбер', 'Время (секунды)',
#                'Зависимость времени от количества рёбер')
#
#     time_vs_vertices_fibonacci_heap = [measure_time_adjacency_matrix(num_vertices, 1000) for num_vertices in
#                                     vertices_range]
#     time_vs_edges_fibonacci_heap = [measure_time_binary_heap(1000, num_edges) for num_edges in edges_range]
#     plot_graph(vertices_range, time_vs_vertices_fibonacci_heap, 'Количество узлов', 'Время (секунды)',
#                'Зависимость времени от количества узлов')
#     plot_graph(edges_range, time_vs_edges_fibonacci_heap, 'Количество рёбер', 'Время (секунды)',
#                'Зависимость времени от количества рёбер')
#
# if __name__ == "__main__":
#     main()