def encrypt_caesar(plaintext: str) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    n = 0
    ciphertext = ''
    while n < len(plaintext):
        a = ord(plaintext[n])
        if 88 <= a <= 90 or 120 <= a <= 122:
            a -= 23
        elif 65 <= a <= 87 or 97 <= a <= 119:
            a += 3
        n += 1
        ciphertext += chr(a)
    return ciphertext


def decrypt_caesar(ciphertext: str) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    n = 0
    plaintext = ''
    while n < len(ciphertext):
        a = ord(ciphertext[n])
        if 65 <= a <= 67 or 97 <= a <= 99:
            a += 23
        elif 68 <= a <= 90 or 100 <= a <= 122:
            a -= 3
        n += 1
        plaintext += chr(a)
    return plaintext
