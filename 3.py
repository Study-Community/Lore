import random
import string

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    print(f"Generated password: {password}")

if __name__ == "__main__":
    length = int(input("Enter password length: "))
    generate_password(length)