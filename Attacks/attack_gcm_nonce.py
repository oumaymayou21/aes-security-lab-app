import os
from colorama import Fore, Style
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from aes_modes import generate_key

def run_gcm_nonce_demo():
    print(f"\n{Fore.CYAN}--- NONCE REUSE ATTACK (CTR/GCM) ---")
    key = generate_key()
    
    nonce = os.urandom(16) 

    msg1 = b"Ceci est un secret A"
    msg2 = b"Ceci est un secret B"

    cipher1 = Cipher(algorithms.AES(key), modes.CTR(nonce))
    ct1 = cipher1.encryptor().update(msg1) + cipher1.encryptor().finalize()

    cipher2 = Cipher(algorithms.AES(key), modes.CTR(nonce))
    ct2 = cipher2.encryptor().update(msg2) + cipher2.encryptor().finalize()

    xor_ciphertexts = bytes(a ^ b for a, b in zip(ct1, ct2))
    xor_plaintexts = bytes(a ^ b for a, b in zip(msg1, msg2))

    if xor_ciphertexts == xor_plaintexts:
        print(f"{Fore.RED}{Style.BRIGHT}RÉSULTAT : Fuite d'information détectée \u26a0\ufe0f")
        print(f"{Fore.YELLOW}Le XOR des chiffrés est égal au XOR des messages clairs.")
        print(f"L'attaquant peut maintenant déduire des informations sur les messages.")
    else:
        print(f"{Fore.GREEN}RÉSULTAT : Aucune fuite directe détectée.")