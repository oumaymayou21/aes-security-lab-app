import sys
from colorama import init, Fore, Style
from aes_modes import generate_key, encrypt, decrypt
from Attacks.attack_ecb import run_ecb_demo
from Attacks.attack_bit_flipping import run_bit_flipping_demo
from Attacks.attack_gcm_nonce import run_gcm_nonce_demo

init(autoreset=True)


def print_header(title):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*40}")
    print(f"{Fore.CYAN}{Style.BRIGHT}  {title}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'='*40}")


# 🔹 TEST SIMPLE
def demo():
    print_header("TEST COMPLET AES")
    message = input(f"{Fore.YELLOW}Entrez un message à chiffrer : ").encode()
    key = generate_key()

    for mode in ["ECB", "CBC", "CTR", "GCM"]:
        print(f"\n{Fore.MAGENTA}>>> Mode: {mode}")
        result = encrypt(mode, key, message)
        print(f"{Fore.WHITE}Ciphertext (hex): {result['ciphertext'].hex()[:50]}...")

        decrypted = decrypt(
            mode,
            key,
            result["ciphertext"],
            iv=result.get("iv"),
            nonce=result.get("nonce"),
            tag=result.get("tag"),
        )

        if decrypted:
            print(f"{Fore.GREEN}SUCCESS: Déchiffré -> {decrypted.decode(errors='ignore')}")
        else:
            print(f"{Fore.RED}ERROR: Échec du déchiffrement")


# 🔐 CHIFFRER UN FICHIER
def encrypt_file():
    print_header("CHIFFREMENT DE FICHIER")

    filename = input("Chemin du fichier (ex: files/message.txt) : ")
    mode = input("Mode (ECB, CBC, CTR, GCM) : ").upper()

    try:
        with open(filename, "rb") as f:
            data = f.read()
    except:
        print(f"{Fore.RED}Fichier introuvable ❌")
        return

    key = generate_key()
    result = encrypt(mode, key, data)

    with open("files/encrypted.bin", "wb") as f:
        f.write(result["ciphertext"])

    print(f"{Fore.GREEN}✔ Fichier chiffré : files/encrypted.bin")
    print("Clé :", key.hex())

    if "iv" in result:
        print("IV :", result["iv"].hex())
    if "nonce" in result:
        print("Nonce :", result["nonce"].hex())
    if "tag" in result:
        print("Tag :", result["tag"].hex())


# 🔓 DECHIFFRER UN FICHIER
def decrypt_file():
    print_header("DECHIFFREMENT DE FICHIER")

    mode = input("Mode (ECB, CBC, CTR, GCM) : ").upper()
    key = bytes.fromhex(input("Clé (hex) : "))

    iv = input("IV (hex si nécessaire) : ")
    nonce = input("Nonce (hex si nécessaire) : ")
    tag = input("Tag (hex si nécessaire) : ")

    kwargs = {}
    if iv:
        kwargs["iv"] = bytes.fromhex(iv)
    if nonce:
        kwargs["nonce"] = bytes.fromhex(nonce)
    if tag:
        kwargs["tag"] = bytes.fromhex(tag)

    try:
        with open("files/encrypted.bin", "rb") as f:
            ciphertext = f.read()
    except:
        print(f"{Fore.RED}Fichier chiffré introuvable ❌")
        return

    decrypted = decrypt(mode, key, ciphertext, **kwargs)

    if decrypted:
        with open("files/decrypted.txt", "wb") as f:
            f.write(decrypted)

        print(f"{Fore.GREEN}✔ Fichier déchiffré : files/decrypted.txt")
    else:
        print(f"{Fore.RED}Erreur de déchiffrement ❌")


# 🔥 MENU PRINCIPAL
def main():
    while True:
        print_header("AES SECURITY LAB - MENU")
        print(f"{Fore.YELLOW}1.{Fore.WHITE} Tester AES (Modes classiques)")
        print(f"{Fore.YELLOW}2.{Fore.WHITE} Lancer les attaques (Démos)")
        print(f"{Fore.YELLOW}3.{Fore.WHITE} Chiffrer un fichier")
        print(f"{Fore.YELLOW}4.{Fore.WHITE} Déchiffrer un fichier")
        print(f"{Fore.YELLOW}0.{Fore.WHITE} Quitter")

        choix = input(f"\n{Fore.CYAN}Sélectionnez une option : ")

        if choix == "1":
            demo()

        elif choix == "2":
            print_header("SIMULATION D'ATTAQUES")
            run_bit_flipping_demo()
            run_ecb_demo()
            run_gcm_nonce_demo()
            input(f"\n{Fore.YELLOW}Appuyez sur Entrée pour revenir au menu...")

        elif choix == "3":
            encrypt_file()

        elif choix == "4":
            decrypt_file()

        elif choix == "0":
            print(f"{Fore.GREEN}Au revoir !")
            sys.exit()

        else:
            print(f"{Fore.RED}Option invalide, réessayez.")


if __name__ == "__main__":
    main()