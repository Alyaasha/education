from random import *
yes = 'ДА Да да'
no = 'Нет нет НЕТ'
digits = '0123456789'
lowercase_letters = 'abcdefghijklmnopqrstuvwxyz'
uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
punctuation =  '!#$%&*+-=?@^_'
chars = ''


def gen(len_pw, dight, up_c, low_c, sym, mix_sym):
    chars = ''
    password = ''
    if dight in yes:
        chars = chars + dighits
    if up_c in yes:
        chars = chars + uppercase_letters
    if low_c in yes:
        chars = chars + lowercase_letters
    if sym in yes:
        chars = chars + punctuation
    if mix_sym in yes:
        while 'il1Lo0O' in chars:
            chars = chars.replace('il1Lo0O','', 1)
    while len_pw != len(password):
        password = password + choice(chars)
    return password

cnt_pw, len_pw, dight, up_c, low_c, sym, mix_sym = int(input('Количество паролей для генерации: ')), int(input('Длина одного пароля: ')), input('Включать ли цифры? '), input('Включать ли прописные буквы? '), input('Включать ли строчные буквы? '), input('Включать ли символы? '), input('Исключать ли неоднозначные символы (il1Lo0O) ? ')
for i in range(cnt_pw):
    print(gen(len_pw, dight, up_c, low_c, sym, mix_sym))