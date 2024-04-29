from random import *
print('Добро пожаловать в числовую угадайку')
def is_valid(x, a, b):
    if x.isdigit():
        if a <= int(x) <= b: return True
        else: return False
    else:
        return False

def game():
    print('Укажите границы игры:')
    a, b = int(input()), int(input())
    n = randrange(a,b+1)
    cnt = 0
    while True:
        print('Введите число для игры: ')
        x = input()
        if (not(is_valid(x,a,b))):
            print(f'А может быть все-таки введем целое число от {a} до {b}?')
            x = int(input())
        else:
            x = int(x)
            if n > x:
                print('Ваше число меньше загаданного, попробуйте еще разок')
                cnt += 1
            elif n < x:
                print('Ваше число больше загаданного, попробуйте еще разок')
                cnt += 1
            elif n == x:
                print('Вы угадали, поздравляем!')
                break
    print('Ваше число попыток:', cnt)

    print('Хотите сыграть ещё ?')
    y = input()
    if y == 'да' or y == 'Да' or y == 'ДА':
        print(game())
    else:
        print('Спасибо, что играли в числовую угадайку. Еще увидимся...')


while True:
    game()
    break