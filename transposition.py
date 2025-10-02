# goit-pnc-hw-02/simple_transposition.py
import math
from colorama import Fore, Style, init
init(autoreset=True)

# Читання тексту з файлу який лежить поруч
with open("text.txt", "r", encoding="utf-8") as file:
    text = file.read().strip()


# Проста перестановка
def simple_transposition_encrypt(text, key):
    cols = len(key)
    rows = math.ceil(len(text) / cols)
    padded_text = text.ljust(rows * cols)
    matrix = [padded_text[i:i+cols] for i in range(0, len(padded_text), cols)]
    column_order = sorted(range(len(key)), key=lambda i: key[i])
    encrypted_text = ''.join(matrix[row][col]
                             for col in column_order for row in range(rows))
    return encrypted_text


def simple_transposition_decrypt(ciphertext, key):
    cols = len(key)
    rows = math.ceil(len(ciphertext) / cols)
    column_order = sorted(range(len(key)), key=lambda i: key[i])
    inverse_order = [column_order.index(i) for i in range(cols)]
    matrix = [''] * rows
    index = 0
    for col in column_order:
        for row in range(rows):
            matrix[row] += ciphertext[index]
            index += 1
    decrypted_text = ''.join(matrix[row][col]
                             for row in range(rows) for col in inverse_order)
    return decrypted_text


# Подвійна перестановка
def double_transposition_encrypt(text, key1, key2):
    first_pass = simple_transposition_encrypt(text, key1)
    second_pass = simple_transposition_encrypt(first_pass, key2)
    return second_pass


def double_transposition_decrypt(ciphertext, key1, key2):
    first_pass = simple_transposition_decrypt(ciphertext, key2)
    second_pass = simple_transposition_decrypt(first_pass, key1)
    return second_pass


# Ключі
key1 = "SECRET"
key2 = "CRYPTO"

# Шифрування
encrypted_simple = simple_transposition_encrypt(text, key1)
decrypted_simple = simple_transposition_decrypt(encrypted_simple, key1)

encrypted_double = double_transposition_encrypt(text, key1, key2)
decrypted_double = double_transposition_decrypt(encrypted_double, key1, key2)

# Вивід результатів
print(f"{Fore.LIGHTCYAN_EX}\nEncrypted (Simple Transposition):\n {Style.RESET_ALL}",
      encrypted_simple[:200])
print(f"{Fore.LIGHTGREEN_EX}\nDecrypted (Simple Transposition):\n{Style.RESET_ALL}",
      decrypted_simple[:200])

print(f"{Fore.LIGHTCYAN_EX}\nEncrypted (Double Transposition):\n {Style.RESET_ALL}",
      encrypted_double[:200])
print(f"{Fore.LIGHTGREEN_EX}\nDecrypted (Double Transposition):\n{Style.RESET_ALL}",
      decrypted_double[:200])
