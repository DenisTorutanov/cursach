
alpha = tuple("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.!?"
              "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя@ ")


def gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = gcd(b % a, a)
        return g, x - (b // a) * y, y


def extendGcd(a, b):
    g, x, y = gcd(a, b)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % b


# Генирация ключа
def generateKey(p, q):
    n = abs(p * q)
    fn = (p - 1) * (q - 1)
    e = 0
    for prime_number in [3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if fn % prime_number != 0:
            e = prime_number
            break
    x = extendGcd(e, fn)
    if x < 0:
        x = x + fn
    d = x
    return (e, n), (d, n)


publicKey, privateKey = generateKey(11, 13)


def encryption(text, Key, action):
    try:
        digit_text = []
        for char in text:
            digit = alpha.index(char) + 1
            digit = pow(digit, Key[0]) % Key[1]
            digit_text.append(str(digit))
        digit_text = '-'.join(digit_text)

        if action == "текст":
            with open('encrypted_text.txt', 'a', encoding='utf8') as text_file:
                text_file.write(digit_text + '\n')
                return True

        if action == "регистрация":
            with open('login.txt', 'r+', encoding='utf8') as text_file:
                for line in text_file:
                    if digit_text.rstrip().strip() == line.rstrip().strip():
                        return False
                text_file.write(digit_text + '\n')
                return True

        if action == "авторизация":
            with open('login.txt', 'r', encoding='utf8') as text_file:
                for line in text_file:
                    if digit_text.rstrip().strip() == line.rstrip().strip():
                        return True
                return False

    except Exception as e:
        print(e)
        return False


def decryption(digital_text, Key):
    try:
        digital_text = digital_text.split('-')
        text = []
        for digit in digital_text:
            char = pow(int(digit), Key[0]) % Key[1]
            text.append(alpha[char-1])
        return ''.join(text)
    except Exception as e:
        print(e)
        return False


def data_verification(username, password):
    if (' ' in password) or (len(password) < 8) or (len(username) < 3) \
            or (len(password) > 40) or (len(username) > 50):
        return False
    elif not encryption(username+password, publicKey, 'регистрация'):
        return False
    else:
        return True
