from colorama import Fore, Style
from aes_modes import generate_key, encrypt

def run_ecb_demo():
    print(f"\n{Fore.CYAN}--- ECB PATTERN LEAK ATTACK ---")
    
    message = b"A" * 16 + b"B" * 16 + b"A" * 16
    key = generate_key()

    result = encrypt("ECB", key, message)
    ct = result["ciphertext"]

    block1 = ct[0:16]
    block2 = ct[16:32]
    block3 = ct[32:48]

    print(f"Bloc 1 chiffré : {block1.hex()[:20]}...")
    print(f"Bloc 2 chiffré : {block2.hex()[:20]}...")
    print(f"Bloc 3 chiffré : {block3.hex()[:20]}...")

    if block1 == block3:
        print(f"{Fore.RED}{Style.BRIGHT}RÉSULTAT : Patterns détectés \u2192 ECB non sécurisé \u274c")
        print(f"{Fore.YELLOW}(Le bloc 1 et le bloc 3 sont identiques dans le ciphertext !)")
    else:
        print(f"{Fore.GREEN}RÉSULTAT : Aucun pattern détecté \u2714\ufe0f")