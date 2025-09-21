# create_hash.py
# verify_pw.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = "$2b$12$OIat1QzUgw7sjpDmjV4jveVeTb7/NFzSPxEe6q/fU8kua/ty1ek5a"
print(pwd_context.verify("Ravi@1234", hashed))


'''from passlib.context import CryptContext

# Create a bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Replace this with your desired password
password = "Ravi@1234"

# Generate hash
hashed_pw = pwd_context.hash(password)

print("Hashed password:", hashed_pw)'''
