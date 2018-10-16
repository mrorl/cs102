def encrypt_vigenere(plaintext: str, keyword: str) -> str :
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    n = len(keyword)
    m = 0
    ciphertext = ''
    if len(keyword) < len(plaintext):
        a = len(plaintext) - len(keyword)
        for i in range(len(keyword), len(plaintext)):
            keyword += keyword[i - n]
    while m < len(plaintext):
        a = ord(plaintext[m])
        b = ord(keyword[m])
        if 97 <= a <= 122:
            k = a + (b - 97)
            if k > 122:
                t = k - 123
                k = 97 + t

        elif 65 <= a <= 90:
            k = a + (b - 65)
            if k > 90:
                t = k - 91
                k = 65 + t
        m += 1
        ciphertext += chr(k)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str :
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    n = len(keyword)
    m = 0
    plaintext = ''
    if len(keyword) < len(ciphertext):
        a = len(ciphertext) - len(keyword)
        for i in range(len(keyword), len(ciphertext)):
            keyword += keyword[i - n]
    while m < len(ciphertext):
        a = ord(ciphertext[m])
        b = ord(keyword[m])
        if 97 <= a <= 122:
            k = a - (b - 97)
            if k < 97:
                t = 96 - k
                k = 122 - t

        elif 65 <= a <= 90:
            k = a - (b - 65)
            if k < 65:
                t = 64 - k
                k = 90 - t
        m += 1
        plaintext += chr(k)
    return plaintext
