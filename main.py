from aes_modes import generate_key, encrypt, decrypt

def demo():
    message = input("Message : ").encode()
    key = generate_key()

    for mode in ["ECB", "CBC", "CTR", "GCM"]:
        print(f"\n=== {mode} ===")

        result = encrypt(mode, key, message)
        print("Ciphertext:", result["ciphertext"].hex())

        decrypted = decrypt(
            mode,
            key,
            result["ciphertext"],
            iv=result.get("iv"),
            nonce=result.get("nonce"),
            tag=result.get("tag")
        )

        print("Decrypted:", decrypted)

def main():
    while True:
        print("\n===== AES SECURITY LAB =====")
        print("1. Tester AES")
        print("0. Quitter")

        choix = input("Choix : ")

        if choix == "1":
            demo()
        elif choix == "0":
            break
        else:
            print("Erreur")

if __name__ == "__main__":
    main()