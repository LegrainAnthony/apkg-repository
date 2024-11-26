import hashlib

SECRET_KEY = os.getenv("HMAC_KEY")

hashed_secret_key = hashlib.sha256(SECRET_KEY.encode()).hexdigest()
print(f"Hashed key: {hashed_secret_key}")