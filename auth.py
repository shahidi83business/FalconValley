from models import User
import hashlib
import uuid

def hash_password(password):
    # Hash the password with a salt
    salt = uuid.uuid4().hex
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(stored_password, provided_password):
    # Verify the provided password against the stored password
    salt, hashed = stored_password.split('$')
    return hashed == hashlib.sha256((provided_password + salt).encode()).hexdigest()

def register(username, password):
    # Register a new user
    if User.objects(username=username).first():
        return "User already exists."

    hashed_password = hash_password(password)
    user = User(username=username, password=hashed_password)
    user.save()
    return "User registered successfully."

def login(username, password):
    # Login a user
    user = User.objects(username=username).first()
    if not user:
        return "User not found."

    if verify_password(user.password, password):
        return "Login successful."
    else:
        return "Invalid password."

def forget_password(username, new_password):
    # Reset a user's password
    user = User.objects(username=username).first()
    if not user:
        return "User not found."

    hashed_password = hash_password(new_password)
    user.password = hashed_password
    user.save()
    return "Password reset successfully."