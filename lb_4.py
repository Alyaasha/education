import random
import timeit
import matplotlib.pyplot as plt

def generate_random_data(size):
    return [random.randint(1, 10) for _ in range(size)]

# Функция бинарного поиска
# Поиск осуществляется с середины отсортированной последовательности,
# и далее происходит смещение по одну из частей последовательности
# Сложность O(log2(n)+1) - если находим элемент, что стоит в конце, O(1) -если элемент середины
def binarySearch(arr, x):
    end = len(arr) - 1
    start = 0
    while start < end:
        mid = (start + end) // 2
        if arr[mid] == x:
            return f"Индекс элемента {x} - {mid}"
        elif arr[mid] > x: # Случай, если элемент в первой половине последовательности
            end = mid - 1
        else: # arr[mid] <= x - элемент во второй половине последовательности
            start = mid + 1
    return f"Элемента {x} не найден"


# Функция Фиббоначи
# Совмещение бинарного поиска и чисел фибоначчи (F(m) = F(m-2) + F(m-1))
# Поиск начинается с конца
# и далее перемещение по последовательности происходит по шагам чисел фибоначчи
# Сложность O(1) - в случае, если элемент находится в первой итерации (arr[i] == x)
# Сложность O(log2(n))
def fibonacciSearch(arr, x):
    fb_m2 = 0  # Элемент F(m-2)
    fb_m1 = 1   # Элемент F(m-1)
    fb_m = fb_m2 + fb_m1  # Элемент F(m)
    start = -1
    while fb_m < len(arr):
        fb_m2 = fb_m1  # в начале элемент F(m-2) = 1
        fb_m1 = fb_m  # в начале элемент F(m-1) = 1
        fb_m = fb_m2 + fb_m1  # в начале F(m) = 2
    while fb_m > 1:
        i = min(start + fb_m, len(arr)-1)  # Поиск элемента в массиве - в начале i = 1
        if arr[i] == x:
            return f"Индекс элемента {x} - {i}"
        elif arr[i] < x: # перемещение в вторую половину последовательности
            start = i
            fb_m = fb_m1
            fb_m1 = fb_m2
            fb_m2 = fb_m - fb_m1
        else: # arr[i] > x - элемент во второй половине последовательности
            fb_m = fb_m2
            fb_m1 = fb_m1 - fb_m2
            fb_m2 = fb_m - fb_m1
    return f"Элемент {x} не найден"

# Функция интерполяционного поиска
# Поиск основан на принципе бинарного поиска
# В данном поиске помимо определения половины путем сравнения,
# также учитывается и расстояние до исходного элемента
# O(log2(log2 n)) для среднего случая и O(n) для наихудшего случая (числовые значения ключей увеличиваются экспоненциально)
def interpolationSearch(arr, x):
    start = 0
    end = len(arr) - 1
    while (arr[start] < x) and (arr[end] > x):
        if arr[end] == arr[start]:  #Защита от деления на 0
            break
        # Дифференцируемый шаг, зависящий от расстояния до исходного элемента
        mid = start + ((x - arr[start]) * (end - start)) // (arr[end] - arr[start])
        if arr[mid] < x:
            start = mid + 1
        elif arr[mid] > x:
            end = mid - 1
        else:
            return f"Индекс элемента {x} - {mid}"
    if arr[start] == x:
        return f"Индекс элемента {x} - {start}"
    if arr[end] == x:
        return f"Индекс элемента {x} - {end}"
    return f"Элемента {x} не найден"



# Функция бинарного дерева
# Расход памяти	- O(n)
# Поиск	- O(log n)
# Вставка - O(log n)
# Удаление - O(log n)
# Класс узла бинарного дерева
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        # Если дерево пустое, создаем корневой узел
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        # Если значение меньше текущего узла, идем в левое поддерево
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        # Если значение больше текущего узла, идем в правое поддерево
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)

    def search(self, value):
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        # Если узел не найден, возвращаем None
        if node is None:
            return None
        # Если значение равно текущему узлу, возвращаем узел
        if node.value == value:
            return node
        # Если значение меньше текущего узла, идем в левое поддерево
        elif value < node.value:
            return self._search_recursive(node.left, value)
        # Если значение больше текущего узла, идем в правое поддерево
        else:
            return self._search_recursive(node.right, value)

    def visualize(self):
        self._visualize_recursive(self.root, 0)

    def _visualize_recursive(self, node, level):
        if node is not None:
            self._visualize_recursive(node.right, level + 1)
            print('  ' * level + str(node.value))
            self._visualize_recursive(node.left, level + 1)

# # Создаем дерево и добавляем элементы
# tree = BinaryTree()
# tree.insert(5)
# tree.insert(8)
# tree.insert(9)
# tree.insert(3)
# tree.insert(2)
#
#
# # Визуализируем дерево
# tree.visualize()

# Ищем элемент в дереве
# result = tree.search(3)
# if result is not None:
#     print("Элемент найден:", result.value)
# else:
#     print("Элемент не найден")

# Функция простого рехеширования
'''
m = длина хеш-таблицы
n = общее количество ключей, которые будут вставлены в хеш-таблицу.
Коэффициент нагрузки lf = n/m
Ожидаемое время поиска = O(1 +lf)
Ожидаемое время вставки/удаления = O(1 + lf)
Временная сложность поиска, вставки и удаления равна
O(1), если lf равно O(1)
'''
class SimpleRehashing:
    def __init__(self, initial_size, load_factor=0.75):
        self.size = initial_size
        self.load_factor = load_factor
        self.threshold = int(initial_size * load_factor)
        self.bucket_array = [None] * initial_size
        self.count = 0

    def hash_function(self, key):
        return hash(key) % self.size

    def rehash_function(self):
        """
        Повторное хэширование - увеличение размера хэш-таблицы вдвое и перехэширование элементов.
        """
        new_size = self.size * 2
        new_threshold = int(new_size * self.load_factor)
        new_bucket_array = [None] * new_size

        # Перехэширование элементов
        for item in self.bucket_array:
            if item is not None:
                index = self.hash_function(item)
                while new_bucket_array[index] is not None:
                    index = (index + 1) % new_size
                new_bucket_array[index] = item

        # Обновление параметров
        self.size = new_size
        self.threshold = new_threshold
        self.bucket_array = new_bucket_array

    def insert(self, key):
        # Проверка необходимости повторного хэширования
        if self.count >= self.threshold:
            self.rehash_function()

        index = self.hash_function(key)
        while self.bucket_array[index] is not None:
            if self.bucket_array[index] == key:
                # Элемент уже существует в таблице
                return False
            index = (index + 1) % self.size
        self.bucket_array[index] = key
        self.count += 1
        return True

    def search(self, key):
        index = self.hash_function(key)
        while self.bucket_array[index] is not None:
            if self.bucket_array[index] == key:
                return True
            index = (index + 1) % self.size
        return False

    def visualize(self):
        print("Хэш-таблица:")
        for i, item in enumerate(self.bucket_array):
            print(f"{i}: {item}")

#     # Пример использования:
# hash_table = SimpleRehashing(10)
# # Добавляем элементы
# hash_table.insert(0)
# hash_table.insert(1)
# hash_table.insert(2)
#
# # Выводим текущую емкость (макс. кол0во элементов при степени загрузки таблицы = (3/4)) и размер хэш-таблицы
# print("Текущая емкость :", hash_table.threshold)
# print("Текущий размер:", hash_table.size)
#
# # Вставляем элементы до превышения порога коэффициента загрузки
# for i in range(8):
#     hash_table.insert(i+5)
#
# # Выводим текущую емкость и размер хэш-таблицы после добавления элементов
# print("Текущая емкость:", hash_table.threshold)
# print("Текущий размер:", hash_table.size)
# # Поиск элементов
# print(hash_table.search(5))  # True
# print(hash_table.search(15))  # False
#
# # Визуализируем хэш-таблицу
# hash_table.visualize()


# Функция рехэширования с помощью псевдослучайных чисел
class RandomRehashing:
    def __init__(self, initial_size, load_factor=0.75):
        self.size = initial_size
        self.load_factor = load_factor
        self.threshold = int(initial_size * load_factor)
        self.bucket_array = [None] * initial_size
        self.count = 0

    def hash_function(self, key):
        return hash(key) % self.size

    def random_number(self):
        return random.randint(1, self.size)

    def rehash_function(self):
        """
        Повторное хэширование с использованием псевдослучайных чисел - увеличение размера хэш-таблицы вдвое и перехэширование элементов.
        """
        new_size = self.size * 2
        new_threshold = int(new_size * self.load_factor)
        new_bucket_array = [None] * new_size

        # Перехэширование элементов
        for item in self.bucket_array:
            if item is not None:
                index = self.hash_function(item)
                while new_bucket_array[index] is not None:
                    index = (index + self.random_number()) % new_size
                new_bucket_array[index] = item

        # Обновление параметров
        self.size = new_size
        self.threshold = new_threshold
        self.bucket_array = new_bucket_array

    def insert(self, key):
        # Проверка необходимости повторного хэширования
        if self.count >= self.threshold:
            self.rehash_function()

        index = self.hash_function(key)
        while self.bucket_array[index] is not None:
            if self.bucket_array[index] == key:
                # Элемент уже существует в таблице
                return False
            index = (index + self.random_number()) % self.size
        self.bucket_array[index] = key
        self.count += 1
        return True

    def search(self, key):
        index = self.hash_function(key)
        while self.bucket_array[index] is not None:
            if self.bucket_array[index] == key:
                return True
            index = (index + self.random_number()) % self.size
        return False

    def visualize(self):

        print("Хэш-таблица:")
        for i, item in enumerate(self.bucket_array):
            print(f"{i}: {item}")

#     # Пример использования:
# hash_table = RandomRehashing(10)
# # Добавляем элементы
# hash_table.insert(0)
# hash_table.insert(1)
# hash_table.insert(2)
#
# # Выводим текущую емкость (макс. кол-во элементов при степени загрузки таблицы = (3/4)) и размер хэш-таблицы
# print("Текущая емкость :", hash_table.threshold)
# print("Текущий размер:", hash_table.size)
#
# # Вставляем элементы до превышения порога коэффициента загрузки
# for i in range(8):
#     hash_table.insert(i+5)
#
# # Выводим текущую емкость и размер хэш-таблицы после добавления элементов
# print("Текущая емкость:", hash_table.threshold)
# print("Текущий размер:", hash_table.size)
# # Поиск элементов
# print(hash_table.search(5))  # True
# print(hash_table.search(15))  # False
#
# # Визуализируем хэш-таблицу
# hash_table.visualize()

# Функция метода цепочек
class NodeHash:
    def __init__(self, value):
        self.key = hash(value)  # Ключ вычисляется на основе значения
        self.value = value
        self.next = None

class ChainingHashTable:
    def __init__(self, size):
        self.size = size
        self.bucket_array = [None] * size

    def hash_function(self, key):
        return key % self.size

    def insert(self, value):
        key = hash(value)
        index = self.hash_function(key)
        new_node = NodeHash(value)
        if self.bucket_array[index] is None:
            self.bucket_array[index] = new_node
        else:
            # Вставляем новый узел в начало связанного списка
            new_node.next = self.bucket_array[index]
            self.bucket_array[index] = new_node
        return True

    def search(self,  value):
        key = hash(value)
        index = self.hash_function(key)
        current = self.bucket_array[index]
        while current:
            if current.value == value:
                return True
            current = current.next
        return False

    def remove(self, value):
        key = hash(value)
        index = self.hash_function(key)
        current = self.bucket_array[index]
        prev = None
        while current:
            if current.value == value:
                if prev:
                    prev.next = current.next
                else:
                    self.bucket_array[index] = current.next
                return True
            prev = current
            current = current.next
        return False
    def visualize(self):
        print("Хэш-таблица:")
        for i, head in enumerate(self.bucket_array):
            print(f"{i}:", end=" ")
            current = head
            while current:
                print(f"({current.value})", end=" -> ")
                current = current.next
            print("None")

# # Пример использования:
# hash_table = ChainingHashTable(10)
#
# # Добавляем элементы
# hash_table.insert(1)
# hash_table.insert(11)
# hash_table.insert(22)
# hash_table.insert(33)
# hash_table.insert(44)
#
# # Пример коллизии и поиск элементов
# print(hash_table.search(1))  # True  # True
# print(hash_table.search(5))  # False
#
# # Удаляем элементы
# print(hash_table.remove(2))  # True
# print(hash_table.remove(5))  # False
#
# # Визуализируем хэш-таблицу
# hash_table.visualize()


# data = generate_random_data(1000)
# target_element = 5
# binary_tree = BinaryTree()
# simple_hash_table = SimpleRehashing(1000)
# random_hash_table = RandomRehashing(1000)
# chaining_hash_table = ChainingHashTable(1000)
# for element in data:
#     binary_tree.insert(element)
#     simple_hash_table.insert(element)
#     random_hash_table.insert(element)
#     chaining_hash_table.insert(element)

# binary_search_time = timeit.timeit(lambda: binarySearch(data, target_element), number=1000)
# fibonacci_search_time = timeit.timeit(lambda: fibonacciSearch(data, target_element), number=1000)
# interpolation_search_time = timeit.timeit(lambda: interpolationSearch(data, target_element), number=1000)
# binary_tree_search_time = timeit.timeit(lambda: binary_tree.search(random.choice(data)), number=1000)
# simple_hash_table_time = timeit.timeit(lambda: simple_hash_table.search(random.choice(data)), number=1000)
# random_hash_table_time = timeit.timeit(lambda: random_hash_table.search(random.choice(data)), number=1000)
# chaining_hash_table_time = timeit.timeit(lambda: chaining_hash_table.search(random.choice(data)), number=1000)
# standard_search_time = timeit.timeit(lambda: data.index(target_element), number=1000)
#
# print(f"Время выполнения бинарного поиска: {binary_search_time*1000:.2f} миллисекунд")
# print(f"Время выполнения поиска в бинарном дереве: {binary_tree_search_time*1000:.2f} миллисекунд")
# print(f"Время выполнения поиска Фиббоначи: {fibonacci_search_time*1000:.2f} миллисекунд")
# print(f"Время выполнения интерполяционного поиска: {interpolation_search_time*1000:.2f} миллисекунд")
# print(f"Время выполнения поиска в хэш таблице: {simple_hash_table_time*1000:.2f} миллисекунд")
# print(f"Время выполнения поиска в рандомизированной хэш таблице: {random_hash_table_time*1000:.2f} миллисекунд")
# print(f"Время выполнения поиска с помощью метода цепочек в хэш таблице: {chaining_hash_table_time*1000:.2f} миллисекунд")
# print(f"Время выполнения стандартной функции поиска: {standard_search_time*1000:.2f} миллисекунд")
