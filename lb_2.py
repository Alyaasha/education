# класс для работы со Stack
class Stack:
    # инициализация
    def __init__(self):
        self.items = []
    # проверка на пустоту
    def isEmpty(self):
        return self.items == []
    # добавить элемент
    def push(self, item):
        self.items.append(item)
    # удалить элемент
    def pop(self):
        return self.items.pop() if self.items else None
    # развернуть
    def reverse(self):
        self.items.reverse()

# класс для работы с Deque
class Deque:
    # инициализация
    def __init__(self):
        self.items = []
    # проверка на пустоту
    def isEmpty(self):
        return self.items == []
    # добавить вправо
    def append(self, item):
        self.items.append(item)
    # добавить влево
    def appendleft(self, item):
        self.items.insert(0, item)
    # удалить справа, исключаем ошибку, если дек окажется пустым
    def pop(self):
        return self.items.pop() if self.items else None
     # удалить слева, исключаем ошибку, если дек окажется пустым
    def popleft(self):
        return self.items.pop(0) if self.items else None
    # вернуть элемент без удаления, исключаем ошибку, если дек окажется пустым
    def peek(self):
        return self.items[-1] if self.items else None
     # развернуть
    def reverse(self):
        self.items.reverse()
    # получить длину
    def __len__(self):
        return len(self.items)


# Функция для чтения текста из файла
def read_file(filename):
    with open(filename, 'r', encoding = "utf-8") as file:
        return [row.strip() for row in file]

# Функция для загрузки в файла
def save_to_file(filename, result):
    with open(filename, 'w', encoding = "utf-8") as f:
        if isinstance(result, str):
            f.write(result + "\n")
        else:
            for item in result:
                f.write(str(item) + "\n")

# task_1
# Отсортировать строки файла, содержащие названия книг, в алфавитном порядке с использованием двух деков.
def sort_books(input_file_path):
    # Создаем экземпляр класса для хранения книг
    deq = Deque()
    # Создаем экземпляр класса для отсортированных книг
    sort_deq = Deque()

    # Заполняем дек книгами из файла
    for book in read_file(input_file_path):
        deq.append(book.strip())

    # Сортируем книги в алфавитном порядке
    while not(deq.isEmpty()):
        element = deq.pop()  # Извлекаем элемент из неотсортированного дека
        while not (sort_deq.isEmpty()) and element < sort_deq.peek():
            deq.append(sort_deq.pop())  # Перемещаем элементы из отсортированного дека в неотсортированную, если необходимо
        sort_deq.append(element)

    # Записываем отсортированные книги в файл
    save_to_file("task_1_output.txt", sort_deq.items)

    # Выводим отсортированные книги
    print("Отсортированные названия книг:")
    while not sort_deq.isEmpty():
        print(sort_deq.popleft())  # Печатаем отсортированные книги и удаляем их из отсортированной деки


# task_2
# функция для расшифровки текста
def decode_text(input_file_path):
  deq = Deque()
  [deq.append(letter) for letter in 'abcdefghijklmnoprstuvwxyz']
  decrypted_text = ""
  decode = read_file(input_file_path)
  # функция для расшифровки каждого символа
  def decryptText(variable):
    for letter in range(len(deq)):
      symbol = deq.popleft()
      # если наш извлеченный символ из дека == сравниваемому из текста
      if symbol == variable:
        # добавляем наш извлеченный символ из дека в конец дека
        deq.append(symbol)
        # извлечем след. символ после symbol
        next_symbol = deq.popleft()
        # посместим его в конец списка
        deq.append(next_symbol)
        # вернем последний извлченный символ для добавления в decrypted_text
        return next_symbol
      deq.append(symbol)

  for string in decode:
    for symbol in string.lower():
      decode_symbol = decryptText(symbol)
      # проверяет, произошло ли шифрование
      if decode_symbol:
          decrypted_text += decode_symbol
      else:
          decrypted_text += symbol

    # Записываем расшифрованный текст в файл
    save_to_file("task_2_output.txt", decrypted_text)
    print(f"Расшифрованный текст: {decrypted_text}")


# task_3
def hanoi_tower(input_file_path):
    # Создаем три стека для представления стержней A, B и C
    A = Stack()
    B = Stack()
    C = Stack()

    # Считываем число дисков из файла
    n = int(read_file(input_file_path)[0])

    # Инициализируем стержень A дисками от n до 1 в порядке убывания
    [A.push(disk) for disk in range(n, 0, -1)]

    # Назначаем имена стержням
    A.name, C.name, B.name = "A", "C", "B"

    # Выводим начальное состояние стержня A
    print(f'Состояние стержня A: {A.items}')

    # Внутренняя рекурсивная функция для перемещения дисков
    def move_disks(n, start, end, middle):
        if n == 1:
            # Если есть только один диск, перемещаем его сразу на нужный стержень
            end.push(start.pop())
            print(f'Перемещаем диск 1 со стержня {start.name} на стержень {end.name}')
            return
        else:
            # Рекурсивно перемещаем n-1 дисков с начального стержня на вспомогательный
            move_disks(n - 1, start, middle, end)

            # После этого перемещаем самый большой диск на конечный стержень
            print(f'Перемещаем диск со стержня {start.name} на стержень {end.name}')
            end.push(start.pop())

            # Затем рекурсивно перемещаем n-1 дисков с вспомогательного стержня на конечный
            move_disks(n - 1, middle, end, start)

    # Вызываем рекурсивную функцию для перемещения всех дисков с A на C
    move_disks(n, A, C, B)

    # Разворачиваем стержень C, так как верхний диск находится внизу
    C.reverse()

    # Сохраняем конечное состояние стержня C в файл
    save_to_file("task_3_output.txt", C.items)

    # Выводим конечное состояние стержня C на экран
    print(f'Состояние стержня C: {C.items}')

    # Функция завершается
    return


# task_4
def balance_round_brackets(input_file_path):
    # Функция для чтения текста из файла
    def read_file(filename):
        with open(filename, 'r', encoding="utf-8") as file:
            return [row.strip() for row in file]

    balance = Stack()  # Создаем экземпляр класса Stack
    text = read_file(input_file_path)  # Читаем файл с текстом
    test = [symbol for row in text for symbol in row]  # Считываем символы из файла
    for symbol in test:
        if symbol == "(":  # Если символ - открывающая скобка
            balance.push(symbol)  # Помещаем ее в стек
        elif symbol == ")":  # Если символ - закрывающая скобка
            if balance.isEmpty():  # Если стек пуст
                print("Не сохраняется баланс скобок")
                save_to_file("task_4_output.txt", str(balance.isEmpty())) # Выводим сообщение о несбалансированности
                return False
            balance.pop()  # Удаляем соответствующую открывающую скобку из стека

    # Вызываем функцию сохранения в файл
    save_to_file("task_4_output.txt", str(balance.isEmpty()))
    # Выводим сообщение о сохранении баланса скобок
    print("Сохраняется баланс скобок")
    # Возвращаем True/False
    return balance.isEmpty()

# task_5
def balance_square_brackets(input_file_path):
    balance = Deque()  # Создаем экземпляр класса Deque
    text = read_file(input_file_path)  # Читаем файл с текстом
    test = [symbol for row in text for symbol in row]  # Считываем символы из файла
    for symbol in test:
        if symbol == "[":  # Если символ - открывающая скобка
            balance.append(symbol)  # Помещаем ее в дек
        elif symbol == "]":  # Если символ - закрывающая скобка
            if balance.isEmpty():  # Если дек пуст
                print("Не сохраняется баланс скобок")
                save_to_file("task_5_output.txt", "False")# Выводим сообщение о несбалансированности
                return False
            balance.pop()  # Удаляем соответствующую открывающую скобку из дека
    # Вызываем функцию сохранения в файл
    save_to_file("task_5_output.txt", str(balance.isEmpty()))
    # Выводим сообщение о сохранении баланса скобок
    print("Сохраняется баланс скобок")
    # Возвращаем True/False
    return balance.isEmpty()


# task_6
def sort_text(input_file_path):
    stack = Stack()
    new_doc = ""
    for word in read_file(input_file_path):
        for symbol in word:
            if symbol.isdigit():
                new_doc += symbol
            else:
                stack.push(symbol)
    for item in stack.items:
        if item.isalpha():
            new_doc += item
    for item in stack.items:
        if not item.isalpha():
            new_doc += item
    save_to_file("task_6_output.txt", new_doc)
    print(new_doc)

# task_7
def sort_digits(input_file_path):
    digits = []
    # Читаем строку из файла и разделяем её на отдельные числа
    for line in read_file(input_file_path):
        numbers = line.strip().split()
        # Преобразуем каждое число из строки в целое значение и добавляем в список digits
        digits.extend([int(number) for number in numbers])

    # Создаем дек для сортировки чисел
    deq = Deque()
    # Добавляем числа в дек
    for number in digits:
        # Если число положительное, добавляем вправо, если отрицательное - влево
        if number >= 0:
            deq.append(number)
        else:
            deq.appendleft(number)

    # Записываем результат в файл
    save_to_file("task_7_output.txt", deq.items)
    while not deq.isEmpty():
        print(deq.popleft())  # Выводим числа

# task_8
def reverse_strings(input_file_path):
    phrases = Stack()  # Создаем стек для хранения строк
    [phrases.push(string) for string in read_file(input_file_path)]  # Добавляем строки в стек
    phrases.reverse()  # Разворачиваем стек для получения строк в обратном порядке
    # Записываем строки в файл в обратном порядке
    save_to_file("task_8_output.txt", phrases.items)
    phrases.reverse()  # Возвращаем стек в исходный порядок
    # Выводим строки на экран
    while not phrases.isEmpty():
        print(phrases.pop())

# Вызываем функции
print("Задание №1")
sort_books("task_1.txt")  # Сортируем названия книг
print("Задание №2")
decode_text("task_2.txt")  # Расшифровываем текст
print("Задание №3")
hanoi_tower("task_3.txt")  # Переносим диски
print("Задание №4")
balance_round_brackets("task_4.txt")  # Проверяем баланс круглых скобок
print("Задание №5")
balance_square_brackets("task_5.txt")  # Проверяем баланс квадратных скобок
print("Задание №6")
sort_text("task_6.txt")  # Сортируем текст
print("Задание №7")
sort_digits("task_7.txt")  # Сортируем числа
print("Задание №8")
reverse_strings("task_8.txt")  # Выводим строки в обратном порядке