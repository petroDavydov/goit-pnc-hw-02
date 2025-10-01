# goit-pnc-hw-02/vigenere.py
from collections import Counter
from collections import defaultdict


def extend_key(text, key):
    key = key.upper()
    work_text = ""
    key_index = 0

    for char in text:
        if char.isalpha():
            work_text += key[key_index % len(key)]
            key_index += 1
        else:
            work_text += char  # Зберігаємо пробіли та крапки

    return work_text


def vigenere_encrypt(text, key):
    text = text.upper()
    key = extend_key(text, key)
    cipher_text = []

    for i in range(len(text)):
        if text[i].isalpha():
            x = (ord(text[i]) + ord(key[i]) - 2 * ord('A')) % 26
            cipher_text.append(chr(x + ord('A')))
        else:
            cipher_text.append(text[i])  # залишаємо не шифруємо

    return ''.join(cipher_text)


def vigenere_decrypt(cipher_text, key):
    cipher_text = cipher_text.upper()
    key = extend_key(cipher_text, key)
    original_text = []

    for i in range(len(cipher_text)):
        if cipher_text[i].isalpha():
            x = (ord(cipher_text[i]) - ord(key[i]) + 26) % 26
            original_text.append(chr(x + ord('A')))
        else:
            original_text.append(cipher_text[i])  # Залишаємо, не дешифруємо

    return ''.join(original_text)


# Використання функцій Kasiki та Fridman для аналізу

# Kasiki
def kasiski_test(ciphertext):
    distances = defaultdict(list)
    for i in range(len(ciphertext) - 3):
        trigram = ciphertext[i:i+3]
        for j in range(i+3, len(ciphertext) - 3):
            if ciphertext[j:j+3] == trigram:
                distances[trigram].append(j - i)
    return distances


# Fridman
def friedman_test(ciphertext):
    only_letters = [c for c in ciphertext if c.isalpha()]
    number_total_letters = len(only_letters)
    letter_frequencies = Counter(only_letters)
    index_of_coincidence = sum(f * (f - 1) for f in letter_frequencies.values()) / (
        number_total_letters * (number_total_letters - 1)) if number_total_letters > 1 else 0
    estimated_key_length = (0.0265 * number_total_letters) / (
        (0.0385 * number_total_letters) - index_of_coincidence) if index_of_coincidence != 0 else 0
    return round(estimated_key_length)


# Читання з файлу text.txt
with open("text.txt", "r", encoding="utf-8") as file:
    text = file.read().strip()

key = "CRYPTOGRAPHY"

encrypted_text = vigenere_encrypt(text, key)
print("\n Зашифрований текст(vigenere_encrypt):\n", encrypted_text[:400])

decrypted_text = vigenere_decrypt(encrypted_text, key)
print("\n Розшифрований текст(vigenere_decrypt):\n", decrypted_text[:400])


# Приклад використання Kasiki:
ciphertext = vigenere_encrypt(text, "CRYPTOGRAPHY")
kasiki_test = kasiski_test(ciphertext)
print("\n Повторювані триграми та відстані(Kasiki):\n", kasiki_test)


# Приклад викристання Fridman:
fridman_test = friedman_test(ciphertext)
print("\n Оцінка довжини ключа(Fridman):\n", fridman_test)
