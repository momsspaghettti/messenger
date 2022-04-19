import random
import string

letters: str = string.ascii_letters + string.digits


def random_str(min_len: int = 1, max_len: int = 255) -> str:
    return get_random_str(random.randint(min_len, max_len))


def utc_offset():
    return random.randint(-24, 24)


def get_random_str(length: int) -> str:
    return ''.join(random.choice(letters) for _ in range(length))
