import pyotp

secret = pyotp.random_base32()
print("Your secret key is:", secret)
