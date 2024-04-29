import matplotlib.pyplot as plt
class QueensPlacement:
    def __init__(self, board_size, num_queens):
        self.board_size = board_size
        self.num_queens = num_queens
        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.queens = []

    def place_queens(self):
        self.place_queen(0)

    def place_queen(self, row):
        # метод для размещения ферзя в заданной строке
        if row == self.num_queens:
            return True
        for col in range(self.board_size):
            # Проверяем каждую клетку в строке на безопасность размещения ферзя
            if self.is_safe(row, col):
                # Если клетка безопасна, размещаем ферзя на ней
                self.board[row][col] = 1
                self.queens.append((row, col))
                # размещаем следующего ферзя в следующей строке
                if self.place_queen(row + 1):
                    return True
                # Если следующее размещение не удалось, отменяем текущее размещение
                self.board[row][col] = 0
                self.queens.pop()
            # Если не удалось разместить ферзя в текущей строке, возвращаем False
        return False

    def is_safe(self, row, col):
        for i in range(row):
            # Проверяем вертикаль, левую и правую диагонали от текущей клетки
            if self.board[i][col] == 1:
                return False
            if col - (row - i) >= 0 and self.board[i][col - (row - i)] == 1:
                return False
            if col + (row - i) < self.board_size and self.board[i][col + (row - i)] == 1:
                return False

        return True

    def print_solution(self):
        for row in self.board:
            print(' '.join(map(str, row)))

        print("\nРасположение ферзей")
        for queen in self.queens:
            print(queen)

    def visualize_solution(self):
        # Рисует квадрат
        chessboard = plt.figure()
        ax = chessboard.add_subplot(111, aspect='equal')

        # Рисует черные и белые клетки в квадратном поле
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = 'white' if (row + col) % 2 == 0 else 'black'
                ax.add_patch(plt.Rectangle((col, row), 1, 1, color=color))
        # Рисует ферзей
        for queen in self.queens:
            ax.text(queen[1] + 0.5, queen[0] + 0.5, '♕', ha='center', va='center', fontsize=20, color='red')

        ax.set_xlim(0, self.board_size)
        ax.set_ylim(0, self.board_size)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.invert_yaxis()

        plt.show()

# Пример использования
board_size = 8  # Размер поля
num_queens = 8  # Количество ферзей


queens_placement = QueensPlacement(board_size, num_queens)
queens_placement.place_queens()
queens_placement.print_solution()
queens_placement.visualize_solution()
