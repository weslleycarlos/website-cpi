# generate_secret_key.py
import secrets

def generate_secret_key():
    return secrets.token_hex(32)

if __name__ == '__main__':
    print("SUA NOVA CHAVE SECRETA:")
    print(generate_secret_key())
    print("\nAdicione esta chave ao seu .env como SECRET_KEY")