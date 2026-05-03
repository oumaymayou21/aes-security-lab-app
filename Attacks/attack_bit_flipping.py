from aes_modes import generate_key, encrypt, decrypt
from colorama import Fore

def run_bit_flipping_demo():
    print("\n--- BIT FLIPPING ATTACK ---")
    message = b"A" * 16 + b"montant=10000000" 
    key = generate_key()

    for mode in ["CBC", "CTR", "GCM"]:
        result = encrypt(mode, key, message)
        ct = bytearray(result["ciphertext"])

        ct[0] ^= 0xFF 
        
        try:
            decrypted = decrypt(
                mode, 
                key, 
                bytes(ct), 
                iv=result.get("iv"), 
                nonce=result.get("nonce"), 
                tag=result.get("tag")
            )
            
            if decrypted is None:
                print(f"{mode} \u2192 {Fore.GREEN}modification détectée \u2714\ufe0f")
            else:
                print(f"{mode} \u2192 {Fore.RED}message modifié accepté \u274c")
                
        except Exception:
            print(f"{mode} \u2192 {Fore.YELLOW}erreur (modification détectée ou crash de padding) \u2714\ufe0f")