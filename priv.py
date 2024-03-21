class CaesarCipher:
    def __init__(self):
        self.shift = 3

    def encrypt_message(self, message):
        encrypted_message = ''
        for char in message:
            if char.isalpha():
                shifted_char = chr((ord(char) + self.shift - ord('A')) % 26 + ord('A')) if char.isupper() \
                    else chr((ord(char) + self.shift - ord('a')) % 26 + ord('a'))
                encrypted_message += shifted_char
            else:
                encrypted_message += char
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        decrypted_message = ''
        for char in encrypted_message:
            if char.isalpha():
                shifted_char = chr((ord(char) - self.shift - ord('A')) % 26 + ord('A')) if char.isupper() \
                    else chr((ord(char) - self.shift - ord('a')) % 26 + ord('a'))
                decrypted_message += shifted_char
            else:
                decrypted_message += char
        return decrypted_message

# Example usage
message = "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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"

cipher = CaesarCipher()
encrypted_message = cipher.encrypt_message(message)
print("Encrypted message:", encrypted_message)

decrypted_message = cipher.decrypt_message(encrypted_message)
print("Decrypted message:", decrypted_message)
