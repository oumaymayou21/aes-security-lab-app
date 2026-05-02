import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.exceptions import InvalidTag

BLOCK_SIZE = 128

def generate_key(size=32):
    return os.urandom(size)

def pad_data(data):
    padder = PKCS7(BLOCK_SIZE).padder()
    return padder.update(data) + padder.finalize()

def unpad_data(padded_data):
    unpadder = PKCS7(BLOCK_SIZE).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()

def encrypt(mode, key, plaintext, **kwargs):
    mode = mode.upper()

    if mode == "ECB":
        cipher = Cipher(algorithms.AES(key), modes.ECB())
        encryptor = cipher.encryptor()
        padded = pad_data(plaintext)
        ciphertext = encryptor.update(padded) + encryptor.finalize()
        return {"ciphertext": ciphertext}

    elif mode == "CBC":
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padded = pad_data(plaintext)
        ciphertext = encryptor.update(padded) + encryptor.finalize()
        return {"ciphertext": ciphertext, "iv": iv}

    elif mode == "CTR":
        nonce = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return {"ciphertext": ciphertext, "nonce": nonce}

    elif mode == "GCM":
        nonce = os.urandom(12)
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return {"ciphertext": ciphertext, "nonce": nonce, "tag": encryptor.tag}

def decrypt(mode, key, ciphertext, **kwargs):
    mode = mode.upper()

    if mode == "ECB":
        cipher = Cipher(algorithms.AES(key), modes.ECB())
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()
        return unpad_data(padded)

    elif mode == "CBC":
        iv = kwargs.get("iv")
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()
        return unpad_data(padded)

    elif mode == "CTR":
        nonce = kwargs.get("nonce")
        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()

    elif mode == "GCM":
        nonce = kwargs.get("nonce")
        tag = kwargs.get("tag")
        try:
            cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag))
            decryptor = cipher.decryptor()
            return decryptor.update(ciphertext) + decryptor.finalize()
        except InvalidTag:
            print("❌ Message modifié !")
            return None