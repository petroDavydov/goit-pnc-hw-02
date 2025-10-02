# goit-pnc-hw-02/table.py


from colorama import Fore, Style, init
init(autoreset=True)

# Читання тексту з файлу
with open("text.txt", "r", encoding="utf-8") as file:
    text = file.read().strip()


# Шифр Віженера
def extend_key(text, key):
    key = key.upper()
    extended_key = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            extended_key += key[key_index % len(key)]
            key_index += 1
        else:
            extended_key += char
    return extended_key


def vigenere_encrypt(text, key):
    text = text.upper()
    key = extend_key(text, key)
    cipher_text = []
    for i in range(len(text)):
        if text[i].isalpha():
            x = (ord(text[i]) + ord(key[i]) - 2 * ord('A')) % 26
            cipher_text.append(chr(x + ord('A')))
        else:
            cipher_text.append(text[i])
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
            original_text.append(cipher_text[i])
    return ''.join(original_text)


# Табличний шифр
def table_chipher(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # взяли за умову схожість букв J і I
    key = ''.join(sorted(set(key.upper()), key=lambda x: key.index(x)))
    square = key + ''.join(c for c in alphabet if c not in key)
    return [square[i:i+5] for i in range(0, 25, 5)]


def table_encrypt(text, key):
    square = table_chipher(key)
    coords = ""
    for char in text.upper():
        if char == 'J':
            char = 'I'
        for i, row in enumerate(square):
            if char in row:
                coords += str(i+1) + str(row.index(char)+1) + " "
                break
    return coords.strip()


def table_decrypt(coords, key):
    square = table_chipher(key)
    pairs = coords.split()
    return ''.join(square[int(p[0])-1][int(p[1])-1] for p in pairs)


# Ключі
key_vigenere = "CRYPTO"
key_table = "MATRIX"


# Шифрування та дешифрування
encrypted_table = table_encrypt(text, key_table)
decrypted_table = table_decrypt(encrypted_table, key_table)

print(f"{Fore.LIGHTRED_EX}\nEncrypted (Table):{Style.RESET_ALL}\n",
      encrypted_table[:200])
print(f"{Fore.LIGHTGREEN_EX}\nDecrypted (Table):{Style.RESET_ALL}\n",
      decrypted_table[:200])

# Комбіноване шифрування Віженер - Табличний
step1 = vigenere_encrypt(text, key_vigenere)
step2 = table_encrypt(step1.replace(
    "J", "I").replace(" ", "").upper(), key_vigenere)

print(
    f"{Fore.LIGHTCYAN_EX}\nFinal encrypted (Vigenere → Table):\n {Style.RESET_ALL}", step2[:200])
