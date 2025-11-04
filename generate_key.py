import secrets
import os

key = secrets.token_urlsafe(32)
print(f"Your new SECRET_KEY is:\n{key}")