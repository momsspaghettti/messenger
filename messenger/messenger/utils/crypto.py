import hashlib
import datetime


def compute_sha512_hash(data: str) -> str:
    return hashlib.sha512(data.encode('utf-8')).hexdigest().upper()


def is_correct_password(password: str, password_hash: str) -> bool:
    return compute_sha512_hash(password) == password_hash


def compute_session_id(login: str, password_hash: str) -> str:
    return compute_sha512_hash(login + password_hash + str(datetime.datetime.now().timestamp()))
