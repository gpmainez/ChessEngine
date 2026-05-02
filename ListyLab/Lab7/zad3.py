import random
import string


class PasswordGenerator:
    def __init__(self, length, count, charset=string.ascii_letters + string.digits ):
        self.length = length
        self.charset = charset
        self.count = count

    def generate_password(self):
        password = ''.join(random.choice(self.charset) for _ in range(self.length))
        return password

    def __iter__(self):
        return self

    def __next__(self):
        self.count -= 1
        if self.count < 0:
            raise StopIteration
        return self.generate_password()


passw = PasswordGenerator(10,8, string.ascii_letters + string.digits)
print(next(passw))
for passwor in passw:
    print(passwor)