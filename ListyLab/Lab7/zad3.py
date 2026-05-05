import random
import string
import pytest


class PasswordGenerator:
    def __init__(self, length, count, charset=string.ascii_letters + string.digits):
        self.length = length
        self.charset = charset
        self.count = count

    @property
    def charset(self):
        return self._charset

    @charset.setter
    def charset(self, value):
        if not value:
            raise ValueError("charset can't be empty")
        self._charset = value

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        if value <= 0:
            raise ValueError("length must be a positive number")
        self._length = value

    def generate_password(self):
        return ''.join(random.choice(self.charset) for _ in range(self.length))

    def __iter__(self):
        return self

    def __next__(self):
        if self.count <= 0:
            raise StopIteration
        self.count -= 1
        return self.generate_password()


def test_password_constraints():
    length = 5
    generator = PasswordGenerator(length=length, count=1)
    reslt = next(generator)

    assert len(reslt) == length
    with pytest.raises(StopIteration):
        next(generator)


def test_empty_charset_raises_error():
    with pytest.raises(ValueError, match="charset can't be empty"):
        PasswordGenerator(length=5, count=1, charset="")


def test_invalid_length():
    with pytest.raises(ValueError, match="length must be a positive number"):
        PasswordGenerator(length=0, count=1)


def test_negative_count_behavior():
    generator = PasswordGenerator(length=10, count=-5)
    with pytest.raises(StopIteration):
        next(generator)
