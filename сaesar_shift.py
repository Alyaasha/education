def trans(string_1, shift):
    string_2 = ''
    letters_0 = 'qwertyuiopasdfghjklzxcvbnm'
    letters_1 = 'QWERTYUIOPASDFGHJKLZXCVBNM'
    letters_0, letters_1  = sorted(letters_0), sorted(letters_1)
    up_alph = {}
    low_alph = {}

    for i in letters_0:
        low_alph[i] = ord(i) % 96

    for i in letters_1:
        up_alph[i] = ord(i) % 64
    def let(z,y):
        for j in z:
            if z[j] == y:
                return j

    for i in string_1:
        if i in up_alph:
            y = (up_alph[i] + shift) % 26
            if y == 0: y = 26
            string_2 = string_2 + let(up_alph,y)
        elif i in low_alph:
            y = (low_alph[i] + shift) % 26
            if y == 0: y = 26
            string_2 =  string_2 + let(low_alph,y)
        else:
            string_2 = string_2 + i
    return string_2


str_1 = input().split(' ')
result = ""
for i in str_1:
    cnt = 0
    for j in i:
        if j in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM':
            cnt += 1
    result = result + ' ' + trans(i, cnt)
print(result.strip())




'''''
string_1 = "Шсъцхр щмчжмщ йшм, нмтзж йшм лхшщзщг"
string_2 = ''
letters_0 = 'йцукенгшщзхъфывапролджэячсмитьбю'
letters_1 = 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
letters_0, letters_1  = sorted(letters_0), sorted(letters_1)
up_alph = {}
low_alph = {}
shift = 7

for i in letters_0:
    low_alph[i] = ord(i) % 1071

for i in letters_1:
    up_alph[i] = ord(i) % 1039
def let(z,y):
    for j in z:
        if z[j] == y:
            return j

for i in string_1:
    if i in up_alph:
        y = (up_alph[i] - shift) % 32
        if y == 0: y = 32
        string_2 = string_2 + let(up_alph,y)
    elif i in low_alph:
        y = (low_alph[i] - shift) % 32
        if y == 0: y = 32
        string_2 =  string_2 + let(low_alph,y)
    else:
        string_2 = string_2 + i
print(string_2)

'''''