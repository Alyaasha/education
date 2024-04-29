import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit, \
    QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Класс приложения для работы с графами
class GraphApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    # Инициализация пользовательского интерфейса
    def initUI(self):
        self.setWindowTitle("Графическое приложение")
        self.setGeometry(100, 100, 800, 600)

        self.matrix_input_label = QLabel("Введите матрицу смежности:")
        self.matrix_input_textedit = QTextEdit()
        self.import_button = QPushButton("Импорт матрицы")
        self.import_button.clicked.connect(self.import_matrix)

        self.show_graph_button = QPushButton("Показать граф")
        self.show_graph_button.clicked.connect(self.show_graph)

        self.start_vertex_label = QLabel("Начальная вершина:")
        self.start_vertex_input = QLineEdit()

        self.end_vertex_label = QLabel("Конечная вершина:")
        self.end_vertex_input = QLineEdit()

        self.show_shortest_path_button = QPushButton("Показать кратчайший путь")
        self.show_shortest_path_button.clicked.connect(self.show_shortest_path)

        self.clear_button = QPushButton("Очистить поля")
        self.clear_button.clicked.connect(self.clear_fields)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.matrix_input_label)
        layout.addWidget(self.matrix_input_textedit)
        layout.addWidget(self.import_button)
        layout.addWidget(self.show_graph_button)
        layout.addWidget(self.canvas)
        layout.addWidget(self.start_vertex_label)
        layout.addWidget(self.start_vertex_input)
        layout.addWidget(self.end_vertex_label)
        layout.addWidget(self.end_vertex_input)
        layout.addWidget(self.show_shortest_path_button)
        layout.addWidget(self.clear_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # Импорт матрицы смежности из файла
    def import_matrix(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Импорт матрицы", "", "Текстовые файлы (*.txt)")
        if file_path:
            with open(file_path, "r") as file:
                matrix_text = file.read()
                self.matrix_input_textedit.setPlainText(matrix_text)

    # Показать граф в поле
    def show_graph(self):
        adjacency_matrix_str = self.matrix_input_textedit.toPlainText()
        adjacency_matrix = eval(adjacency_matrix_str)
        graph = build_graph(adjacency_matrix)
        self.clear_plot()
        self.draw_graph(graph)

    # Очистить поле
    def clear_plot(self):
        self.figure.clear()
        self.canvas.draw()

    # Нарисовать граф
    def draw_graph(self, graph):
        G = nx.DiGraph()
        for source, targets in graph.items():
            for target, weight in targets.items():
                G.add_edge(source, target, weight=weight)

        pos = nx.spring_layout(G, scale=2)
        edge_labels = nx.get_edge_attributes(G, 'weight')

        ax = self.figure.add_subplot(111)

        nx.draw(G, pos, ax=ax, with_labels=True, node_size=1500, node_color="skyblue", font_size=10, font_weight="bold",
                arrows=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

        self.canvas.draw()
        self.canvas.setMinimumSize(400, 400)

    # Показать кратчайший путь на графе
    def show_shortest_path(self):
        adjacency_matrix_str = self.matrix_input_textedit.toPlainText()
        adjacency_matrix = eval(adjacency_matrix_str)
        start_vertex = self.start_vertex_input.text().strip()
        end_vertex = self.end_vertex_input.text().strip()
        shortest_path, shortest_distance = dijkstra_with_adjacency_matrix(adjacency_matrix, start_vertex, end_vertex)

        graph = build_graph(adjacency_matrix)
        self.clear_plot()
        self.draw_shortest_path(graph, shortest_path)

    # Нарисовать кратчайший путь на графе
    def draw_shortest_path(self, graph, shortest_path):
        G = nx.DiGraph()
        for source, targets in graph.items():
            for target, weight in targets.items():
                G.add_edge(source, target, weight=weight)

        pos = nx.spring_layout(G, scale=2)
        edge_labels = nx.get_edge_attributes(G, 'weight')

        ax = self.figure.add_subplot(111)

        nx.draw(G, pos, ax=ax, with_labels=True, node_size=1500, node_color="skyblue", font_size=10, font_weight="bold",
                arrows=True)

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

        path_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2, ax=ax, arrows=True)

        self.canvas.draw()
        self.canvas.setMinimumSize(400, 400)

    # Очистить поля ввода
    def clear_fields(self):
        self.matrix_input_textedit.clear()
        self.start_vertex_input.clear()
        self.end_vertex_input.clear()
        self.clear_plot()


# Функция построения графа из матрицы смежности
def build_graph(adjacency_matrix):
    graph = {}
    num_vertices = len(adjacency_matrix)
    latin_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    letters = [c for c in latin_alphabet]
    for i in range(1, num_vertices // len(latin_alphabet) + 1):
        letters += [f"{c}{chr(i + ord('A'))}" for c in latin_alphabet]

    for i in range(num_vertices):
        graph[letters[i]] = {}
        for j in range(num_vertices):
            if adjacency_matrix[i][j] != 0:
                graph[letters[i]][letters[j]] = adjacency_matrix[i][j]

    return graph



# Функция алгоритма Дейкстры, использующая матрицу смежности
def dijkstra_with_adjacency_matrix(adjacency_matrix, start, end):
    graph = build_graph(adjacency_matrix)
    distances = {vertex: sys.maxsize for vertex in graph}
    distances[start] = 0
    unvisited = set(graph)

    while unvisited:
        current_vertex = min(unvisited, key=lambda vertex: distances[vertex])
        unvisited.remove(current_vertex)

        for neighbor, weight in graph[current_vertex].items():
            if neighbor in unvisited:
                new_distance = distances[current_vertex] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance

    shortest_path = [end]
    current_vertex = end
    while current_vertex != start:
        for neighbor, weight in graph[current_vertex].items():
            if distances[current_vertex] == distances[neighbor] + weight:
                shortest_path.append(neighbor)
                current_vertex = neighbor
                break

    return shortest_path[::-1], distances[end]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    graph_app = GraphApp()
    graph_app.show()
    sys.exit(app.exec())
