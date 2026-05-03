# main.py
import sys
from colorama import init, Fore, Style
from aes_modes import generate_key, encrypt, decrypt
from Attacks.attack_ecb import run_ecb_demo
from Attacks.attack_bit_flipping import run_bit_flipping_demo
from Attacks.attack_gcm_nonce import run_gcm_nonce_demo

# Initialisation de colorama (nécessaire pour Windows)
init(autoreset=True)

def print_header(title):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*40}")
    print(f"{Fore.CYAN}{Style.BRIGHT}  {title}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'='*40}")

def demo():
    print_header("TEST COMPLET AES")
    message = input(f"{Fore.YELLOW}Entrez un message à chiffrer : ").encode()
    key = generate_key()

    for mode in ["ECB", "CBC", "CTR", "GCM"]:
        print(f"\n{Fore.MAGENTA}>>> Mode: {mode}")
        result = encrypt(mode, key, message)
        print(f"{Fore.WHITE}Ciphertext (hex): {result['ciphertext'].hex()[:50]}...")
        
        decrypted = decrypt(
            mode, key, result["ciphertext"],
            iv=result.get("iv"), nonce=result.get("nonce"), tag=result.get("tag")
        )
        
        if decrypted:
            print(f"{Fore.GREEN}SUCCESS: Déchiffré -> {decrypted.decode()}")
        else:
            print(f"{Fore.RED}ERROR: Échec du déchiffrement")

def main():
    while True:
        print_header("AES SECURITY LAB - MENU")
        print(f"{Fore.YELLOW}1.{Fore.WHITE} Tester AES (Modes classiques)")
        print(f"{Fore.YELLOW}2.{Fore.WHITE} Lancer les attaques (Démos)")
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
        elif choix == "0":
            print(f"{Fore.GREEN}Au revoir !")
            sys.exit()
        else:
            print(f"{Fore.RED}Option invalide, réessayez.")

if __name__ == "__main__":
    main()